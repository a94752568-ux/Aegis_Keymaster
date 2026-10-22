"""Content Generator Module - Python challenges with blanks and explanations"""
import random
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class Challenge:
    text: str
    difficulty: int
    category: str
    concept: str
    hint: str = ""
    challenge_type: str = "full"
    prompt: str = ""
    explanation: str = ""


class ContentGenerator:
    def __init__(self):
        self.learning_paths = self._init_learning_paths()
        self.code_builder_exercises = self._init_code_builder_exercises()
        self.daily_challenges = []
        self._generate_daily_challenges()

    def _init_learning_paths(self) -> Dict[str, List[Challenge]]:
        return {
            "basics": [
                Challenge("x = 42", 1, "basics", "variables", "Asignar entero"),
                Challenge("name = 'Python'", 1, "basics", "variables", "Asignar string"),
                Challenge("is_active = True", 1, "basics", "variables", "Booleano"),
                Challenge("data = None", 1, "basics", "variables", "None"),
                Challenge("print('Hello World')", 1, "basics", "output", "Print"),
                Challenge("print(f'Value: {x}')", 2, "basics", "output", "F-string"),
                Challenge("result = 10 + 5", 2, "basics", "operations", "Suma"),
                Challenge("total = sum([1, 2, 3])", 2, "basics", "operations", "sum"),
                Challenge("length = len('hello')", 2, "basics", "operations", "len"),
                Challenge("42", 1, "basics", "variables", "Entero", "blank", "x = ____", "Asignar crea la variable; el tipo se infiere."),
                Challenge("True", 1, "basics", "variables", "Booleano", "blank", "is_active = ____", "True/False van con mayuscula."),
                Challenge("None", 1, "basics", "variables", "Nulo", "blank", "data = ____", "None es el valor nulo; se compara con is."),
                Challenge("len", 2, "basics", "operations", "Longitud", "blank", "length = ____('hello')", "len() sirve para str, list, dict, etc."),
                Challenge("sum", 2, "basics", "operations", "Suma", "blank", "total = ____([1, 2, 3])", "sum() suma elementos de un iterable."),
                Challenge("f", 2, "basics", "output", "f-string", "blank", "print(____'Value: {x}')", "Las f-strings interpolan con llaves."),
            ],
            "data_structures": [
                Challenge("numbers = [1, 2, 3]", 2, "data_structures", "lists", "Lista"),
                Challenge("nums.append(4)", 2, "data_structures", "lists", "append"),
                Challenge("user = {'name': 'Ana'}", 3, "data_structures", "dicts", "Dict"),
                Challenge("append", 2, "data_structures", "lists", "Agregar", "blank", "nums.____(4)", "append modifica in-place y devuelve None."),
                Challenge("get", 3, "data_structures", "dicts", "Acceso seguro", "blank", "name = user.____('name')", "dict.get evita KeyError."),
            ],
            "control_flow": [
                Challenge("if x > 0:", 2, "control_flow", "conditionals", "if"),
                Challenge("for i in range(10):", 3, "control_flow", "loops", "for range"),
                Challenge("while count < 10:", 3, "control_flow", "loops", "while"),
                Challenge("range", 3, "control_flow", "loops", "range", "blank", "for i in ____(10):", "range(10) produce 0..9 (fin exclusivo)."),
                Challenge(":", 2, "control_flow", "conditionals", "dos puntos", "blank", "if x > 0____", "Tras if/for/def va ':' y el bloque indentado."),
            ],
            "functions": [
                Challenge("def hello():", 3, "functions", "basic", "def"),
                Challenge("def add(a, b):\n    return a + b", 4, "functions", "basic", "return"),
                Challenge("lambda x: x * 2", 5, "functions", "lambda", "lambda"),
                Challenge("def", 3, "functions", "basic", "definir", "blank", "____ greet(name):", "Las funciones se definen con def."),
                Challenge("return", 4, "functions", "basic", "devolver", "blank", "def add(a, b):\n    ____ a + b", "Sin return la funcion devuelve None."),
            ],
            "oop": [Challenge("class Person:", 4, "oop", "classes", "class")],
            "modules": [Challenge("import math", 3, "modules", "imports", "import")],
            "file_io": [Challenge("with open('file.txt') as f:", 5, "file_io", "reading", "with open")],
            "exceptions": [Challenge("try:", 4, "exceptions", "handling", "try")],
            "advanced": [Challenge("@decorator", 6, "advanced", "decorators", "decorator")],
            "stdlib": [Challenge("import json", 3, "stdlib", "json", "json")],
            "best_practices": [Challenge("assert x > 0, 'msg'", 5, "best_practices", "assertions", "assert")],
        }

    def get_challenge(self, difficulty: int, path: str = None, prefer_blank: bool = False) -> Challenge:
        def _pick(candidates):
            if not candidates:
                return None
            if prefer_blank:
                blanks = [c for c in candidates if getattr(c, "challenge_type", "full") == "blank"]
                if blanks and random.random() < 0.45:
                    return random.choice(blanks)
            return random.choice(candidates)
        if path and path in self.learning_paths:
            candidates = [ch for ch in self.learning_paths[path] if abs(ch.difficulty - difficulty) <= 2]
            picked = _pick(candidates)
            if picked:
                return picked
        all_ch = []
        for challenges in self.learning_paths.values():
            all_ch.extend([ch for ch in challenges if abs(ch.difficulty - difficulty) <= 2])
        picked = _pick(all_ch)
        if picked:
            return picked
        all_ch = [ch for challenges in self.learning_paths.values() for ch in challenges]
        return random.choice(all_ch)

    def get_path_progress(self, path: str, completed_concepts: set) -> Tuple[int, int]:
        if path not in self.learning_paths:
            return 0, 0
        concepts = set(ch.concept for ch in self.learning_paths[path])
        return len(concepts & completed_concepts), len(concepts)

    def _generate_daily_challenges(self):
        self.daily_challenges = [self.get_challenge(3), self.get_challenge(6), self.get_challenge(9)]

    def get_daily_challenges(self) -> List[Challenge]:
        return self.daily_challenges

    def get_available_paths(self) -> List[str]:
        return list(self.learning_paths.keys())

    def get_path_name(self, path: str) -> str:
        names = {"basics": "Fundamentos", "data_structures": "Estructuras de Datos", "control_flow": "Control de Flujo", "functions": "Funciones", "oop": "POO", "modules": "Modulos", "file_io": "Archivos I/O", "exceptions": "Excepciones", "advanced": "Avanzado", "stdlib": "Stdlib", "best_practices": "Buenas Practicas"}
        return names.get(path, path.title())

    def get_recommended_path_order(self) -> List[str]:
        return ["basics", "data_structures", "control_flow", "functions", "modules", "file_io", "exceptions", "oop", "stdlib", "best_practices", "advanced"]

    def get_explanation(self, concept: str, challenge: Challenge = None) -> str:
        if challenge is not None and getattr(challenge, "explanation", ""):
            return challenge.explanation
        tips = {"variables": "Las variables se crean al asignar; no declaras el tipo.", "operations": "Prefiere built-ins (len, sum, round) cuando baste.", "output": "print acepta varios args; f-strings son la forma moderna.", "lists": "Las listas son mutables; append modifica in-place.", "dicts": "Usa .get() para acceso seguro sin KeyError.", "loops": "for itera iterables; range genera enteros (fin exclusivo).", "conditionals": "Tras if/else va ':' y el bloque indentado.", "basic": "def nombre(params): y return para devolver valor.", "lambda": "lambda args: expr — una sola expresion.", "classes": "class + __init__(self, ...) para estado.", "exceptions": "try/except atrapa errores.", "file_io": "with open cierra el archivo aunque haya errores."}
        return tips.get(concept, "Practica este patron hasta automatizarlo.")

    def get_challenge_display_text(self, challenge: Challenge) -> str:
        if getattr(challenge, "challenge_type", "full") == "blank" and challenge.prompt:
            return challenge.prompt
        return challenge.text

    def _init_code_builder_exercises(self) -> Dict[str, List[Dict]]:
        try:
            from builder_content import BUILDER_EXERCISES
            return BUILDER_EXERCISES
        except ImportError:
            return {"basic_functions": [{"title": "Suma", "difficulty": 2, "code": "def sumar(a, b):\n    return a + b", "scaffold": "def sumar(a, b):\n    pass", "description": "Suma dos numeros", "goals": ["return a + b"], "concept": "functions"}]}

    def get_code_builder_exercise(self, difficulty: int = None, category: str = None):
        if category and category in self.code_builder_exercises:
            exercises = self.code_builder_exercises[category]
            if difficulty:
                filtered = [ex for ex in exercises if abs(ex['difficulty'] - difficulty) <= 2]
                if filtered:
                    return random.choice(filtered)
            return random.choice(exercises)
        all_ex = []
        for exercises in self.code_builder_exercises.values():
            all_ex.extend(exercises)
        return random.choice(all_ex) if all_ex else None

    def get_code_builder_categories(self) -> List[str]:
        return list(self.code_builder_exercises.keys())

    def get_code_builder_structure_hint(self, exercise: dict) -> str:
        code = exercise.get("code", "")
        lines = code.split("\n")
        goals = exercise.get("goals") or []
        parts = [f"{len(lines)} lineas esperadas"]
        if goals:
            parts.append("Objetivos: " + "; ".join(goals[:4]))
        keys = []
        for kw in ("def ", "class ", "for ", "while ", "if ", "return ", "with ", "try:", "lambda "):
            if kw in code:
                keys.append(kw.strip().rstrip(":"))
        if keys:
            parts.append("Palabras clave: " + ", ".join(keys))
        return " | ".join(parts)

    def get_category_name(self, category: str) -> str:
        names = {"basic_functions": "Funciones Basicas", "loops_practice": "Practica de Bucles", "list_operations": "Operaciones con Listas", "dict_operations": "Operaciones con Dicts", "classes_basic": "Clases Basicas", "error_handling": "Manejo de Errores", "file_operations": "Operaciones con Archivos", "advanced_concepts": "Conceptos Avanzados"}
        return names.get(category, category.replace('_', ' ').title())
