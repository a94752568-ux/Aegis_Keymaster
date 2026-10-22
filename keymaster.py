"""
KeyMaster // ORBITAL TRAINER
SpaceX-Cyberpunk UI · modos de tecleo, aprendizaje y constructor.
IA local opcional via Ollama (modelo, ratio, adaptativo).
Contratos diarios (3 misiones/día).
"""
import customtkinter as ctk
import time
from sound_engine import SoundEngine
from profile_manager import PlayerProfile
from content_generator import ContentGenerator
from tips_system import TipsSystem
from constructor_mode import ConstructorMixin
try:
    from contracts_ui import ContractsUIMixin
except Exception:
    class ContractsUIMixin:
        def _build_contracts_chip(self, parent):
            self.lbl_contracts = ctk.CTkLabel(parent, text="Contratos 0/3", font=("Segoe UI", 12), text_color=THEME["amber"])
            self.lbl_contracts.pack(anchor="e")
        def _refresh_contracts_label(self):
            pass
        def _show_contracts_panel(self):
            pass
        def _toast_contract(self, message, color=None):
            try:
                self.lbl_feedback.configure(text=str(message))
            except Exception:
                pass

try:
    from ollama_tutor import get_tutor
except Exception:
    get_tutor = None
try:
    from splash_screen import show_splash
except Exception:
    show_splash = None

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

THEME = {
    "bg": "#05070B", "surface": "#0B1018", "surface2": "#111827", "panel": "#0E1522",
    "border": "#1E2A3A", "cyan": "#00E5FF", "cyan_dim": "#00A8B8", "magenta": "#FF2BD6",
    "magenta_dim": "#B01A96", "amber": "#FFB020", "lime": "#39FF14", "red": "#FF3355",
    "red_dim": "#C91838", "violet": "#A855F7", "violet_dim": "#7C3AED",
    "text": "#E8F1FF", "muted": "#6B7C93", "ghost": "#3A4A5C",
}

