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
        try:
            self._sync_learner_context()
        except Exception:
            pass
        diff = min(8, 2 + self.player.level // 3)
        exercise = self.content.get_code_builder_exercise(
            difficulty=diff, category=self.current_code_category
        )
        if not exercise:
            self.lbl_feedback.configure(text="Sin ejercicios en esta categoria", text_color="#FF3355")
            return
        self._builder_exercise = exercise
        self._builder_revealed = 0
        self._builder_used_scaffold = False
        self._builder_used_reveal = False
        self._builder_used_solution = False
        self._builder_passed_via_tests = False
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
        self.lbl_diff.configure(text=f"Nivel {exercise['difficulty']} | {cat_name}")
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
        self._clear_diff_tags()
        self.code_textbox.configure(border_color="#00A8B8")
        n_lines = len(exercise["code"].split("\n"))
        n_tests = len(exercise.get("tests") or [])
        test_note = f" · {n_tests} tests" if n_tests else " · match exacto"
        self.lbl_feedback.configure(
            text=f"Escribe el codigo ({n_lines} lineas{test_note}). Scaffold / Revelar / Ver solucion / Tutor IA. Ctrl+Enter verifica.",
            text_color="#6B7C93",
        )
        self.lbl_hint.pack_forget()
        self.code_textbox.focus()

    def _load_scaffold(self):
        if self.mode != "CODE_BUILDER" or not getattr(self, "_builder_exercise", None):
            return
        scaffold = self._builder_exercise.get("scaffold") or ""
        if not scaffold.strip():
            self.lbl_feedback.configure(text="Este ejercicio no tiene scaffold", text_color="#FFB020")
            return
        self._builder_used_scaffold = True
        self.code_textbox.delete("1.0", "end")
        self._clear_diff_tags()
        self.code_textbox.insert("1.0", scaffold)
        self.code_textbox.configure(border_color="#00E5FF")
        self.lbl_feedback.configure(text="Scaffold cargado. Completa los pass / comentarios.", text_color="#00E5FF")
        self.code_textbox.focus()

    def _reveal_line(self):
        if self.mode != "CODE_BUILDER" or not getattr(self, "_builder_exercise", None):
            return
        target_lines = self._builder_exercise["code"].split("\n")
        if self._builder_revealed >= len(target_lines):
            self.lbl_feedback.configure(text="Ya se revelaron todas las lineas", text_color="#FFB020")
            return
        self._builder_used_reveal = True
        revealed = target_lines[: self._builder_revealed + 1]
        self._builder_revealed += 1
        partial = "\n".join(revealed)
        self.code_textbox.delete("1.0", "end")
        self._clear_diff_tags()
        self.code_textbox.insert("1.0", partial)
        self.code_textbox.configure(border_color="#A855F7")
        left = len(target_lines) - self._builder_revealed
        self.lbl_feedback.configure(text=f"Linea {self._builder_revealed}/{len(target_lines)} revelada. Quedan {left}.", text_color="#A855F7")
        self.code_textbox.focus()

    def _show_solution(self):
        if self.mode != "CODE_BUILDER" or not getattr(self, "_builder_exercise", None):
            return
        code = self._builder_exercise.get("code") or ""
        if not code.strip():
            self.lbl_feedback.configure(text="No hay solucion disponible", text_color="#FF3355")
            return
        self._builder_used_solution = True
        self._builder_used_reveal = True
        self._builder_revealed = len(code.split("\n"))
        self.code_textbox.delete("1.0", "end")
        self._clear_diff_tags()
        self.code_textbox.insert("1.0", code)
        self.code_textbox.configure(border_color="#FF3355")
        goals = self._builder_exercise.get("goals") or []
        note = "Solucion completa. Estudia y escribe de nuevo (Siguiente) para practicar."
        if goals:
            note += " Objetivos: " + " · ".join(goals)
        self.lbl_feedback.configure(text=note, text_color="#FF3355")
        try:
            self.audio.play_powerup()
        except Exception:
            pass
        self.code_textbox.focus()

    def _get_textbox_widget(self):
        tb = self.code_textbox
        return getattr(tb, "_textbox", tb)

    def _setup_diff_tags(self):
        try:
            tb = self._get_textbox_widget()
            tb.tag_configure("diff_ok", background="#0A1F14", foreground="#39FF14")
            tb.tag_configure("diff_bad", background="#2A0A12", foreground="#FF6B7A")
            tb.tag_configure("diff_extra", background="#1A1208", foreground="#FFB020")
            tb.tag_raise("sel")
        except Exception:
            pass

    def _clear_diff_tags(self):
        try:
            tb = self._get_textbox_widget()
            for tag in ("diff_ok", "diff_bad", "diff_extra"):
                tb.tag_remove(tag, "1.0", "end")
        except Exception:
            pass

    def _apply_line_diff(self, user_code: str, target_code: str) -> str:
        self._setup_diff_tags()
        self._clear_diff_tags()
        t_lines = self._normalize_code(target_code).split("\n")
        tb = self._get_textbox_widget()
        raw = self.code_textbox.get("1.0", "end-1c")
        raw_lines = raw.replace("\r\n", "\n").split("\n")
        n_u = [ln.rstrip().replace("\t", "    ") for ln in raw_lines]
        while n_u and n_u[-1] == "":
            n_u.pop()
        n_t = t_lines
        ok = bad = extra = missing = 0
        first_bad = None
        max_check = max(len(n_u), len(n_t))
        for i in range(max_check):
            line_no = i + 1
            start = f"{line_no}.0"
            end = f"{line_no}.end"
            u = n_u[i] if i < len(n_u) else None
            t = n_t[i] if i < len(n_t) else None
            try:
                if u is not None and t is not None:
                    if u == t:
                        tb.tag_add("diff_ok", start, end)
                        ok += 1
                    else:
                        tb.tag_add("diff_bad", start, end)
                        bad += 1
                        if first_bad is None:
                            first_bad = line_no
                elif u is not None and t is None:
                    tb.tag_add("diff_extra", start, end)
                    extra += 1
                    if first_bad is None:
                        first_bad = line_no
                elif u is None and t is not None:
                    missing += 1
                    if first_bad is None:
                        first_bad = line_no
            except Exception:
                pass
        if first_bad is not None:
            try:
                tb.see(f"{first_bad}.0")
                tb.mark_set("insert", f"{first_bad}.0")
            except Exception:
                pass
        parts = []
        if bad:
            parts.append(f"{bad} distinta(s)")
        if missing:
            parts.append(f"{missing} faltante(s)")
        if extra:
            parts.append(f"{extra} de mas")
        summary = "Diff: " + ", ".join(parts) if parts else "Diff: revisa el codigo"
        if first_bad:
            summary += f" · linea {first_bad}"
        summary += "  |  verde=ok  rojo=error  ambar=extra"
        return summary

    def _run_exercise_tests(self, user_code: str, tests: list):
        if not tests:
            return None, "sin tests"
        import io
        import contextlib
        ns = {"__name__": "__builder_test__"}
        buf = io.StringIO()
        try:
            compiled = compile(user_code, "<user>", "exec")
            with contextlib.redirect_stdout(buf):
                exec(compiled, ns, ns)
        except Exception as e:
            return False, f"Error al ejecutar tu codigo: {type(e).__name__}: {e}"
        out = buf.getvalue()
        passed = 0
        for i, t in enumerate(tests, 1):
            if isinstance(t, str):
                try:
                    exec(compile(t, f"<test{i}>", "exec"), ns, ns)
                    passed += 1
                except AssertionError:
                    return False, f"Test {i}/{len(tests)} fallo: {t}"
                except Exception as e:
                    return False, f"Test {i}/{len(tests)} error: {type(e).__name__}: {e}"
            elif isinstance(t, dict):
                if "stdout_contains" in t:
                    needle = str(t["stdout_contains"])
                    if needle not in out:
                        return False, f"Test {i}/{len(tests)}: salida no contiene {needle!r}"
                    passed += 1
                elif "stdout_equals" in t:
                    if out.strip() != str(t["stdout_equals"]).strip():
                        return False, f"Test {i}/{len(tests)}: salida esperada {t['stdout_equals']!r}"
                    passed += 1
                elif "var" in t:
                    name = t["var"]
                    expected = t.get("equals")
                    actual = ns.get(name, "__missing__")
                    if actual != expected:
                        return False, f"Test {i}/{len(tests)}: {name}={actual!r}, se esperaba {expected!r}"
                    passed += 1
                else:
                    return False, f"Test {i}: formato desconocido"
            else:
                return False, f"Test {i}: tipo no soportado"
        return True, f"{passed}/{len(tests)} tests OK"

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
            self.code_textbox.configure(border_color="#FF3355")
            msg = f"Error de sintaxis (linea {e.lineno}): {e.msg}"
            self.lbl_feedback.configure(text=msg, text_color="#FF3355")
            try:
                self._setup_diff_tags()
                self._clear_diff_tags()
                ln = e.lineno or 1
                tb = self._get_textbox_widget()
                tb.tag_add("diff_bad", f"{ln}.0", f"{ln}.end")
                tb.see(f"{ln}.0")
            except Exception:
                pass
            try:
                self.audio.play_error()
            except Exception:
                pass
            return
        tests = []
        try:
            if getattr(self, "_builder_exercise", None):
                tests = list(self._builder_exercise.get("tests") or [])
        except Exception:
            tests = []
        if tests:
            ok, msg = self._run_exercise_tests(user_code, tests)
            if ok:
                self._builder_passed_via_tests = True
                self.lbl_feedback.configure(text=f"Tests: {msg}", text_color="#39FF14")
                self._on_code_builder_success()
                return
            self.code_textbox.configure(border_color="#FF3355")
            self.lbl_feedback.configure(text=msg, text_color="#FF3355")
            try:
                self._apply_line_diff(user_code, target_code)
            except Exception:
                pass
            try:
                self.audio.play_error()
            except Exception:
                pass
            try:
                concept = ""
                if getattr(self, "_builder_exercise", None):
                    concept = self._builder_exercise.get("concept", "")
                if concept and hasattr(self, "player"):
                    self.player.record_concept_fail(concept, errors=1)
            except Exception:
                pass
            return
        if self._codes_equivalent(user_code, target_code):
            self._builder_passed_via_tests = False
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
        self.code_textbox.configure(border_color="#FF3355")
        diff_summary = self._apply_line_diff(user_code, target_code)
        msg = problems[0] if problems else "No coincide. Revisa indentacion y sintaxis."
        self.lbl_feedback.configure(text=msg + "\n" + diff_summary, text_color="#FF3355")
        try:
            concept = ""
            if getattr(self, "_builder_exercise", None):
                concept = self._builder_exercise.get("concept", "")
            if concept and hasattr(self, "player"):
                self.player.record_concept_fail(concept, errors=1)
        except Exception:
            pass
        try:
            self.audio.play_error()
        except Exception:
            pass

    def _on_code_builder_success(self):
        try:
            self.audio.play_levelup()
        except Exception:
            pass
        self._clear_diff_tags()
        try:
            self._setup_diff_tags()
            tb = self._get_textbox_widget()
            tb.tag_add("diff_ok", "1.0", "end")
        except Exception:
            pass
        self.code_textbox.configure(border_color="#39FF14")
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
        try:
            if hasattr(self, "player") and hasattr(self.player, "bump_contract"):
                just = self.player.bump_contract("constructor_ok", 1)
                if just and hasattr(self, "_refresh_contracts_label"):
                    self._refresh_contracts_label()
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
        via = " · tests OK" if getattr(self, "_builder_passed_via_tests", False) else ""
        self.lbl_feedback.configure(
            text=f"Codigo correcto{via}! +{base} XP{bonus_note}",
            text_color="#39FF14",
        )
        self._builder_passed_via_tests = False
        if exp:
            self.lbl_hint.configure(text=f"📖 {exp}")
            self.lbl_hint.pack(pady=(0, 8))
        self.lbl_level.configure(text=f"LVL {self.player.level}")
        need = max(1, self.player.xp_for_next_level)
        self.progress.set(min(1.0, self.player.xp / need))
        self.after(1800, self._new_code_builder_exercise)

    def _ai_builder_hint(self):
        if self.mode != "CODE_BUILDER" or not getattr(self, "_builder_exercise", None):
            return
        if not getattr(self, "use_ai", False) or not getattr(self, "tutor", None):
            self.lbl_feedback.configure(text="Activa IA local (Ollama) para pistas del tutor", text_color="#FFB020")
            return
        try:
            self.lbl_feedback.configure(text="Consultando tutor local…", text_color="#6B7C93")
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
                self.lbl_feedback.configure(text="Pista del tutor lista", text_color="#00E5FF")
            else:
                self.lbl_feedback.configure(text="El tutor no respondio; prueba Scaffold o Revelar linea", text_color="#FFB020")
        except Exception as e:
            self.lbl_feedback.configure(text=f"Tutor no disponible: {e}", text_color="#FF3355")
