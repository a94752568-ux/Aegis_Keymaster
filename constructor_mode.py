"""Constructor mode helpers for KeyMaster Pro."""
import ast


class ConstructorMixin:
    """Mixin with Code Builder (Constructor) mode methods."""

    def _start_code_builder(self):
        self.cat_frame.pack(pady=(4, 8))
        self.path_frame.pack_forget()
        self.lbl_target.pack_forget()
        self.entry.pack_forget()
        self.lbl_desc.pack(pady=(4, 4))
        self.lbl_tip.pack(pady=(0, 6))
        self.code_textbox.pack(pady=12)
        self.btn_verify.pack(pady=6)
        self.builder_btns.pack(pady=4)
        self.lbl_level.configure(text=f"LVL {self.player.level}")
        self.lbl_rank.configure(text="Constructor")
        self._new_code_builder_exercise()

    def _new_code_builder_exercise(self):
        diff = min(8, 2 + self.player.level // 3)
        exercise = self.content.get_code_builder_exercise(
            difficulty=diff, category=self.current_code_category
        )
        if not exercise:
            self.lbl_feedback.configure(text="Sin ejercicios en esta categoria", text_color="#C92C2C")
            return

        self._builder_exercise = exercise
        self._builder_revealed = 0
        self._builder_used_scaffold = False
        self._builder_used_reveal = False
        self._builder_used_solution = False

        self.current_challenge = type("obj", (object,), {
            "text": exercise["code"],
            "difficulty": exercise["difficulty"],
            "concept": exercise.get("concept", ""),
            "title": exercise.get("title", ""),
            "description": exercise.get("description", ""),
            "hint": exercise.get("description", "Escribe el bloque completo"),
            "challenge_type": "full",
            "prompt": "",
            "explanation": "",
            "scaffold": exercise.get("scaffold", ""),
            "goals": exercise.get("goals", []),
        })()

        cat_name = self.content.get_category_name(self.current_code_category)
        self.lbl_diff.configure(
            text=f"Nivel {exercise['difficulty']} | {cat_name}"
        )
        self.lbl_concept.configure(text=exercise.get("title", ""))
        desc = exercise.get("description", "")
        goals = exercise.get("goals") or []
        if goals:
            desc = desc + "\nObjetivos: " + " · ".join(goals)
        self.lbl_desc.configure(text=desc)
        self.lbl_desc.pack(pady=(4, 4))

        self.lbl_target.pack_forget()
        tip = ""
        try:
            tip = self.tips.get_tip_for_concept(exercise.get("concept", ""))
        except Exception:
            tip = self.content.get_explanation(exercise.get("concept", ""))
        structure = ""
        try:
            structure = self.content.get_code_builder_structure_hint(exercise)
        except Exception:
            structure = ""
        if structure:
            tip = (tip + "\n" if tip else "") + "📐 " + structure
        if tip:
            self.lbl_tip.configure(text=tip)
            self.lbl_tip.pack(pady=(0, 6))
        else:
            self.lbl_tip.pack_forget()

        self.code_textbox.delete("1.0", "end")
        self.code_textbox.configure(border_color="#565b5e")
        n_lines = len(exercise["code"].split("\n"))
        self.lbl_feedback.configure(
            text=f"Escribe el codigo ({n_lines} lineas). Scaffold / Revelar / Ver solucion / Tutor IA si necesitas ayuda. Ctrl+Enter verifica.",
            text_color="gray",
        )
        self.lbl_hint.pack_forget()
        self.code_textbox.focus()

    def _load_scaffold(self):
        if self.mode != "CODE_BUILDER" or not getattr(self, "_builder_exercise", None):
            return
        scaffold = self._builder_exercise.get("scaffold") or ""
        if not scaffold.strip():
            self.lbl_feedback.configure(text="Este ejercicio no tiene scaffold", text_color="#FFB84D")
            return
        self._builder_used_scaffold = True
        self.code_textbox.delete("1.0", "end")
        self.code_textbox.insert("1.0", scaffold)
        self.code_textbox.configure(border_color="#3B8ED0")
        self.lbl_feedback.configure(
            text="Scaffold cargado. Completa los pass / comentarios.",
            text_color="#3B8ED0",
        )
        self.code_textbox.focus()

    def _reveal_line(self):
        if self.mode != "CODE_BUILDER" or not getattr(self, "_builder_exercise", None):
            return
        target_lines = self._builder_exercise["code"].split("\n")
        if self._builder_revealed >= len(target_lines):
            self.lbl_feedback.configure(text="Ya se revelaron todas las lineas", text_color="#FFB84D")
            return
        self._builder_used_reveal = True
        revealed = target_lines[: self._builder_revealed + 1]
        self._builder_revealed += 1
        partial = "\n".join(revealed)
        self.code_textbox.delete("1.0", "end")
        self.code_textbox.insert("1.0", partial)
        self.code_textbox.configure(border_color="#8B5CF6")
        left = len(target_lines) - self._builder_revealed
        self.lbl_feedback.configure(
            text=f"Linea {self._builder_revealed}/{len(target_lines)} revelada. Quedan {left}.",
            text_color="#8B5CF6",
        )
        self.code_textbox.focus()

    def _show_solution(self):
        """Show the full correct code in the editor (study mode)."""
        if self.mode != "CODE_BUILDER" or not getattr(self, "_builder_exercise", None):
            return
        code = self._builder_exercise.get("code") or ""
        if not code.strip():
            self.lbl_feedback.configure(text="No hay solucion disponible", text_color="#C92C2C")
            return
        self._builder_used_solution = True
        self._builder_used_reveal = True
        self._builder_revealed = len(code.split("\n"))
        self.code_textbox.delete("1.0", "end")
        self.code_textbox.insert("1.0", code)
        self.code_textbox.configure(border_color="#E85D4C")
        goals = self._builder_exercise.get("goals") or []
        note = "Solucion completa. Estudiá y escribe de nuevo (Siguiente) para practicar."
        if goals:
            note += " Objetivos: " + " · ".join(goals)
        self.lbl_feedback.configure(text=note, text_color="#E85D4C")
        try:
            self.audio.play_powerup()
        except Exception:
            pass
        self.code_textbox.focus()

    def _normalize_code(self, s: str) -> str:
        lines = [ln.rstrip() for ln in s.replace("\r\n", "\n").replace("\t", "    ").split("\n")]
        while lines and lines[-1] == "":
            lines.pop()
        return "\n".join(lines)

    def _codes_equivalent(self, user: str, target: str) -> bool:
        return self._normalize_code(user) == self._normalize_code(target)

    def _verify_code(self):
        if self.mode != "CODE_BUILDER" or not self.current_challenge:
            return
        user_code = self.code_textbox.get("1.0", "end-1c")
        target_code = self.current_challenge.text

        try:
            ast.parse(user_code)
        except SyntaxError as e:
            self.code_textbox.configure(border_color="#C92C2C")
            msg = f"Error de sintaxis (linea {e.lineno}): {e.msg}"
            self.lbl_feedback.configure(text=msg, text_color="#C92C2C")
            try:
                self.audio.play_error()
            except Exception:
                pass
            return

        if self._codes_equivalent(user_code, target_code):
            self._on_code_builder_success()
            return

        u_lines = self._normalize_code(user_code).split("\n")
        t_lines = self._normalize_code(target_code).split("\n")
        problems = []
        for i, tline in enumerate(t_lines):
            uline = u_lines[i] if i < len(u_lines) else None
            if uline is None:
                preview = tline[:50] + ("..." if len(tline) > 50 else "")
                problems.append(f"Falta linea {i+1}: {preview}")
                break
            if uline != tline:
                if uline.strip() == "" and tline.strip():
                    problems.append(f"Linea {i+1} vacia; se esperaba codigo")
                elif tline.strip().startswith(uline.strip()) and uline.strip():
                    problems.append(f"Linea {i+1} incompleta")
                else:
                    problems.append(f"Linea {i+1} no coincide (revisa indentacion/operadores)")
                break
        if not problems and len(u_lines) > len(t_lines):
            problems.append(f"Hay {len(u_lines) - len(t_lines)} linea(s) de mas al final")

        self.code_textbox.configure(border_color="#C92C2C")
        msg = problems[0] if problems else "No coincide. Revisa indentacion y sintaxis."
        ai_note = ""
        try:
            if getattr(self, "use_ai", False) and getattr(self, "tutor", None):
                desc = ""
                concept = ""
                if getattr(self, "_builder_exercise", None):
                    desc = self._builder_exercise.get("description", "")
                    concept = self._builder_exercise.get("concept", "")
                guided = self.tutor.explain_mismatch(
                    user_code=user_code,
                    target_code=target_code,
                    concept=concept,
                    description=desc,
                )
                if guided:
                    ai_note = guided
        except Exception:
            ai_note = ""
        self.lbl_feedback.configure(text=msg, text_color="#C92C2C")
        if ai_note:
            self.lbl_hint.configure(text=f"🤖 Tutor: {ai_note}")
            self.lbl_hint.pack(pady=(0, 8))
        try:
            self.audio.play_error()
        except Exception:
            pass

    def _on_code_builder_success(self):
        try:
            self.audio.play_levelup()
        except Exception:
            pass
        self.code_textbox.configure(border_color="#2CC985")
        base = 30 + self.current_challenge.difficulty * 10
        if getattr(self, "_builder_used_solution", False):
            base = max(5, base // 4)
        elif getattr(self, "_builder_used_reveal", False):
            base = max(10, base - 15)
        if getattr(self, "_builder_used_scaffold", False) and getattr(self, "_builder_revealed", 0) == 0:
            if not getattr(self, "_builder_used_solution", False):
                base = max(10, base - 5)
        self.player.add_xp(base)
        concept = self.current_challenge.concept
        try:
            self.player.record_challenge_completion(
                0, 0, len(self.current_challenge.text), concept, True
            )
        except Exception:
            pass

        exp = self.content.get_explanation(concept, self.current_challenge)
        bonus_note = ""
        if getattr(self, "_builder_used_solution", False):
            bonus_note = " (viste la solucion)"
        elif getattr(self, "_builder_used_reveal", False):
            bonus_note = " (XP reducido por revelaciones)"
        elif getattr(self, "_builder_used_scaffold", False):
            bonus_note = " (usaste scaffold)"
        self.lbl_feedback.configure(
            text=f"Codigo correcto! +{base} XP{bonus_note}",
            text_color="#2CC985",
        )
        if exp:
            self.lbl_hint.configure(text=f"📖 {exp}")
            self.lbl_hint.pack(pady=(0, 8))
        self.lbl_level.configure(text=f"LVL {self.player.level}")
        need = max(1, self.player.xp_for_next_level)
        self.progress.set(min(1.0, self.player.xp / need))
        self.after(1800, self._new_code_builder_exercise)

    def _ai_builder_hint(self):
        """Request a guided hint from Ollama without revealing the full solution."""
        if self.mode != "CODE_BUILDER" or not getattr(self, "_builder_exercise", None):
            return
        if not getattr(self, "use_ai", False) or not getattr(self, "tutor", None):
            self.lbl_feedback.configure(text="Activa IA local (Ollama) para pistas del tutor", text_color="#FFB84D")
            return
        try:
            self.lbl_feedback.configure(text="Consultando tutor local…", text_color="#888")
            self.update_idletasks()
            partial = self.code_textbox.get("1.0", "end-1c")
            hint = self.tutor.guided_hint(
                description=self._builder_exercise.get("description", ""),
                concept=self._builder_exercise.get("concept", ""),
                partial_code=partial,
            )
            if hint:
                self.lbl_hint.configure(text=f"🤖 {hint}")
                self.lbl_hint.pack(pady=(0, 8))
                self.lbl_feedback.configure(text="Pista del tutor lista", text_color="#4ECDC4")
            else:
                self.lbl_feedback.configure(text="El tutor no respondio; prueba Scaffold o Revelar linea", text_color="#FFB84D")
        except Exception as e:
            self.lbl_feedback.configure(text=f"Tutor no disponible: {e}", text_color="#C92C2C")