class KeyMasterApp(ContractsUIMixin, ConstructorMixin, ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("KeyMaster // ORBITAL TRAINER")
        self.geometry("1180x780")
        self.configure(fg_color=THEME["bg"])
        self.player = PlayerProfile()
        self.content = ContentGenerator()
        self.audio = SoundEngine()
        self.tips = TipsSystem()
        self.mode = "TRAINING"
        self.current_learning_path = getattr(self.player, "current_learning_path", "basics")
        self.current_code_category = "basic_functions"
        self.lives = 3
        self.survival_score = 0
        self.survival_difficulty = 1
        self.combo = 0
        self.current_challenge = None
        self.current_text = ""
        self.start_time = 0
        self.is_typing = False
        self.last_len = 0
        self.error_count = 0
        self._pending_explanation = ""
        self._builder_exercise = None
        self._builder_revealed = 0
        self._builder_used_scaffold = False
        self._builder_used_reveal = False
        self._builder_used_solution = False
        self.use_ai = False
        self.tutor = None
        self._stats_win = None
        if get_tutor:
            try:
                self.tutor = get_tutor(force_refresh=True)
            except Exception:
                self.tutor = None
        self._build_ui()
        self._set_mode("TRAINING")
        try:
            self.player.ensure_daily_contracts()
            self._refresh_contracts_label()
        except Exception:
            pass

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=16, pady=8)
        left = ctk.CTkFrame(header, fg_color="transparent")
        left.pack(side="left")
        self.lbl_level = ctk.CTkLabel(left, text="LVL 1", font=("Segoe UI", 24, "bold"), text_color=THEME["cyan"])
        self.lbl_level.pack(anchor="w")
        self.lbl_rank = ctk.CTkLabel(left, text="Novato", font=("Segoe UI", 12), text_color=THEME["muted"])
        self.lbl_rank.pack(anchor="w")
        self.mode_panel = ctk.CTkSegmentedButton(
            header, values=["ENTRENAMIENTO", "APRENDIZAJE", "CONSTRUCTOR", "SUPERVIVENCIA", "DIARIO"],
            command=self._on_mode, font=("Segoe UI", 11, "bold"),
            fg_color=THEME["surface"], selected_color=THEME["cyan_dim"], selected_hover_color=THEME["cyan"],
            unselected_color=THEME["surface2"], unselected_hover_color=THEME["panel"], text_color=THEME["text"])
        self.mode_panel.set("ENTRENAMIENTO")
        self.mode_panel.pack(side="top", pady=4)
        ai_row = ctk.CTkFrame(header, fg_color="transparent")
        ai_row.pack(side="top", pady=(2, 0))
        self.ai_switch = ctk.CTkSwitch(ai_row, text="IA local", command=self._toggle_ai, font=("Segoe UI", 11),
            progress_color=THEME["cyan"], button_color=THEME["cyan"], button_hover_color=THEME["magenta"], text_color=THEME["text"])
        self.ai_switch.pack(side="left", padx=4)
        self.lbl_ai = ctk.CTkLabel(ai_row, text="Ollama offline", font=("Segoe UI", 11), text_color=THEME["ghost"])
        self.lbl_ai.pack(side="left", padx=4)
        self.model_menu = ctk.CTkOptionMenu(ai_row, values=["(sin modelos)"], command=self._on_model_change, width=140, height=24, font=("Segoe UI", 10),
            fg_color=THEME["surface2"], button_color=THEME["cyan_dim"], button_hover_color=THEME["cyan"], text_color=THEME["text"],
            dropdown_fg_color=THEME["panel"], dropdown_hover_color=THEME["surface2"], dropdown_text_color=THEME["text"])
        self.model_menu.pack(side="left", padx=4)
        self.model_menu.configure(state="disabled")
        self.adaptive_switch = ctk.CTkSwitch(ai_row, text="Adaptativo", command=self._toggle_adaptive, font=("Segoe UI", 11),
            progress_color=THEME["magenta"], button_color=THEME["magenta"], button_hover_color=THEME["cyan"], text_color=THEME["text"])
        self.adaptive_switch.select()
        self.adaptive_switch.pack(side="left", padx=4)
        ctk.CTkLabel(ai_row, text="Ratio IA", font=("Segoe UI", 10), text_color=THEME["muted"]).pack(side="left", padx=(8, 2))
        self.ratio_slider = ctk.CTkSlider(ai_row, from_=0, to=100, number_of_steps=20, command=self._on_ratio_change, width=90, height=16,
            progress_color=THEME["cyan"], button_color=THEME["cyan"], button_hover_color=THEME["magenta"], fg_color=THEME["surface2"])
        self.ratio_slider.set(55)
        self.ratio_slider.pack(side="left", padx=2)
        self.lbl_ratio = ctk.CTkLabel(ai_row, text="55%", font=("Segoe UI", 10, "bold"), text_color=THEME["cyan"], width=36)
        self.lbl_ratio.pack(side="left")
        self._refresh_ai_status()
        right = ctk.CTkFrame(header, fg_color="transparent")
        right.pack(side="right")
        self.lbl_combo = ctk.CTkLabel(right, text="", font=("Segoe UI", 18, "bold"), text_color=THEME["magenta"])
        self.lbl_combo.pack(anchor="e")
        self._build_contracts_chip(right)
        self.lbl_wpm = ctk.CTkLabel(right, text="WPM: 0", font=("Segoe UI", 14), text_color=THEME["text"])
        self.lbl_wpm.pack(anchor="e")
        pw = ctk.CTkFrame(right, fg_color="transparent")
        pw.pack(anchor="e", pady=4)
        self.btn_hint = ctk.CTkButton(pw, text="Pista", width=70, height=28, command=lambda: self._power("hint"),
            fg_color=THEME["surface2"], hover_color=THEME["violet_dim"], border_width=1, border_color=THEME["violet"], text_color=THEME["text"], corner_radius=6)
        self.btn_hint.pack(side="left", padx=2)
        self.btn_skip = ctk.CTkButton(pw, text="Saltar", width=70, height=28, command=lambda: self._power("skip"),
            fg_color=THEME["surface2"], hover_color=THEME["cyan_dim"], border_width=1, border_color=THEME["cyan"], text_color=THEME["text"], corner_radius=6)
        self.btn_skip.pack(side="left", padx=2)
        self.btn_stats = ctk.CTkButton(pw, text="Stats", width=70, height=28, command=self._show_stats,
            fg_color=THEME["surface2"], hover_color=THEME["magenta_dim"], border_width=1, border_color=THEME["magenta"], text_color=THEME["text"], corner_radius=6)
        self.btn_stats.pack(side="left", padx=2)
        self.area = ctk.CTkScrollableFrame(self, fg_color="transparent", scrollbar_button_color=THEME["cyan_dim"], scrollbar_button_hover_color=THEME["cyan"])
        self.area.grid(row=1, column=0, sticky="nsew", padx=20, pady=8)
        self.path_frame = ctk.CTkFrame(self.area, fg_color=THEME["panel"], corner_radius=12, border_width=1, border_color=THEME["cyan_dim"])
        ctk.CTkLabel(self.path_frame, text="◈ RUTA DE APRENDIZAJE", font=("Segoe UI", 13, "bold"), text_color=THEME["cyan"]).pack(pady=(8, 4))
        self.path_selector = ctk.CTkOptionMenu(self.path_frame, values=self.content.get_available_paths(), command=self._on_path_change, font=("Segoe UI", 12),
            fg_color=THEME["surface2"], button_color=THEME["cyan_dim"], button_hover_color=THEME["cyan"], text_color=THEME["text"],
            dropdown_fg_color=THEME["panel"], dropdown_hover_color=THEME["surface2"], dropdown_text_color=THEME["text"])
        self.path_selector.set(self.current_learning_path)
        self.path_selector.pack(pady=(0, 8), padx=10)
        self.cat_frame = ctk.CTkFrame(self.area, fg_color=THEME["panel"], corner_radius=12, border_width=1, border_color=THEME["magenta_dim"])
        ctk.CTkLabel(self.cat_frame, text="◈ CATEGORIA DE CODIGO", font=("Segoe UI", 13, "bold"), text_color=THEME["magenta"]).pack(pady=(8, 4))
        cats = self.content.get_code_builder_categories()
        self.cat_selector = ctk.CTkOptionMenu(self.cat_frame, values=cats, command=self._on_category_change, font=("Segoe UI", 12),
            fg_color=THEME["surface2"], button_color=THEME["magenta_dim"], button_hover_color=THEME["magenta"], text_color=THEME["text"],
            dropdown_fg_color=THEME["panel"], dropdown_hover_color=THEME["surface2"], dropdown_text_color=THEME["text"])
        if cats:
            self.cat_selector.set(cats[0])
            self.current_code_category = cats[0]
        self.cat_selector.pack(pady=(0, 8), padx=10)
        self.lbl_diff = ctk.CTkLabel(self.area, text="", font=("Consolas", 12), text_color=THEME["ghost"])
        self.lbl_diff.pack(pady=(12, 4))
        self.lbl_concept = ctk.CTkLabel(self.area, text="", font=("Segoe UI", 11), text_color=THEME["muted"])
        self.lbl_concept.pack()
        self.lbl_desc = ctk.CTkLabel(self.area, text="", font=("Segoe UI", 13), text_color=THEME["muted"], wraplength=850)
        self.lbl_target = ctk.CTkLabel(self.area, text="...", font=("JetBrains Mono", 26, "bold"), wraplength=900, text_color=THEME["text"])
        self.lbl_target.pack(pady=12)
        self.lbl_tip = ctk.CTkLabel(self.area, text="", font=("Segoe UI", 12), text_color=THEME["amber"], wraplength=850)
        self.lbl_hint = ctk.CTkLabel(self.area, text="", font=("Segoe UI", 12), text_color=THEME["cyan"], wraplength=850)
        self.entry_var = ctk.StringVar()
        self.entry_var.trace_add("write", self._on_type)
        self.entry = ctk.CTkEntry(self.area, textvariable=self.entry_var, width=720, height=56, font=("JetBrains Mono", 22), justify="center", corner_radius=10, border_width=2,
            fg_color=THEME["surface"], border_color=THEME["cyan_dim"], text_color=THEME["cyan"], placeholder_text_color=THEME["ghost"])
        self.entry.pack(pady=12)
        self.code_textbox = ctk.CTkTextbox(self.area, width=780, height=260, font=("JetBrains Mono", 14), corner_radius=10, border_width=2, wrap="none",
            fg_color=THEME["surface"], border_color=THEME["cyan_dim"], text_color=THEME["text"])
        self.code_textbox.bind("<Control-Return>", lambda e: self._verify_code())
        self.lbl_feedback = ctk.CTkLabel(self.area, text="// SISTEMA LISTO — escribe para iniciar", font=("Segoe UI", 14), text_color=THEME["muted"])
        self.lbl_feedback.pack(pady=4)
        self.btn_verify = ctk.CTkButton(self.area, text="⚡ VERIFICAR  ·  Ctrl+Enter", command=self._verify_code,
            fg_color=THEME["lime"], hover_color="#2BD910", font=("Segoe UI", 14, "bold"), height=44, width=300, border_width=2, border_color=THEME["lime"], text_color=THEME["bg"], corner_radius=8)
        self.builder_btns = ctk.CTkFrame(self.area, fg_color="transparent")
        self.btn_scaffold = ctk.CTkButton(self.builder_btns, text="Scaffold", width=100, height=32, command=self._load_scaffold, fg_color=THEME["cyan_dim"], hover_color=THEME["cyan"], border_width=1, border_color=THEME["cyan"], text_color=THEME["bg"], font=("Segoe UI", 12, "bold"), corner_radius=8)
        self.btn_scaffold.pack(side="left", padx=4)
        self.btn_reveal = ctk.CTkButton(self.builder_btns, text="Revelar linea", width=120, height=32, command=self._reveal_line, fg_color=THEME["violet_dim"], hover_color=THEME["violet"], border_width=1, border_color=THEME["violet"], text_color=THEME["text"], font=("Segoe UI", 12, "bold"), corner_radius=8)
        self.btn_reveal.pack(side="left", padx=4)
        self.btn_solution = ctk.CTkButton(self.builder_btns, text="Ver solucion", width=120, height=32, command=self._show_solution, fg_color=THEME["red_dim"], hover_color=THEME["red"], border_width=1, border_color=THEME["red"], text_color=THEME["text"], font=("Segoe UI", 12, "bold"), corner_radius=8)
        self.btn_solution.pack(side="left", padx=4)
        self.btn_ai_hint = ctk.CTkButton(self.builder_btns, text="Tutor IA", width=100, height=32, command=self._ai_builder_hint, fg_color=THEME["magenta_dim"], hover_color=THEME["magenta"], border_width=1, border_color=THEME["magenta"], text_color=THEME["text"], font=("Segoe UI", 12, "bold"), corner_radius=8)
        self.btn_ai_hint.pack(side="left", padx=4)
        self.btn_next_ex = ctk.CTkButton(self.builder_btns, text="Siguiente", width=100, height=32, command=self._new_code_builder_exercise, fg_color=THEME["surface2"], hover_color=THEME["panel"], border_width=1, border_color=THEME["border"], text_color=THEME["text"], font=("Segoe UI", 12, "bold"), corner_radius=8)
        self.btn_next_ex.pack(side="left", padx=4)
        self.progress = ctk.CTkProgressBar(self, height=10, progress_color=THEME["cyan"], fg_color=THEME["surface2"], corner_radius=4)
        self.progress.grid(row=2, column=0, sticky="ew")
        self.entry.focus()

    def _on_mode(self, value):
        m = {"ENTRENAMIENTO": "TRAINING", "APRENDIZAJE": "LEARNING", "CONSTRUCTOR": "CODE_BUILDER", "SUPERVIVENCIA": "SURVIVAL", "DIARIO": "DAILY"}
        self._set_mode(m.get(value, "TRAINING"))

    def _on_path_change(self, path):
        self.current_learning_path = path
        try:
            self.player.current_learning_path = path
            self.player.save_profile()
        except Exception:
            pass
        self._new_challenge()

    def _on_category_change(self, category):
        self.current_code_category = category
        self._new_code_builder_exercise()

    def _set_mode(self, mode):
        self.mode = mode
        self.combo = 0
        self.lives = 3
        self.lbl_combo.configure(text="")
        self.path_frame.pack_forget()
        self.cat_frame.pack_forget()
        self.lbl_desc.pack_forget()
        self.lbl_tip.pack_forget()
        self.lbl_hint.pack_forget()
        self.code_textbox.pack_forget()
        self.btn_verify.pack_forget()
        try:
            self.builder_btns.pack_forget()
        except Exception:
            pass
        self.entry.pack_forget()
        self.lbl_target.pack_forget()
        if mode == "TRAINING":
            self.lbl_level.configure(text=f"LVL {self.player.level}")
            self.lbl_rank.configure(text=self.player.rank)
            self.lbl_target.pack(pady=12)
            self.entry.pack(pady=12)
            self._new_challenge()
            self.entry.focus()
        elif mode == "LEARNING":
            self.path_frame.pack(pady=(4, 8))
            self.lbl_level.configure(text=f"LVL {self.player.level}")
            self.lbl_rank.configure(text=self.player.rank)
            self.lbl_target.pack(pady=12)
            self.entry.pack(pady=12)
            self._new_challenge()
            self.entry.focus()
        elif mode == "CODE_BUILDER":
            self._start_code_builder()
        elif mode == "SURVIVAL":
            self.survival_score = 0
            self.survival_difficulty = 1
            self.lbl_level.configure(text="SCORE 0")
            self.lbl_rank.configure(text=f"Vidas: {self.lives}")
            self.lbl_target.pack(pady=12)
            self.entry.pack(pady=12)
            self._new_challenge()
            self.entry.focus()
        else:
            self.lbl_level.configure(text="DIARIO")
            self.lbl_rank.configure(text=f"Racha: {getattr(self.player, 'daily_streak', 0)}")
            self.lbl_target.pack(pady=12)
            self.entry.pack(pady=12)
            self._new_challenge()
            self.entry.focus()

    def _new_challenge(self):
        self._sync_learner_context()
        if self.mode == "CODE_BUILDER":
            self._new_code_builder_exercise()
            return
        if self.mode == "TRAINING":
            diff = min(10, max(1, self.player.level // 2 or 1))
            self.current_challenge = self.content.get_challenge(diff)
        elif self.mode == "LEARNING":
            diff = min(8, 2 + self.player.level // 3)
            self.current_challenge = self.content.get_challenge(diff, self.current_learning_path, prefer_blank=True)
        elif self.mode == "SURVIVAL":
            self.current_challenge = self.content.get_challenge(self.survival_difficulty)
        else:
            dailies = self.content.get_daily_challenges()
            self.current_challenge = dailies[0] if dailies else self.content.get_challenge(3)
        self._show_challenge()

    def _show_challenge(self):
        ch = self.current_challenge
        if not ch:
            return
        self.current_text = ch.text
        self.error_count = 0
        self.last_len = 0
        self.is_typing = False
        self.start_time = 0
        display = self.content.get_challenge_display_text(ch)
        is_blank = getattr(ch, "challenge_type", "full") == "blank"
        if is_blank:
            self.lbl_target.configure(text=display, text_color=THEME["amber"])
            self.lbl_feedback.configure(text="Completa el hueco ____", text_color=THEME["amber"])
        else:
            self.lbl_target.configure(text=display, text_color=THEME["text"])
            self.lbl_feedback.configure(text="Escribe el codigo", text_color=THEME["muted"])
        self.lbl_diff.configure(text=f"Nivel {ch.difficulty} | {ch.category}")
        self.lbl_concept.configure(text=f"Concepto: {ch.concept}" if self.mode == "LEARNING" else "")
        self.lbl_hint.configure(text="")
        self.lbl_hint.pack_forget()
        self.entry_var.set("")
        self.entry.configure(border_color=THEME["cyan_dim"])

    def _on_type(self, *args):
        if self.mode == "CODE_BUILDER":
            return
        text = self.entry_var.get()
        target = self.current_text
        if not self.is_typing and text:
            self.is_typing = True
            self.start_time = time.time()
        if len(text) > self.last_len:
            if target.startswith(text):
                try:
                    self.audio.play_click()
                except Exception:
                    pass
                self.entry.configure(border_color=THEME["lime"])
            else:
                self.error_count += 1
                try:
                    self.audio.play_error()
                except Exception:
                    pass
                self.entry.configure(border_color=THEME["red"])
                if self.mode == "SURVIVAL":
                    self.lives -= 1
                    self.combo = 0
                    self.lbl_rank.configure(text=f"Vidas: {self.lives}")
                    try:
                        if self.current_challenge:
                            self.player.record_concept_fail(self.current_challenge.concept, errors=1)
                    except Exception:
                        pass
                    if self.lives <= 0:
                        self.lbl_feedback.configure(text="Game Over", text_color=THEME["red"])
                        try:
                            self.audio.play_gameover()
                        except Exception:
                            pass
                        self.after(1500, lambda: self._set_mode("SURVIVAL"))
                        self.last_len = len(text)
                        return
        self.last_len = len(text)
        if text == target and target:
            self._success()

    def _success(self):
        duration = max(0.001, time.time() - self.start_time)
        words = max(1, len(self.current_text.split()))
        wpm = int((words / duration) * 60)
        perfect = self.error_count == 0
        self.lbl_wpm.configure(text=f"WPM: {wpm}")
        self.combo = self.combo + 1 if perfect else 0
        self.lbl_combo.configure(text=f"x{self.combo}" if self.combo > 1 else "")
        concept = self.current_challenge.concept if self.current_challenge else ""
        try:
            self.player.record_challenge_completion(wpm, self.error_count, len(self.current_text), concept, perfect)
        except Exception:
            pass
        try:
            just = []
            if self.mode == "TRAINING":
                just = self.player.bump_contract("training_ok", 1)
            elif self.mode == "LEARNING":
                just = self.player.bump_contract("learning_ok", 1)
                is_blank = getattr(self.current_challenge, "challenge_type", "full") == "blank"
                if is_blank and perfect:
                    just = list(just) + list(self.player.bump_contract("blank_perfect", 1) or [])
                try:
                    due = set(self.player.get_due_concepts(limit=20))
                    if concept and concept in due:
                        just = list(just) + list(self.player.bump_contract("due_review", 1) or [])
                except Exception:
                    pass
            elif self.mode == "SURVIVAL":
                just = self.player.bump_contract("survival_score", getattr(self, "survival_score", 0))
            if just:
                labels = ", ".join((c.get("label") or c.get("id", "?"))[:48] for c in just)
                self._toast_contract(f"◆ Contrato listo: {labels}", THEME["amber"])
                try:
                    info = self.player.get_contracts_progress()
                    if info.get("all_done") and not info.get("claimed"):
                        self.after(600, self._show_contracts_panel)
                except Exception:
                    pass
            self._refresh_contracts_label()
        except Exception:
            pass
        exp = self.content.get_explanation(concept, self.current_challenge)
        self._pending_explanation = exp or ""
        if self.mode == "TRAINING":
            base = 10 + len(self.current_text)
            total = int(base * (1 + 0.1 * max(0, self.combo - 1)))
            leveled = self.player.add_xp(total)
            self.lbl_feedback.configure(text=f"+{total} XP", text_color=THEME["lime"])
            self.lbl_level.configure(text=f"LVL {self.player.level}")
            self.lbl_rank.configure(text=self.player.rank)
            if leveled:
                try:
                    self.audio.play_levelup()
                except Exception:
                    pass
            need = max(1, self.player.xp_for_next_level)
            self.progress.set(min(1.0, self.player.xp / need))
        elif self.mode == "LEARNING":
            base = 15 + len(self.current_text)
            if getattr(self.current_challenge, "challenge_type", "full") == "blank":
                base += 5
            self.player.add_xp(base)
            self.lbl_feedback.configure(text=f"+{base} XP (aprendizaje)", text_color=THEME["cyan"])
        elif self.mode == "SURVIVAL":
            self.survival_score += 10 + self.survival_difficulty
            if self.combo and self.combo % 5 == 0:
                self.survival_difficulty = min(12, self.survival_difficulty + 1)
            self.lbl_level.configure(text=f"SCORE {self.survival_score}")
            self.lbl_feedback.configure(text="OK", text_color=THEME["lime"])
            try:
                self.player.bump_contract("survival_score", self.survival_score)
                self._refresh_contracts_label()
            except Exception:
                pass
        else:
            self.lbl_feedback.configure(text="Desafio diario OK", text_color=THEME["amber"])
        if self._pending_explanation:
            self.lbl_hint.configure(text=f"📖 {self._pending_explanation}")
            self.lbl_hint.pack(before=self.entry, pady=(0, 8))
        self.after(1200, self._new_challenge)

    def _power(self, kind):
        try:
            ok = self.player.use_powerup(kind)
        except Exception:
            ok = False
        if not ok:
            self.lbl_feedback.configure(text="Sin power-up", text_color=THEME["red"])
            return
        try:
            self.audio.play_powerup()
        except Exception:
            pass
        if kind == "hint" and self.current_challenge:
            parts = [f"💡 {self.current_challenge.hint or 'Sigue el patron'}"]
            exp = self.content.get_explanation(self.current_challenge.concept, self.current_challenge)
            if exp:
                parts.append(f"📖 {exp}")
            self.lbl_hint.configure(text="\n".join(parts))
            self.lbl_hint.pack(before=self.entry, pady=(0, 8))
        elif kind == "skip":
            self.after(200, self._new_code_builder_exercise if self.mode == "CODE_BUILDER" else self._new_challenge)

    def _refresh_ai_status(self):
        if not get_tutor:
            self.lbl_ai.configure(text="Modulo ollama no cargado", text_color=THEME["ghost"])
            try:
                self.model_menu.configure(values=["(sin modelos)"], state="disabled")
            except Exception:
                pass
            return
        try:
            if self.tutor is None:
                self.tutor = get_tutor(force_refresh=True)
            else:
                self.tutor.refresh()
            if self.tutor.is_available():
                models = self.tutor.list_models() or [self.tutor.model or "?"]
                self.model_menu.configure(values=models, state="normal")
                current = self.tutor.model or models[0]
                if current not in models:
                    current = models[0]
                    self.tutor.set_model(current)
                self.model_menu.set(current)
                self.lbl_ai.configure(text="online", text_color=THEME["lime"])
            else:
                self.lbl_ai.configure(text="offline", text_color=THEME["ghost"])
                self.model_menu.configure(values=["(sin modelos)"], state="disabled")
        except Exception:
            self.lbl_ai.configure(text="offline", text_color=THEME["ghost"])

    def _on_model_change(self, name: str):
        if not self.tutor or not name or name.startswith("("):
            return
        ok = self.tutor.set_model(name)
        self.lbl_feedback.configure(text=f"Modelo: {self.tutor.model}" if ok else f"No se pudo seleccionar {name}", text_color=THEME["lime"] if ok else THEME["red"])

    def _on_ratio_change(self, value):
        pct = int(round(float(value)))
        self.lbl_ratio.configure(text=f"{pct}%")
        self.content.set_ai_ratio(pct / 100.0)

    def _toggle_adaptive(self):
        enabled = bool(self.adaptive_switch.get())
        self.content.set_adaptive(enabled)
        self._sync_learner_context()
        self.lbl_feedback.configure(text="Modo adaptativo ON · refuerza conceptos debiles" if enabled else "Modo adaptativo OFF", text_color=THEME["cyan"] if enabled else THEME["muted"])

    def _sync_learner_context(self):
        try:
            weak = self.player.get_weak_concepts(limit=6)
        except Exception:
            weak = []
        try:
            due = self.player.get_due_concepts(limit=8)
        except Exception:
            due = []
        self.content.set_learner_context(weak_concepts=weak, level=self.player.level, due_concepts=due)

    def _toggle_ai(self):
        self.use_ai = bool(self.ai_switch.get())
        self._refresh_ai_status()
        if self.use_ai:
            if not self.tutor or not self.tutor.is_available():
                self.use_ai = False
                self.ai_switch.deselect()
                self.lbl_feedback.configure(text="Ollama no responde. Instala ollama.com y: ollama pull llama3.2", text_color=THEME["amber"])
                return
            self.content.set_ai(True, self.tutor)
            self.content.set_ai_ratio(float(self.ratio_slider.get()) / 100.0)
            self.content.set_adaptive(bool(self.adaptive_switch.get()))
            self._sync_learner_context()
            self.lbl_feedback.configure(text=f"IA activa · {self.tutor.model} · ratio {int(self.ratio_slider.get())}%", text_color=THEME["lime"])
        else:
            self.content.set_ai(False, self.tutor)
            self.lbl_feedback.configure(text="IA desactivada · banco fijo de ejercicios", text_color=THEME["muted"])

    def _concept_mastery_rows(self, limit: int = 12):
        rows = []
        stats = getattr(self.player, "concept_stats", {}) or {}
        for concept, st in stats.items():
            attempts = max(1, int(st.get("attempts", 0) or 0))
            successes = int(st.get("successes", 0) or 0)
            fails = int(st.get("fails", 0) or 0)
            errors = int(st.get("errors", 0) or 0)
            success_rate = successes / attempts
            fail_rate = fails / attempts
            mastery = max(0.0, min(1.0, success_rate * (1.0 - 0.5 * fail_rate)))
            struggle = fail_rate * 2.0 + (errors / attempts) * 0.5
            if successes == 0 and attempts >= 1:
                struggle += 0.4
            rows.append({"concept": concept, "mastery": mastery, "struggle": struggle, "attempts": attempts, "successes": successes, "fails": fails, "errors": errors})
        rows.sort(key=lambda r: (-r["struggle"], -r["attempts"]))
        return rows[:limit]

    def _show_stats(self):
        if getattr(self, "_stats_win", None) is not None:
            try:
                if self._stats_win.winfo_exists():
                    self._stats_win.lift()
                    self._stats_win.focus()
                    return
            except Exception:
                pass
        win = ctk.CTkToplevel(self)
        self._stats_win = win
        win.title("KeyMaster // TELEMETRIA")
        win.geometry("520x720")
        win.configure(fg_color=THEME["bg"])
        try:
            win.transient(self)
        except Exception:
            pass
        ctk.CTkLabel(win, text="◈ TELEMETRIA ORBITAL", font=("Segoe UI", 18, "bold"), text_color=THEME["cyan"]).pack(pady=(16, 4))
        try:
            summary = self.player.get_stats_summary()
        except Exception:
            summary = {"level": self.player.level, "xp": self.player.xp, "rank": getattr(self.player, "rank", "?"), "accuracy": 100, "challenges": 0, "perfect": 0, "best_wpm": 0, "survival": 0, "streak": 0, "weak": []}
        card = ctk.CTkFrame(win, fg_color=THEME["panel"], corner_radius=12, border_width=1, border_color=THEME["cyan_dim"])
        card.pack(fill="x", padx=16, pady=8)
        grid = ctk.CTkFrame(card, fg_color="transparent")
        grid.pack(fill="x", padx=12, pady=12)
        def cell(parent, title, value, color):
            f = ctk.CTkFrame(parent, fg_color=THEME["surface"], corner_radius=8)
            f.pack(side="left", expand=True, fill="x", padx=4)
            ctk.CTkLabel(f, text=title, font=("Segoe UI", 10), text_color=THEME["muted"]).pack(pady=(6, 0))
            ctk.CTkLabel(f, text=str(value), font=("Segoe UI", 16, "bold"), text_color=color).pack(pady=(0, 6))
        row1 = ctk.CTkFrame(grid, fg_color="transparent")
        row1.pack(fill="x", pady=2)
        cell(row1, "NIVEL", summary.get("level", 1), THEME["cyan"])
        cell(row1, "XP", summary.get("xp", 0), THEME["lime"])
        cell(row1, "RANGO", summary.get("rank", "?"), THEME["magenta"])
        ctk.CTkButton(win, text="Ver contratos del dia", width=200, height=32, command=lambda: (win.destroy(), self._show_contracts_panel()),
            fg_color=THEME["amber"], hover_color="#E09A10", text_color=THEME["bg"], font=("Segoe UI", 12, "bold")).pack(pady=8)
        ctk.CTkButton(win, text="Cerrar", width=120, height=32, command=win.destroy, fg_color=THEME["surface2"], hover_color=THEME["panel"], border_width=1, border_color=THEME["border"], text_color=THEME["text"]).pack(pady=(0, 16))


if __name__ == "__main__":
    if show_splash:
        try:
            show_splash()
        except Exception:
            pass
    app = KeyMasterApp()
    app.mainloop()
