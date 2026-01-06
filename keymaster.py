"""
KeyMaster Pro - Advanced Python Typing Practice
Gamified application to memorize and mechanize Python code construction

Módulos:
- sound_engine.py: Gestión de efectos de sonido
- profile_manager.py: Sistema de perfil y progresión
- content_generator.py: Generación de desafíos de Python
- achievements.py: Sistema de logros
- tips_system.py: Sistema de notas educativas
- splash_screen.py: Pantalla de bienvenida con banner
"""
import customtkinter as ctk
import time
import math
from sound_engine import SoundEngine
from profile_manager import PlayerProfile
from content_generator import ContentGenerator
from achievements import Achievement
from tips_system import TipsSystem
from splash_screen import show_splash
from PIL import Image, ImageTk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class KeyMasterApp(ctk.CTk):
    """Main application class with enhanced gamification"""
    
    def __init__(self):
        super().__init__()
        self.title("KeyMaster Pro - Python Mastery")
        self.geometry("1100x750")
        
        # Initialize systems
        self.player = PlayerProfile()
        self.content = ContentGenerator()
        self.audio = SoundEngine()
        self.tips = TipsSystem()

        # Game state
        self.mode = "TRAINING"  # TRAINING | SURVIVAL | LEARNING | DAILY | CODE_BUILDER
        self.current_learning_path = self.player.current_learning_path
        self.current_code_category = "basic_functions"
        
        # Training state
        self.lives = 3
        self.survival_score = 0
        self.survival_difficulty = 1
        self.streak = 0
        self.combo = 0
        self.combo_multiplier = 1.0
        
        # Input tracking
        self.current_challenge = None
        self.current_text = ""
        self.start_time = 0
        self.is_typing = False
        self.last_len = 0
        self.error_count = 0
        
        # Power-ups state
        self.hint_active = False
        self.slow_time_active = False
        
        # UI References
        self.achievement_notification = None

        self._setup_ui()
        self._set_mode("TRAINING")

    def _setup_ui(self):
        """Setup the main user interface"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # === HEADER ===
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        # Left Panel - Player Info
        self.info_panel = ctk.CTkFrame(self.header, fg_color="transparent")
        self.info_panel.pack(side="left", anchor="w")
        
        self.lbl_main_stat = ctk.CTkLabel(
            self.info_panel, 
            text="LVL 1", 
            font=("Roboto Black", 28), 
            text_color="#3B8ED0"
        )
        self.lbl_main_stat.pack(anchor="w")
        
        self.lbl_sub_stat = ctk.CTkLabel(
            self.info_panel, 
            text="🐣 Novato", 
            font=("Roboto", 14), 
            text_color="gray"
        )
        self.lbl_sub_stat.pack(anchor="w")
        
        self.lbl_achievement_count = ctk.CTkLabel(
            self.info_panel,
            text="🏆 0/25",
            font=("Roboto", 12),
            text_color="#FFD700"
        )
        self.lbl_achievement_count.pack(anchor="w")

        # Center Panel - Mode Selector
        self.mode_panel = ctk.CTkSegmentedButton(
            self.header, 
            values=["ENTRENAMIENTO", "APRENDIZAJE", "CONSTRUCTOR", "SUPERVIVENCIA", "DIARIO"],
            command=self._on_mode_change,
            font=("Roboto", 11)
        )
        self.mode_panel.set("ENTRENAMIENTO")
        self.mode_panel.pack(side="top", pady=10)

        # Right Panel - Stats and Power-ups
        self.stats_panel = ctk.CTkFrame(self.header, fg_color="transparent")
        self.stats_panel.pack(side="right", anchor="e")
        
        # Combo indicator
        self.lbl_combo = ctk.CTkLabel(
            self.stats_panel,
            text="",
            font=("Roboto Black", 20),
            text_color="#FF6B6B"
        )
        self.lbl_combo.pack(anchor="e")
        
        self.lbl_lives = ctk.CTkLabel(
            self.stats_panel, 
            text="", 
            font=("Segoe UI Emoji", 24)
        )
        self.lbl_lives.pack(anchor="e")
        
        self.lbl_wpm = ctk.CTkLabel(
            self.stats_panel, 
            text="WPM: 0", 
            font=("Roboto Medium", 16)
        )
        self.lbl_wpm.pack(anchor="e")
        
        # Power-ups panel
        self.powerups_frame = ctk.CTkFrame(self.stats_panel, fg_color="transparent")
        self.powerups_frame.pack(anchor="e", pady=(5, 0))
        
        self.btn_hint = ctk.CTkButton(
            self.powerups_frame,
            text="💡 (3)",
            width=60,
            height=30,
            font=("Roboto", 11),
            command=lambda: self._use_powerup("hint"),
            fg_color="#4ECDC4",
            hover_color="#45B7AF"
        )
        self.btn_hint.pack(side="left", padx=2)
        
        self.btn_skip = ctk.CTkButton(
            self.powerups_frame,
            text="⏭️ (2)",
            width=60,
            height=30,
            font=("Roboto", 11),
            command=lambda: self._use_powerup("skip"),
            fg_color="#FFB84D",
            hover_color="#E6A844"
        )
        self.btn_skip.pack(side="left", padx=2)

        # === GAME AREA === (Scrollable for small screens)
        self.game_area_container = ctk.CTkScrollableFrame(
            self, 
            fg_color="transparent",
            scrollbar_button_color="#3B8ED0",
            scrollbar_button_hover_color="#2E7AB8"
        )
        self.game_area_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        
        self.game_area = ctk.CTkFrame(self.game_area_container, fg_color="transparent")
        self.game_area.pack(fill="both", expand=True, padx=30)

        # Learning path selector (hidden by default)
        self.learning_path_frame = ctk.CTkFrame(self.game_area, fg_color="#1a1a1a", corner_radius=10)
        
        self.lbl_path = ctk.CTkLabel(
            self.learning_path_frame,
            text="Ruta de Aprendizaje",
            font=("Roboto Bold", 14)
        )
        self.lbl_path.pack(pady=(10, 5))
        
        self.path_selector = ctk.CTkOptionMenu(
            self.learning_path_frame,
            values=self.content.get_available_paths(),
            command=self._on_path_change,
            font=("Roboto", 12)
        )
        self.path_selector.set(self.current_learning_path)
        self.path_selector.pack(pady=(0, 10), padx=10)
        
        # Code category selector (for code builder mode)
        self.code_category_frame = ctk.CTkFrame(self.game_area, fg_color="#1a1a1a", corner_radius=10)
        
        self.lbl_code_category = ctk.CTkLabel(
            self.code_category_frame,
            text="Categoría de Código",
            font=("Roboto Bold", 14)
        )
        self.lbl_code_category.pack(pady=(10, 5))
        
        self.category_selector = ctk.CTkOptionMenu(
            self.code_category_frame,
            values=self.content.get_code_builder_categories(),
            command=self._on_category_change,
            font=("Roboto", 12)
        )
        self.category_selector.set(self.current_code_category)
        self.category_selector.pack(pady=(0, 10), padx=10)

        # Challenge info
        self.lbl_diff = ctk.CTkLabel(
            self.game_area, 
            text="BÁSICO", 
            font=("Consolas Bold", 12), 
            text_color="#555"
        )
        self.lbl_diff.pack(pady=(20, 5))
        
        self.lbl_concept = ctk.CTkLabel(
            self.game_area,
            text="",
            font=("Roboto", 11),
            text_color="#888"
        )
        self.lbl_concept.pack()

        # Exercise description (for code builder)
        self.lbl_exercise_desc = ctk.CTkLabel(
            self.game_area,
            text="",
            font=("Roboto", 13),
            text_color="#888",
            wraplength=800
        )
        
        # Challenge text
        self.lbl_target = ctk.CTkLabel(
            self.game_area, 
            text="Cargando...", 
            font=("JetBrains Mono", 40),
            wraplength=900
        )
        self.lbl_target.pack(pady=20)

        # Hint label (hidden by default)
        self.lbl_hint = ctk.CTkLabel(
            self.game_area,
            text="",
            font=("Roboto Italic", 12),
            text_color="#4ECDC4"
        )
        
        # Educational tip (for code builder mode)
        self.lbl_tip = ctk.CTkLabel(
            self.game_area,
            text="",
            font=("Roboto Italic", 12),
            text_color="#FFD700",
            wraplength=800
        )

        # Input entry (single line)
        self.entry_var = ctk.StringVar()
        self.entry_var.trace_add("write", self._check_input)
        self.entry = ctk.CTkEntry(
            self.game_area, 
            textvariable=self.entry_var,
            width=700, 
            height=60,
            font=("JetBrains Mono", 28), 
            justify="center",
            corner_radius=15, 
            border_width=3
        )
        self.entry.pack(pady=20)
        
        # Multi-line input (for code builder mode)
        self.code_textbox = ctk.CTkTextbox(
            self.game_area,
            width=750,
            height=250,
            font=("JetBrains Mono", 15),
            corner_radius=15,
            border_width=3,
            wrap="none"
        )
        # Bind Ctrl+Enter to verify code
        self.code_textbox.bind("<Control-Return>", lambda e: self._verify_code())

        # Feedback
        self.lbl_feedback = ctk.CTkLabel(
            self.game_area, 
            text="Escribe para empezar", 
            font=("Roboto", 16)
        )
        self.lbl_feedback.pack()
        
        # Verify button (for code builder mode) - más compacto
        self.btn_verify = ctk.CTkButton(
            self.game_area,
            text="✓ Verificar Código (Ctrl+Enter)",
            command=self._verify_code,
            fg_color="#2CC985",
            hover_color="#25A870",
            font=("Roboto Bold", 14),
            height=45,
            width=280
        )
        
        # Action buttons
        self.btn_restart = ctk.CTkButton(
            self.game_area, 
            text="🔄 Reintentar", 
            command=self._reset_survival,
            fg_color="#C92C2C", 
            hover_color="#8a1c1c",
            font=("Roboto", 14),
            height=40
        )
        
        self.btn_stats = ctk.CTkButton(
            self.game_area,
            text="📊 Ver Estadísticas",
            command=self._show_stats,
            fg_color="#3B8ED0",
            hover_color="#2E7AB8",
            font=("Roboto", 14),
            height=40
        )
        self.btn_stats.pack(pady=10)
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self, height=10)
        self.progress_bar.grid(row=2, column=0, sticky="ew", padx=0, pady=0)
        
        # Achievement notification (initially hidden)
        self._setup_achievement_popup()

    def _setup_achievement_popup(self):
        """Setup achievement notification popup"""
        self.achievement_popup = ctk.CTkFrame(
            self,
            fg_color="#1a1a1a",
            corner_radius=15,
            border_width=2,
            border_color="#FFD700"
        )
        
        self.ach_icon = ctk.CTkLabel(
            self.achievement_popup,
            text="🏆",
            font=("Segoe UI Emoji", 40)
        )
        self.ach_icon.pack(pady=(15, 5))
        
        self.ach_title = ctk.CTkLabel(
            self.achievement_popup,
            text="¡LOGRO DESBLOQUEADO!",
            font=("Roboto Black", 16),
            text_color="#FFD700"
        )
        self.ach_title.pack()
        
        self.ach_name = ctk.CTkLabel(
            self.achievement_popup,
            text="",
            font=("Roboto Bold", 14),
            text_color="white"
        )
        self.ach_name.pack(pady=(5, 0))
        
        self.ach_desc = ctk.CTkLabel(
            self.achievement_popup,
            text="",
            font=("Roboto", 11),
            text_color="#888"
        )
        self.ach_desc.pack(pady=(0, 15), padx=20)

    def _on_mode_change(self, value):
        """Handle mode selection change"""
        mode_map = {
            "ENTRENAMIENTO": "TRAINING",
            "APRENDIZAJE": "LEARNING",
            "CONSTRUCTOR": "CODE_BUILDER",
            "SUPERVIVENCIA": "SURVIVAL",
            "DIARIO": "DAILY"
        }
        self._set_mode(mode_map.get(value, "TRAINING"))
    
    def _on_path_change(self, path: str):
        """Handle learning path change"""
        self.current_learning_path = path
        self.player.current_learning_path = path
        self.player.save_profile()
        self._new_challenge()
    
    def _on_category_change(self, category: str):
        """Handle code category change"""
        self.current_code_category = category
        self._new_code_builder_exercise()

    def _set_mode(self, mode: str):
        """Set game mode and update UI accordingly"""
        self.mode = mode
        self.btn_restart.pack_forget()
        self.entry.configure(state="normal")
        self.entry.focus()
        self.combo = 0
        self._update_combo_display()
        
        # Hide selectors by default
        self.learning_path_frame.pack_forget()
        self.code_category_frame.pack_forget()
        self.lbl_exercise_desc.pack_forget()
        self.lbl_tip.pack_forget()
        
        # Hide code textbox and verify button by default
        self.code_textbox.pack_forget()
        self.btn_verify.pack_forget()
        
        # Show entry by default
        self.entry.pack(pady=20)
        
        if mode == "TRAINING":
            self.lbl_main_stat.configure(
                text=f"LVL {self.player.level}", 
                text_color="#3B8ED0"
            )
            self.lbl_sub_stat.configure(text=self.player.rank)
            self.lbl_lives.configure(text="")
            
            xp_progress = self.player.xp / self.player.xp_for_next_level
            self.progress_bar.set(xp_progress)
            self.progress_bar.configure(progress_color="#3B8ED0")
            
            self._update_achievement_count()
            self._new_challenge()
            
        elif mode == "LEARNING":
            self.learning_path_frame.pack(pady=(10, 20))
            
            path_name = self.content.get_path_name(self.current_learning_path)
            completed, total = self.content.get_path_progress(
                self.current_learning_path,
                self.player.completed_concepts
            )
            
            self.lbl_main_stat.configure(
                text=f"📚 {path_name}",
                text_color="#4ECDC4"
            )
            self.lbl_sub_stat.configure(
                text=f"Progreso: {completed}/{total} conceptos"
            )
            self.lbl_lives.configure(text="")
            
            progress = completed / total if total > 0 else 0
            self.progress_bar.set(progress)
            self.progress_bar.configure(progress_color="#4ECDC4")
            
            self._new_challenge()
            
        elif mode == "SURVIVAL":
            self._reset_survival()
            
        elif mode == "DAILY":
            self._start_daily_challenges()
            
        elif mode == "CODE_BUILDER":
            self._start_code_builder()
    
    def _start_code_builder(self):
        """Start code builder mode"""
        self.code_category_frame.pack(pady=(10, 20))
        
        # Hide single line entry
        self.entry.pack_forget()
        
        # Show multi-line textbox and verify button
        self.code_textbox.pack(pady=20)
        self.btn_verify.pack(pady=15)
        
        category_name = self.content.get_category_name(self.current_code_category)
        self.lbl_main_stat.configure(
            text=f"🔧 {category_name}",
            text_color="#9B59B6"
        )
        self.lbl_sub_stat.configure(
            text="Escribe el código completo"
        )
        self.lbl_lives.configure(text="")
        self.progress_bar.set(0)
        self.progress_bar.configure(progress_color="#9B59B6")
        
        self._new_code_builder_exercise()
    
    def _start_daily_challenges(self):
        """Start daily challenge mode"""
        self.lbl_main_stat.configure(
            text="🌟 DESAFÍO DIARIO",
            text_color="#FFD700"
        )
        self.lbl_sub_stat.configure(
            text=f"Racha: {self.player.daily_streak} días 🔥"
        )
        self.lbl_lives.configure(text="")
        self.progress_bar.set(0)
        self.progress_bar.configure(progress_color="#FFD700")
        
        # Show daily challenges
        dailies = self.content.get_daily_challenges()
        if dailies:
            self.current_challenge = dailies[0]
            self._display_challenge()

    def _reset_survival(self):
        """Reset survival mode"""
        self.lives = 3
        self.survival_score = 0
        self.survival_difficulty = 1
        self.streak = 0
        self.combo = 0
        self.btn_restart.pack_forget()
        self.entry.configure(state="normal")
        
        self.lbl_main_stat.configure(
            text="⚔️ SCORE: 0", 
            text_color="#E04F5F"
        )
        self.lbl_sub_stat.configure(
            text=f"Récord: {self.player.best_survival_score}"
        )
        self.progress_bar.configure(progress_color="#E04F5F")
        self._update_lives_ui()
        self._update_combo_display()
        self._new_challenge()

    def _update_lives_ui(self):
        """Update lives display"""
        hearts = "❤️ " * self.lives + "🖤 " * (3 - self.lives)
        self.lbl_lives.configure(text=hearts.strip())
    
    def _update_combo_display(self):
        """Update combo multiplier display"""
        if self.combo >= 5:
            self.lbl_combo.configure(text=f"🔥 COMBO x{self.combo}")
            self.combo_multiplier = 1.0 + (self.combo * 0.1)
        else:
            self.lbl_combo.configure(text="")
            self.combo_multiplier = 1.0
    
    def _update_achievement_count(self):
        """Update achievement counter"""
        unlocked = self.player.achievement_manager.get_unlocked_count()
        total = self.player.achievement_manager.get_total_count()
        self.lbl_achievement_count.configure(text=f"🏆 {unlocked}/{total}")
    
    def _update_powerup_buttons(self):
        """Update power-up button displays"""
        hint_count = self.player.powerups.get("hint", 0)
        skip_count = self.player.powerups.get("skip", 0)
        
        self.btn_hint.configure(text=f"💡 ({hint_count})")
        self.btn_skip.configure(text=f"⏭️ ({skip_count})")
        
        # Disable if no uses left
        self.btn_hint.configure(state="normal" if hint_count > 0 else "disabled")
        self.btn_skip.configure(state="normal" if skip_count > 0 else "disabled")

    def _new_challenge(self):
        """Generate and display a new challenge"""
        # Determine difficulty
        diff = 1
        if self.mode == "TRAINING":
            diff = min(10, math.ceil(self.player.level / 2))
        elif self.mode == "LEARNING":
            diff = min(8, 2 + (self.player.level // 3))
        elif self.mode == "SURVIVAL":
            diff = self.survival_difficulty
        elif self.mode == "DAILY":
            return  # Daily challenges are set separately

        # Get challenge from content generator
        if self.mode == "LEARNING":
            self.current_challenge = self.content.get_challenge(
                diff, 
                self.current_learning_path
            )
        else:
            self.current_challenge = self.content.get_challenge(diff)
        
        self._display_challenge()
    
    def _display_challenge(self):
        """Display the current challenge"""
        if not self.current_challenge:
            return
        
        self.current_text = self.current_challenge.text
        self.error_count = 0
        self.hint_active = False
        self.lbl_hint.pack_forget()
        
        # Update challenge text
        self.lbl_target.configure(text=self.current_text, text_color="white")
        
        # Update difficulty indicator
        diff = self.current_challenge.difficulty
        diff_names = ["BÁSICO", "CÓDIGO", "PRO", "HACKER", "DIOS"]
        diff_idx = min(4, (diff-1)//2)
        self.lbl_diff.configure(
            text=f"/// NIVEL {diff}: {diff_names[diff_idx]} ///"
        )
        
        # Show concept if in learning mode
        if self.mode == "LEARNING":
            concept_display = f"Concepto: {self.current_challenge.concept}"
            self.lbl_concept.configure(text=concept_display)
            self.lbl_concept.pack()
        else:
            self.lbl_concept.pack_forget()
        
        # Reset input
        self.entry_var.set("")
        self.entry.configure(border_color="#565b5e")
        self.start_time = 0
        self.is_typing = False
        self.last_len = 0
        self.lbl_feedback.configure(text="¡Escribe!", text_color="gray")
        
        self._update_powerup_buttons()

    def _check_input(self, *args):
        """Check input as user types"""
        user_input = self.entry_var.get()
        target = self.current_text
        
        # Audio feedback
        if len(user_input) > self.last_len:
            if target.startswith(user_input):
                self.audio.play_click()
            else:
                self.audio.play_error()
                self.error_count += 1
        
        self.last_len = len(user_input)

        # Start timer on first keystroke
        if user_input and not self.is_typing:
            self.start_time = time.time()
            self.is_typing = True

        # Validation
        if target.startswith(user_input):
            self.entry.configure(border_color="#2CC985")
            
            # Show progress
            progress = len(user_input) / len(target)
            progress_text = "." * int(progress * 20)
            self.lbl_feedback.configure(
                text=progress_text, 
                text_color="#2CC985"
            )
            
            # Complete challenge
            if user_input == target:
                self._on_success()
        else:
            self.entry.configure(border_color="#C92C2C")
            self.lbl_feedback.configure(text="¡Error!", text_color="#C92C2C")
            
            # Survival mode penalty
            if self.mode == "SURVIVAL" and len(user_input) > len(target):
                self._trigger_fail()

    def _on_success(self):
        """Handle successful challenge completion"""
        # Calculate performance stats
        duration = time.time() - self.start_time
        word_count = len(self.current_text.split())
        wpm = int((word_count / duration) * 60) if duration > 0 else 0
        
        perfect = (self.error_count == 0)
        keystrokes = len(self.current_text)
        
        self.lbl_wpm.configure(text=f"⚡ {wpm} WPM")
        
        # Update combo
        if perfect:
            self.combo += 1
            self._update_combo_display()
            if self.combo >= 5 and self.combo % 5 == 0:
                self.audio.play_combo()
        else:
            self.combo = 0
            self._update_combo_display()
        
        # Record statistics
        concept = self.current_challenge.concept if self.current_challenge else ""
        self.player.record_challenge_completion(
            wpm, 
            self.error_count, 
            keystrokes,
            concept, 
            perfect
        )
        
        # Mode-specific rewards
        if self.mode == "TRAINING":
            # Calculate XP with combo multiplier
            base_xp = 10 + len(self.current_text)
            bonus_xp = int(base_xp * (self.combo_multiplier - 1.0))
            total_xp = base_xp + bonus_xp
            
            lvl_up = self.player.add_xp(total_xp)
            
            if bonus_xp > 0:
                self.lbl_feedback.configure(
                    text=f"+{total_xp} XP (Combo x{self.combo_multiplier:.1f})",
                    text_color="#FFD700"
                )
            else:
                self.lbl_feedback.configure(
                    text=f"+{total_xp} XP",
                    text_color="#2CC985"
                )
            
            if lvl_up:
                self.audio.play_levelup()
                self.lbl_main_stat.configure(text=f"LVL {self.player.level}")
                self.lbl_sub_stat.configure(text=self.player.rank)
                
                # Award power-ups on level up
                if self.player.level % 5 == 0:
                    self.player.earn_powerup("hint", 1)
                    self.player.earn_powerup("skip", 1)
            
            xp_progress = self.player.xp / self.player.xp_for_next_level
            self.progress_bar.set(xp_progress)
            
            # Check for achievements
            self._check_achievements()
            
            self.after(800, self._new_challenge)
            
        elif self.mode == "LEARNING":
            # Track concept mastery
            base_xp = 15 + len(self.current_text)
            self.player.add_xp(base_xp)
            
            path_name = self.content.get_path_name(self.current_learning_path)
            completed, total = self.content.get_path_progress(
                self.current_learning_path,
                self.player.completed_concepts
            )
            
            self.lbl_sub_stat.configure(
                text=f"Progreso: {completed}/{total} conceptos"
            )
            
            progress = completed / total if total > 0 else 0
            self.progress_bar.set(progress)
            
            # Check if path is mastered
            if completed == total and self.current_learning_path not in self.player.mastered_paths:
                self.player.mastered_paths.add(self.current_learning_path)
                self.player.save_profile()
                self.lbl_feedback.configure(
                    text=f"🎉 ¡{path_name} DOMINADO!",
                    text_color="#FFD700"
                )
                self.audio.play_achievement()
            else:
                self.lbl_feedback.configure(
                    text=f"✓ Concepto aprendido",
                    text_color="#4ECDC4"
                )
            
            self.after(1000, self._new_challenge)
            
        elif self.mode == "SURVIVAL":
            # Score with combo multiplier
            base_score = 10 + int(self.survival_difficulty * 1.5)
            combo_bonus = int(base_score * (self.combo_multiplier - 1.0))
            total_score = base_score + combo_bonus
            
            self.survival_score += total_score
            self.streak += 1
            
            # Track combo
            self.player.update_combo(self.combo)
            
            # Increase difficulty
            if self.streak % 5 == 0:
                self.survival_difficulty = min(12, self.survival_difficulty + 1)
                self.lbl_feedback.configure(
                    text="⚠️ DIFICULTAD AUMENTADA",
                    text_color="#FF6B6B"
                )
                self.audio.play_levelup()
            else:
                feedback = f"Perfecto! +{total_score}"
                if combo_bonus > 0:
                    feedback += f" (Combo +{combo_bonus})"
                self.lbl_feedback.configure(text=feedback, text_color="#2CC985")

            self.lbl_main_stat.configure(text=f"⚔️ SCORE: {self.survival_score}")
            
            # Recover life on streak milestone
            if self.streak % 20 == 0 and self.lives < 3:
                self.lives += 1
                self._update_lives_ui()
                self.lbl_feedback.configure(
                    text="❤️ VIDA RECUPERADA",
                    text_color="#2CC985"
                )

            self.after(600, self._new_challenge)
            
        elif self.mode == "DAILY":
            # Mark daily challenge complete
            self.player.complete_daily_challenge(0)
            self.lbl_feedback.configure(
                text=f"✓ Desafío completado! +50 XP Bonus",
                text_color="#FFD700"
            )
            self.audio.play_achievement()
            
            # Update streak display
            self.lbl_sub_stat.configure(
                text=f"Racha: {self.player.daily_streak} días 🔥"
            )

    def _trigger_fail(self):
        """Handle failure in survival mode"""
        if self.mode != "SURVIVAL":
            return
        
        self.lives -= 1
        self.combo = 0
        self._update_lives_ui()
        self._update_combo_display()
        self.audio.play_error()
        
        # Damage flash animation
        self.game_area.configure(fg_color="#4a1818")
        self.after(100, lambda: self.game_area.configure(fg_color="transparent"))

        if self.lives <= 0:
            self._game_over()
        else:
            self.entry_var.set("")
            self.lbl_feedback.configure(
                text="💔 Vida perdida",
                text_color="#C92C2C"
            )

    def _use_powerup(self, powerup_type: str):
        """Use a power-up"""
        if not self.player.use_powerup(powerup_type):
            self.lbl_feedback.configure(
                text="❌ No tienes ese power-up",
                text_color="#C92C2C"
            )
            return
        
        self.audio.play_powerup()
        self._update_powerup_buttons()
        
        if powerup_type == "hint":
            # Show hint
            self.hint_active = True
            if self.current_challenge and self.current_challenge.hint:
                self.lbl_hint.configure(text=f"💡 Pista: {self.current_challenge.hint}")
                self.lbl_hint.pack(before=self.entry, pady=(0, 10))
            else:
                self.lbl_hint.configure(text="💡 ¡Sigue el patrón!")
                self.lbl_hint.pack(before=self.entry, pady=(0, 10))
        
        elif powerup_type == "skip":
            # Skip challenge without penalty
            self.lbl_feedback.configure(
                text="⏭️ Desafío saltado",
                text_color="#FFB84D"
            )
            self.after(500, self._new_challenge)
    
    def _new_code_builder_exercise(self):
        """Generate a new code builder exercise"""
        diff = min(8, 2 + (self.player.level // 3))
        
        exercise = self.content.get_code_builder_exercise(
            difficulty=diff,
            category=self.current_code_category
        )
        
        if not exercise:
            return
        
        self.current_challenge = type('obj', (object,), {
            'text': exercise['code'],
            'difficulty': exercise['difficulty'],
            'concept': exercise['concept'],
            'title': exercise['title'],
            'description': exercise['description']
        })()
        
        # Display exercise
        self.lbl_diff.configure(
            text=f"/// EJERCICIO: {exercise['title']} ///"
        )
        self.lbl_diff.pack(pady=(20, 5))
        
        self.lbl_exercise_desc.configure(text=exercise['description'])
        self.lbl_exercise_desc.pack(pady=(0, 10))
        
        self.lbl_target.configure(
            text=exercise['code'],
            text_color="#888",
            font=("JetBrains Mono", 18),
            anchor="w",
            justify="left"
        )
        
        # Show educational tip
        tip = self.tips.get_tip_for_concept(exercise['concept'])
        self.lbl_tip.configure(text=tip)
        self.lbl_tip.pack(pady=(10, 0))
        
        # Clear textbox
        self.code_textbox.delete("1.0", "end")
        self.code_textbox.focus()
        
        self.lbl_feedback.configure(
            text="Escribe el código completo y presiona 'Verificar' o Ctrl+Enter",
            text_color="gray"
        )
        
        self._update_powerup_buttons()
    
    def _verify_code(self):
        """Verify the code written in code builder mode"""
        if self.mode != "CODE_BUILDER":
            return
        
        user_code = self.code_textbox.get("1.0", "end-1c")
        target_code = self.current_challenge.text
        
        # Normalize whitespace for comparison
        user_lines = [line.rstrip() for line in user_code.split('\n') if line.strip()]
        target_lines = [line.rstrip() for line in target_code.split('\n') if line.strip()]
        
        # Check if code matches
        if user_lines == target_lines:
            self._on_code_builder_success()
        else:
            self._on_code_builder_error(user_lines, target_lines)
    
    def _on_code_builder_success(self):
        """Handle successful code completion"""
        self.audio.play_levelup()
        
        # Flash green
        self.code_textbox.configure(border_color="#2CC985")
        
        self.lbl_feedback.configure(
            text="✓ ¡Código correcto! Excelente trabajo",
            text_color="#2CC985"
        )
        
        # Award XP
        base_xp = 30 + (self.current_challenge.difficulty * 10)
        self.player.add_xp(base_xp)
        
        # Record completion
        concept = self.current_challenge.concept
        lines = len(self.current_challenge.text.split('\n'))
        self.player.record_challenge_completion(
            wpm=0,  # WPM doesn't apply to code builder
            errors=0,
            keystrokes=len(self.current_challenge.text),
            concept=concept,
            perfect=True
        )
        
        # Check achievements
        self._check_achievements()
        
        # Wait and load next exercise
        self.after(2000, self._new_code_builder_exercise)
    
    def _on_code_builder_error(self, user_lines, target_lines):
        """Handle code error"""
        self.audio.play_error()
        
        # Flash red
        self.code_textbox.configure(border_color="#C92C2C")
        self.after(500, lambda: self.code_textbox.configure(border_color="#565b5e"))
        
        # Find first difference
        for i, (user_line, target_line) in enumerate(zip(user_lines, target_lines)):
            if user_line != target_line:
                self.lbl_feedback.configure(
                    text=f"❌ Error en línea {i+1}. Revisa tu código",
                    text_color="#C92C2C"
                )
                return
        
        # Different number of lines
        if len(user_lines) != len(target_lines):
            self.lbl_feedback.configure(
                text=f"❌ Número de líneas incorrecto: {len(user_lines)} vs {len(target_lines)} esperadas",
                text_color="#C92C2C"
            )
        else:
            self.lbl_feedback.configure(
                text="❌ Hay diferencias en el código. Revisa cuidadosamente",
                text_color="#C92C2C"
            )
    
    def _manual_skip_check(self, event):
        """Handle Enter/Escape key press"""
        # Don't skip on Enter in code builder mode
        if self.mode == "CODE_BUILDER":
            return
        
        if self.mode == "SURVIVAL":
            # In survival, skip costs a life
            if self.entry_var.get() != self.current_text:
                self._trigger_fail()
        else:
            # In training/learning, skip is free
            self._new_challenge()
    
    def _check_achievements(self):
        """Check for newly unlocked achievements"""
        newly_unlocked = self.player.check_achievements()
        
        for achievement in newly_unlocked:
            self._show_achievement_popup(achievement)
        
        if newly_unlocked:
            self._update_achievement_count()
    
    def _show_achievement_popup(self, achievement: Achievement):
        """Display achievement unlock animation"""
        self.audio.play_achievement()
        
        # Update popup content
        self.ach_icon.configure(text=achievement.icon)
        self.ach_name.configure(text=achievement.name)
        self.ach_desc.configure(text=achievement.description)
        
        # Position popup
        popup_width = 350
        popup_height = 180
        x = (self.winfo_width() - popup_width) // 2
        y = 100
        
        self.achievement_popup.place(
            x=x, 
            y=y,
            width=popup_width,
            height=popup_height
        )
        
        # Auto-hide after 3 seconds
        self.after(3000, lambda: self.achievement_popup.place_forget())
    
    def _show_stats(self):
        """Show statistics window"""
        stats_window = ctk.CTkToplevel(self)
        stats_window.title("📊 Estadísticas")
        stats_window.geometry("600x700")
        stats_window.transient(self)
        
        # Header
        header = ctk.CTkLabel(
            stats_window,
            text="📊 TUS ESTADÍSTICAS",
            font=("Roboto Black", 24),
            text_color="#3B8ED0"
        )
        header.pack(pady=20)
        
        # Stats frame
        stats_frame = ctk.CTkScrollableFrame(
            stats_window,
            width=550,
            height=550
        )
        stats_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Display stats
        stats = self.player.get_stats_summary()
        for key, value in stats.items():
            stat_row = ctk.CTkFrame(stats_frame, fg_color="#2b2b2b")
            stat_row.pack(fill="x", pady=5, padx=10)
            
            lbl_key = ctk.CTkLabel(
                stat_row,
                text=key,
                font=("Roboto", 14),
                anchor="w"
            )
            lbl_key.pack(side="left", padx=20, pady=10)
            
            lbl_value = ctk.CTkLabel(
                stat_row,
                text=str(value),
                font=("Roboto Bold", 14),
                text_color="#3B8ED0",
                anchor="e"
            )
            lbl_value.pack(side="right", padx=20, pady=10)
        
        # Achievements section
        ach_header = ctk.CTkLabel(
            stats_frame,
            text="\n🏆 LOGROS DESBLOQUEADOS",
            font=("Roboto Bold", 16)
        )
        ach_header.pack(pady=(20, 10))
        
        # Display achievements by category
        categories = ["speed", "level", "accuracy", "survival", "combo"]
        for category in categories:
            achievements = self.player.achievement_manager.get_achievements_by_category(category)
            unlocked = [a for a in achievements if a.unlocked]
            
            if unlocked:
                cat_label = ctk.CTkLabel(
                    stats_frame,
                    text=f"\n{category.title()}",
                    font=("Roboto Bold", 12),
                    text_color="gray"
                )
                cat_label.pack(anchor="w", padx=20)
                
                for ach in unlocked:
                    ach_row = ctk.CTkFrame(stats_frame, fg_color="#1a1a1a")
                    ach_row.pack(fill="x", pady=3, padx=20)
                    
                    ach_label = ctk.CTkLabel(
                        ach_row,
                        text=f"{ach.icon} {ach.name}",
                        font=("Roboto", 12),
                        anchor="w"
                    )
                    ach_label.pack(side="left", padx=10, pady=5)
        
        # Close button
        btn_close = ctk.CTkButton(
            stats_window,
            text="Cerrar",
            command=stats_window.destroy,
            width=200,
            height=40
        )
        btn_close.pack(pady=20)

    def _game_over(self):
        """Handle game over in survival mode"""
        self.audio.play_gameover()
        
        self.lbl_target.configure(text="☠️ GAME OVER", text_color="#FF0000")
        self.lbl_feedback.configure(
            text=f"Score Final: {self.survival_score}",
            text_color="white"
        )
        self.entry.configure(state="disabled")
        
        # Update survival statistics
        is_record = self.player.update_survival_score(
            self.survival_score,
            self.combo
        )
        
        if is_record:
            self.lbl_sub_stat.configure(
                text="🏆 ¡NUEVO RÉCORD!",
                text_color="#FFD700"
            )
            self.audio.play_achievement()
        
        # Check for achievements
        self._check_achievements()
        
        self.btn_restart.pack(pady=10)

def main():
    """Main entry point"""
    # Create main app (but don't show it yet)
    app = KeyMasterApp()
    app.withdraw()  # Hide main window initially
    
    # Show splash screen
    splash = show_splash(app, duration=2500)
    
    # Wait for splash to close, then show main window
    def show_main_window():
        app.deiconify()  # Show main window
        app.focus_force()  # Bring to front
    
    app.after(2600, show_main_window)
    
    # Keyboard bindings
    app.bind("<Return>", lambda e: app._manual_skip_check(e))
    app.bind("<Escape>", lambda e: app._manual_skip_check(e))
    
    # Start the application
    app.mainloop()


if __name__ == "__main__":
    main()