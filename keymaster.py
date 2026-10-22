"""
KeyMaster Pro - Python Mastery (UI + blanks/explanations)
"""
import customtkinter as ctk
import time
import math
from sound_engine import SoundEngine
from profile_manager import PlayerProfile
from content_generator import ContentGenerator
from tips_system import TipsSystem

try:
    from splash_screen import show_splash
except Exception:
    show_splash = None

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")


class KeyMasterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("KeyMaster Pro - Python Mastery")
        self.geometry("1000x700")
        self.player = PlayerProfile()
        self.content = ContentGenerator()
        self.audio = SoundEngine()
        self.tips = TipsSystem()
        self.mode = "TRAINING"
        self.current_learning_path = getattr(self.player, "current_learning_path", "basics")
        self.lives = 3
        self.survival_score = 0
        self.survival_difficulty = 1
        self.combo = 0
        self.combo_multiplier = 1.0
        self.current_challenge = None
        self.current_text = ""
        self.start_time = 0
        self.is_typing = False
        self.last_len = 0
        self.error_count = 0
        self._pending_explanation = ""
        self._build_ui()
        self._set_mode("TRAINING")

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=16, pady=8)
        self.lbl_level = ctk.CTkLabel(header, text="LVL 1", font=("Roboto", 22), text_color="#3B8ED0")
        self.lbl_level.pack(side="left")
        self.lbl_rank = ctk.CTkLabel(header, text="Novato", font=("Roboto", 12), text_color="gray")
        self.lbl_rank.pack(side="left", padx=12)
        self.mode_panel = ctk.CTkSegmentedButton(
            header,
            values=["ENTRENAMIENTO", "APRENDIZAJE", "SUPERVIVENCIA", "DIARIO"],
            command=self._on_mode,
            font=("Roboto", 11),
        )
        self.mode_panel.set("ENTRENAMIENTO")
        self.mode_panel.pack(side="top", pady=4)
        self.lbl_wpm = ctk.CTkLabel(header, text="WPM: 0", font=("Roboto", 14))
        self.lbl_wpm.pack(side="right")
        self.lbl_combo = ctk.CTkLabel(header, text="", font=("Roboto", 16), text_color="#FF6B6B")
        self.lbl_combo.pack(side="right", padx=8)

        self.area = ctk.CTkFrame(self, fg_color="transparent")
        self.area.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.lbl_diff = ctk.CTkLabel(self.area, text="", font=("Consolas", 12), text_color="#555")
        self.lbl_diff.pack(pady=(10, 4))
        self.lbl_concept = ctk.CTkLabel(self.area, text="", font=("Roboto", 11), text_color="#888")
        self.lbl_concept.pack()
        self.lbl_target = ctk.CTkLabel(self.area, text="...", font=("JetBrains Mono", 28), wraplength=900)
        self.lbl_target.pack(pady=16)
        self.lbl_hint = ctk.CTkLabel(self.area, text="", font=("Roboto", 12), text_color="#4ECDC4", wraplength=800)
        self.entry_var = ctk.StringVar()
        self.entry_var.trace_add("write", self._on_type)
        self.entry = ctk.CTkEntry(self.area, textvariable=self.entry_var, width=640, height=50,
                                  font=("JetBrains Mono", 22), justify="center")
        self.entry.pack(pady=12)
        self.lbl_feedback = ctk.CTkLabel(self.area, text="Escribe para empezar", font=("Roboto", 14))
        self.lbl_feedback.pack()
        pw = ctk.CTkFrame(self.area, fg_color="transparent")
        pw.pack(pady=8)
        self.btn_hint = ctk.CTkButton(pw, text="Pista", width=80, command=lambda: self._power("hint"))
        self.btn_hint.pack(side="left", padx=4)
        self.btn_skip = ctk.CTkButton(pw, text="Saltar", width=80, command=lambda: self._power("skip"))
        self.btn_skip.pack(side="left", padx=4)
        self.progress = ctk.CTkProgressBar(self, height=8)
        self.progress.grid(row=2, column=0, sticky="ew")
        self.entry.focus()

    def _on_mode(self, value):
        m = {"ENTRENAMIENTO": "TRAINING", "APRENDIZAJE": "LEARNING",
             "SUPERVIVENCIA": "SURVIVAL", "DIARIO": "DAILY"}
        self._set_mode(m.get(value, "TRAINING"))

    def _set_mode(self, mode):
        self.mode = mode
        self.combo = 0
        self.lives = 3
        if mode == "TRAINING":
            self.lbl_level.configure(text=f"LVL {self.player.level}")
            self.lbl_rank.configure(text=self.player.rank)
        elif mode == "SURVIVAL":
            self.lbl_level.configure(text=f"SCORE {self.survival_score}")
            self.lbl_rank.configure(text=f"Vidas: {self.lives}")
        self._new_challenge()

    def _new_challenge(self):
        if self.mode == "TRAINING":
            diff = min(10, max(1, self.player.level // 2 or 1))
            self.current_challenge = self.content.get_challenge(diff)
        elif self.mode == "LEARNING":
            diff = min(8, 2 + self.player.level // 3)
            self.current_challenge = self.content.get_challenge(
                diff, self.current_learning_path, prefer_blank=True)
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
            self.lbl_target.configure(text=display, text_color="#FFD700")
            self.lbl_feedback.configure(text="Completa el hueco ____", text_color="#FFB84D")
        else:
            self.lbl_target.configure(text=display, text_color="white")
            self.lbl_feedback.configure(text="Escribe el codigo", text_color="gray")
        self.lbl_diff.configure(text=f"Nivel {ch.difficulty} | {ch.category}")
        if self.mode == "LEARNING":
            self.lbl_concept.configure(text=f"Concepto: {ch.concept}")
        else:
            self.lbl_concept.configure(text="")
        self.lbl_hint.configure(text="")
        self.lbl_hint.pack_forget()
        self.entry_var.set("")
        self.entry.configure(border_color="#565b5e")

    def _on_type(self, *args):
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
                self.entry.configure(border_color="#2CC985")
            else:
                self.error_count += 1
                try:
                    self.audio.play_error()
                except Exception:
                    pass
                self.entry.configure(border_color="#C92C2C")
                if self.mode == "SURVIVAL":
                    self.lives -= 1
                    self.combo = 0
                    self.lbl_rank.configure(text=f"Vidas: {self.lives}")
                    if self.lives <= 0:
                        self.lbl_feedback.configure(text="Game Over", text_color="#C92C2C")
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
        if perfect:
            self.combo += 1
        else:
            self.combo = 0
        self.lbl_combo.configure(text=f"x{self.combo}" if self.combo > 1 else "")
        concept = self.current_challenge.concept if self.current_challenge else ""
        try:
            self.player.record_challenge_completion(wpm, self.error_count, len(self.current_text), concept, perfect)
        except Exception:
            pass
        exp = self.content.get_explanation(concept, self.current_challenge)
        self._pending_explanation = exp or ""
        if self.mode == "TRAINING":
            base = 10 + len(self.current_text)
            total = int(base * (1 + 0.1 * max(0, self.combo - 1)))
            leveled = self.player.add_xp(total)
            self.lbl_feedback.configure(text=f"+{total} XP", text_color="#2CC985")
            self.lbl_level.configure(text=f"LVL {self.player.level}")
            self.lbl_rank.configure(text=self.player.rank)
            if leveled:
                try:
                    self.audio.play_levelup()
                except Exception:
                    pass
            xp_need = max(1, self.player.xp_for_next_level)
            self.progress.set(min(1.0, self.player.xp / xp_need))
        elif self.mode == "LEARNING":
            base = 15 + len(self.current_text)
            if getattr(self.current_challenge, "challenge_type", "full") == "blank":
                base += 5
            self.player.add_xp(base)
            self.lbl_feedback.configure(text=f"+{base} XP (aprendizaje)", text_color="#4ECDC4")
        elif self.mode == "SURVIVAL":
            self.survival_score += 10 + self.survival_difficulty
            if self.combo and self.combo % 5 == 0:
                self.survival_difficulty = min(12, self.survival_difficulty + 1)
            self.lbl_level.configure(text=f"SCORE {self.survival_score}")
            self.lbl_feedback.configure(text="OK", text_color="#2CC985")
        else:
            self.lbl_feedback.configure(text="Desafio diario OK", text_color="#FFD700")
        if self._pending_explanation:
            self.lbl_hint.configure(text=f"\U0001f4d8 {self._pending_explanation}")
            self.lbl_hint.pack(before=self.entry, pady=(0, 8))
        self.after(1200, self._new_challenge)

    def _power(self, kind):
        try:
            ok = self.player.use_powerup(kind)
        except Exception:
            ok = False
        if not ok:
            self.lbl_feedback.configure(text="Sin power-up", text_color="#C92C2C")
            return
        try:
            self.audio.play_powerup()
        except Exception:
            pass
        if kind == "hint" and self.current_challenge:
            parts = [f"\U0001f4a1 {self.current_challenge.hint or 'Sigue el patron'}"]
            exp = self.content.get_explanation(self.current_challenge.concept, self.current_challenge)
            if exp:
                parts.append(f"\U0001f4d8 {exp}")
            self.lbl_hint.configure(text="\n".join(parts))
            self.lbl_hint.pack(before=self.entry, pady=(0, 8))
        elif kind == "skip":
            self.after(300, self._new_challenge)


if __name__ == "__main__":
    if show_splash:
        try:
            show_splash()
        except Exception:
            pass
    app = KeyMasterApp()
    app.mainloop()
