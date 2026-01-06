"""
Content Generator Module
Generates Python code challenges organized by learning paths and difficulty
"""
import random
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class Challenge:
    """Represents a code challenge"""
    text: str
    difficulty: int
    category: str
    concept: str
    hint: str = ""


class ContentGenerator:
    """Generates structured Python learning content"""
    
    def __init__(self):
        self.learning_paths = self._init_learning_paths()
        self.code_builder_exercises = self._init_code_builder_exercises()
        self.daily_challenges = []
        self._generate_daily_challenges()
    
    def _init_learning_paths(self) -> Dict[str, List[Challenge]]:
        """Initialize learning paths with structured Python challenges"""
        return {
            "basics": [
                # Variables and types
                Challenge("x = 42", 1, "basics", "variables", "Asignar un número entero"),
                Challenge("name = 'Python'", 1, "basics", "variables", "Asignar un string"),
                Challenge("pi = 3.14159", 1, "basics", "variables", "Asignar un float"),
                Challenge("is_active = True", 1, "basics", "variables", "Asignar un booleano"),
                Challenge("data = None", 1, "basics", "variables", "Usar None"),
                
                # Basic operations
                Challenge("result = 10 + 5", 2, "basics", "operations", "Suma"),
                Challenge("total = sum([1, 2, 3])", 2, "basics", "operations", "Función sum"),
                Challenge("length = len('hello')", 2, "basics", "operations", "Función len"),
                Challenge("rounded = round(3.7)", 2, "basics", "operations", "Función round"),
                
                # Print statements
                Challenge("print('Hello World')", 1, "basics", "output", "Print simple"),
                Challenge("print(f'Value: {x}')", 2, "basics", "output", "F-string"),
                Challenge("print(x, y, sep=', ')", 2, "basics", "output", "Print con separador"),
            ],
            
            "data_structures": [
                # Lists
                Challenge("numbers = [1, 2, 3]", 2, "data_structures", "lists", "Crear lista"),
                Challenge("nums.append(4)", 2, "data_structures", "lists", "Agregar elemento"),
                Challenge("nums[0] = 10", 2, "data_structures", "lists", "Modificar elemento"),
                Challenge("first = nums[0]", 2, "data_structures", "lists", "Acceder elemento"),
                Challenge("last = nums[-1]", 3, "data_structures", "lists", "Último elemento"),
                Challenge("sliced = nums[1:3]", 3, "data_structures", "lists", "Slicing"),
                Challenge("nums.extend([5, 6])", 3, "data_structures", "lists", "Extend"),
                Challenge("nums.remove(3)", 3, "data_structures", "lists", "Remove"),
                
                # Dictionaries
                Challenge("user = {'name': 'Ana'}", 3, "data_structures", "dicts", "Crear diccionario"),
                Challenge("user['age'] = 25", 3, "data_structures", "dicts", "Agregar clave"),
                Challenge("name = user.get('name')", 3, "data_structures", "dicts", "Get seguro"),
                Challenge("keys = user.keys()", 3, "data_structures", "dicts", "Obtener claves"),
                
                # Sets and tuples
                Challenge("unique = {1, 2, 3}", 3, "data_structures", "sets", "Crear set"),
                Challenge("coords = (10, 20)", 2, "data_structures", "tuples", "Crear tupla"),
            ],
            
            "control_flow": [
                # Conditionals
                Challenge("if x > 0:", 2, "control_flow", "conditionals", "If simple"),
                Challenge("if x > 0:\n    print('pos')", 3, "control_flow", "conditionals", "If con bloque"),
                Challenge("if x > 0:\n    pass\nelse:\n    pass", 4, "control_flow", "conditionals", "If-else"),
                Challenge("result = x if x > 0 else 0", 4, "control_flow", "conditionals", "Ternario"),
                
                # Loops
                Challenge("for i in range(10):", 3, "control_flow", "loops", "For con range"),
                Challenge("for item in items:", 3, "control_flow", "loops", "For en lista"),
                Challenge("while count < 10:", 3, "control_flow", "loops", "While loop"),
                Challenge("for i, val in enumerate(lst):", 4, "control_flow", "loops", "Enumerate"),
                Challenge("for k, v in dict.items():", 4, "control_flow", "loops", "Iterar dict"),
                
                # List comprehensions
                Challenge("squares = [x**2 for x in nums]", 5, "control_flow", "comprehensions", "List comp"),
                Challenge("evens = [x for x in nums if x % 2 == 0]", 5, "control_flow", "comprehensions", "List comp con filtro"),
            ],
            
            "functions": [
                Challenge("def hello():", 3, "functions", "basic", "Función simple"),
                Challenge("def greet(name):", 3, "functions", "basic", "Función con parámetro"),
                Challenge("def add(a, b):\n    return a + b", 4, "functions", "basic", "Función con return"),
                Challenge("def func(x=10):", 4, "functions", "params", "Parámetro default"),
                Challenge("def func(*args):", 4, "functions", "params", "Args variables"),
                Challenge("def func(**kwargs):", 4, "functions", "params", "Kwargs"),
                Challenge("lambda x: x * 2", 5, "functions", "lambda", "Lambda simple"),
                Challenge("sorted(items, key=lambda x: x['age'])", 6, "functions", "lambda", "Lambda como key"),
            ],
            
            "oop": [
                Challenge("class Person:", 4, "oop", "classes", "Definir clase"),
                Challenge("def __init__(self, name):", 5, "oop", "classes", "Constructor"),
                Challenge("self.name = name", 5, "oop", "classes", "Atributo de instancia"),
                Challenge("def get_name(self):", 5, "oop", "classes", "Método de instancia"),
                Challenge("class Student(Person):", 6, "oop", "inheritance", "Herencia"),
                Challenge("super().__init__(name)", 6, "oop", "inheritance", "Llamar super"),
                Challenge("@property", 6, "oop", "decorators", "Property decorator"),
                Challenge("@staticmethod", 6, "oop", "decorators", "Static method"),
            ],
            
            "modules": [
                Challenge("import math", 3, "modules", "imports", "Import módulo"),
                Challenge("from math import sqrt", 3, "modules", "imports", "Import específico"),
                Challenge("import numpy as np", 3, "modules", "imports", "Import con alias"),
                Challenge("from package import *", 4, "modules", "imports", "Import todo"),
                Challenge("if __name__ == '__main__':", 5, "modules", "main", "Main guard"),
            ],
            
            "file_io": [
                Challenge("with open('file.txt') as f:", 5, "file_io", "reading", "Context manager"),
                Challenge("content = f.read()", 4, "file_io", "reading", "Leer archivo"),
                Challenge("lines = f.readlines()", 4, "file_io", "reading", "Leer líneas"),
                Challenge("f.write('Hello\\n')", 4, "file_io", "writing", "Escribir archivo"),
            ],
            
            "exceptions": [
                Challenge("try:", 4, "exceptions", "handling", "Try block"),
                Challenge("except Exception as e:", 4, "exceptions", "handling", "Except block"),
                Challenge("finally:", 4, "exceptions", "handling", "Finally block"),
                Challenge("raise ValueError('msg')", 5, "exceptions", "raising", "Raise exception"),
            ],
            
            "advanced": [
                Challenge("@decorator", 6, "advanced", "decorators", "Usar decorator"),
                Challenge("def decorator(func):", 7, "advanced", "decorators", "Definir decorator"),
                Challenge("with context_manager():", 6, "advanced", "context", "Context manager"),
                Challenge("async def fetch():", 7, "advanced", "async", "Async function"),
                Challenge("await asyncio.sleep(1)", 7, "advanced", "async", "Await"),
                Challenge("data = {'a': 1, **other}", 6, "advanced", "unpacking", "Dict unpacking"),
                Challenge("[*list1, *list2]", 6, "advanced", "unpacking", "List unpacking"),
            ],
            
            "stdlib": [
                Challenge("from datetime import datetime", 4, "stdlib", "datetime", "Import datetime"),
                Challenge("now = datetime.now()", 4, "stdlib", "datetime", "Datetime now"),
                Challenge("from collections import Counter", 5, "stdlib", "collections", "Import Counter"),
                Challenge("import json", 3, "stdlib", "json", "Import json"),
                Challenge("data = json.loads(text)", 4, "stdlib", "json", "Parse JSON"),
                Challenge("import random", 3, "stdlib", "random", "Import random"),
                Challenge("num = random.randint(1, 10)", 4, "stdlib", "random", "Random int"),
            ],
            
            "best_practices": [
                Challenge("# TODO: implement feature", 2, "best_practices", "comments", "TODO comment"),
                Challenge("\"\"\"Docstring\"\"\"", 3, "best_practices", "docs", "Docstring"),
                Challenge("if __debug__:", 5, "best_practices", "debug", "Debug flag"),
                Challenge("assert x > 0, 'msg'", 5, "best_practices", "assertions", "Assertion"),
            ]
        }
    
    def get_challenge(self, difficulty: int, path: str = None) -> Challenge:
        """Get a challenge based on difficulty and optional learning path"""
        if path and path in self.learning_paths:
            # Filter by path and difficulty
            candidates = [
                ch for ch in self.learning_paths[path]
                if abs(ch.difficulty - difficulty) <= 2
            ]
            if candidates:
                return random.choice(candidates)
        
        # Get from any path matching difficulty
        all_challenges = []
        for challenges in self.learning_paths.values():
            all_challenges.extend([
                ch for ch in challenges
                if abs(ch.difficulty - difficulty) <= 2
            ])
        
        if all_challenges:
            return random.choice(all_challenges)
        
        # Fallback to any challenge
        all_challenges = [ch for challenges in self.learning_paths.values() for ch in challenges]
        return random.choice(all_challenges)
    
    def get_path_progress(self, path: str, completed_concepts: set) -> Tuple[int, int]:
        """Get progress in a learning path"""
        if path not in self.learning_paths:
            return 0, 0
        
        challenges = self.learning_paths[path]
        concepts = set(ch.concept for ch in challenges)
        completed = len(concepts & completed_concepts)
        total = len(concepts)
        return completed, total
    
    def _generate_daily_challenges(self):
        """Generate 3 daily challenges of varying difficulty"""
        self.daily_challenges = [
            self.get_challenge(3),  # Easy
            self.get_challenge(6),  # Medium
            self.get_challenge(9),  # Hard
        ]
    
    def get_daily_challenges(self) -> List[Challenge]:
        """Get today's daily challenges"""
        return self.daily_challenges
    
    def get_available_paths(self) -> List[str]:
        """Get list of all learning paths"""
        return list(self.learning_paths.keys())
    
    def get_path_name(self, path: str) -> str:
        """Get display name for a learning path"""
        names = {
            "basics": "Fundamentos",
            "data_structures": "Estructuras de Datos",
            "control_flow": "Control de Flujo",
            "functions": "Funciones",
            "oop": "Programación Orientada a Objetos",
            "modules": "Módulos e Imports",
            "file_io": "Archivos I/O",
            "exceptions": "Excepciones",
            "advanced": "Conceptos Avanzados",
            "stdlib": "Biblioteca Estándar",
            "best_practices": "Buenas Prácticas"
        }
        return names.get(path, path.title())
    
    def _init_code_builder_exercises(self) -> Dict[str, List[Dict]]:
        """Initialize full code structure exercises for Code Builder mode"""
        return {
            "basic_functions": [
                {
                    "title": "Función de Saludo Simple",
                    "difficulty": 2,
                    "code": "def saludar(nombre):\n    return f'Hola, {nombre}!'",
                    "description": "Crea una función que salude a una persona por su nombre",
                    "concept": "functions"
                },
                {
                    "title": "Calcular Suma",
                    "difficulty": 2,
                    "code": "def sumar(a, b):\n    resultado = a + b\n    return resultado",
                    "description": "Función que suma dos números y devuelve el resultado",
                    "concept": "functions"
                },
                {
                    "title": "Verificar Par o Impar",
                    "difficulty": 3,
                    "code": "def es_par(numero):\n    if numero % 2 == 0:\n        return True\n    else:\n        return False",
                    "description": "Función que verifica si un número es par",
                    "concept": "conditionals"
                },
            ],
            
            "loops_practice": [
                {
                    "title": "Imprimir Números del 1 al 10",
                    "difficulty": 3,
                    "code": "for i in range(1, 11):\n    print(i)",
                    "description": "Usa un bucle for para imprimir números del 1 al 10",
                    "concept": "loops"
                },
                {
                    "title": "Suma de Lista",
                    "difficulty": 3,
                    "code": "numeros = [1, 2, 3, 4, 5]\ntotal = 0\nfor num in numeros:\n    total += num\nprint(total)",
                    "description": "Calcula la suma de todos los números en una lista",
                    "concept": "loops"
                },
                {
                    "title": "Contar Hasta Condición",
                    "difficulty": 4,
                    "code": "contador = 0\nwhile contador < 5:\n    print(f'Contador: {contador}')\n    contador += 1",
                    "description": "Usa while para contar hasta que se cumpla una condición",
                    "concept": "loops"
                },
            ],
            
            "list_operations": [
                {
                    "title": "Filtrar Números Pares",
                    "difficulty": 4,
                    "code": "numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]\npares = []\nfor num in numeros:\n    if num % 2 == 0:\n        pares.append(num)\nprint(pares)",
                    "description": "Filtra solo los números pares de una lista",
                    "concept": "lists"
                },
                {
                    "title": "List Comprehension Pares",
                    "difficulty": 5,
                    "code": "numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]\npares = [n for n in numeros if n % 2 == 0]\nprint(pares)",
                    "description": "Usa list comprehension para filtrar números pares",
                    "concept": "comprehensions"
                },
                {
                    "title": "Cuadrados de Números",
                    "difficulty": 5,
                    "code": "numeros = [1, 2, 3, 4, 5]\ncuadrados = [n**2 for n in numeros]\nprint(cuadrados)",
                    "description": "Crea una lista con los cuadrados de cada número",
                    "concept": "comprehensions"
                },
            ],
            
            "dict_operations": [
                {
                    "title": "Crear y Acceder Diccionario",
                    "difficulty": 4,
                    "code": "persona = {\n    'nombre': 'Ana',\n    'edad': 25,\n    'ciudad': 'Madrid'\n}\nprint(persona['nombre'])\nprint(persona.get('edad'))",
                    "description": "Crea un diccionario y accede a sus valores",
                    "concept": "dicts"
                },
                {
                    "title": "Iterar Diccionario",
                    "difficulty": 5,
                    "code": "estudiante = {'nombre': 'Juan', 'edad': 20, 'carrera': 'Informática'}\nfor clave, valor in estudiante.items():\n    print(f'{clave}: {valor}')",
                    "description": "Itera sobre las claves y valores de un diccionario",
                    "concept": "dicts"
                },
                {
                    "title": "Contar Frecuencias",
                    "difficulty": 6,
                    "code": "palabras = ['python', 'java', 'python', 'c++', 'python', 'java']\nfrecuencia = {}\nfor palabra in palabras:\n    if palabra in frecuencia:\n        frecuencia[palabra] += 1\n    else:\n        frecuencia[palabra] = 1\nprint(frecuencia)",
                    "description": "Cuenta cuántas veces aparece cada palabra",
                    "concept": "dicts"
                },
            ],
            
            "classes_basic": [
                {
                    "title": "Clase Simple",
                    "difficulty": 5,
                    "code": "class Perro:\n    def __init__(self, nombre, edad):\n        self.nombre = nombre\n        self.edad = edad\n    \n    def ladrar(self):\n        return f'{self.nombre} dice: Guau!'\n\nmi_perro = Perro('Max', 3)\nprint(mi_perro.ladrar())",
                    "description": "Define una clase Perro con constructor y método",
                    "concept": "classes"
                },
                {
                    "title": "Clase con Property",
                    "difficulty": 6,
                    "code": "class Rectangulo:\n    def __init__(self, ancho, alto):\n        self.ancho = ancho\n        self.alto = alto\n    \n    @property\n    def area(self):\n        return self.ancho * self.alto\n\nrect = Rectangulo(5, 3)\nprint(f'Área: {rect.area}')",
                    "description": "Clase con property para calcular área",
                    "concept": "classes"
                },
            ],
            
            "error_handling": [
                {
                    "title": "Try-Except Básico",
                    "difficulty": 5,
                    "code": "try:\n    numero = int(input('Ingresa un número: '))\n    resultado = 10 / numero\n    print(f'Resultado: {resultado}')\nexcept ValueError:\n    print('Error: Debes ingresar un número')\nexcept ZeroDivisionError:\n    print('Error: No se puede dividir por cero')",
                    "description": "Maneja errores de conversión y división",
                    "concept": "exceptions"
                },
                {
                    "title": "Try-Except-Finally",
                    "difficulty": 6,
                    "code": "try:\n    archivo = open('datos.txt', 'r')\n    contenido = archivo.read()\n    print(contenido)\nexcept FileNotFoundError:\n    print('Archivo no encontrado')\nfinally:\n    print('Operación finalizada')",
                    "description": "Usa try-except-finally para manejar archivos",
                    "concept": "exceptions"
                },
            ],
            
            "file_operations": [
                {
                    "title": "Escribir Archivo",
                    "difficulty": 5,
                    "code": "with open('output.txt', 'w') as archivo:\n    archivo.write('Hola, mundo!\\n')\n    archivo.write('Python es genial\\n')\n\nprint('Archivo creado exitosamente')",
                    "description": "Escribe texto en un archivo usando context manager",
                    "concept": "file_io"
                },
                {
                    "title": "Leer Archivo Línea por Línea",
                    "difficulty": 5,
                    "code": "with open('datos.txt', 'r') as archivo:\n    for linea in archivo:\n        linea = linea.strip()\n        print(linea)",
                    "description": "Lee un archivo línea por línea",
                    "concept": "file_io"
                },
            ],
            
            "advanced_concepts": [
                {
                    "title": "Función con Args Variables",
                    "difficulty": 6,
                    "code": "def sumar_todos(*numeros):\n    total = 0\n    for num in numeros:\n        total += num\n    return total\n\nresultado = sumar_todos(1, 2, 3, 4, 5)\nprint(f'Suma total: {resultado}')",
                    "description": "Función que acepta cantidad variable de argumentos",
                    "concept": "functions"
                },
                {
                    "title": "Lambda y Map",
                    "difficulty": 7,
                    "code": "numeros = [1, 2, 3, 4, 5]\ncuadrados = list(map(lambda x: x**2, numeros))\nprint(cuadrados)",
                    "description": "Usa lambda con map para transformar lista",
                    "concept": "lambda"
                },
                {
                    "title": "Decorador Simple",
                    "difficulty": 8,
                    "code": "def mi_decorador(func):\n    def wrapper():\n        print('Antes de la función')\n        func()\n        print('Después de la función')\n    return wrapper\n\n@mi_decorador\ndef saludar():\n    print('¡Hola!')\n\nsaludar()",
                    "description": "Define y usa un decorador simple",
                    "concept": "decorators"
                },
            ],
        }
    
    def get_code_builder_exercise(self, difficulty: int = None, category: str = None):
        """Get a code builder exercise"""
        if category and category in self.code_builder_exercises:
            exercises = self.code_builder_exercises[category]
            
            if difficulty:
                # Filter by difficulty
                filtered = [ex for ex in exercises if abs(ex['difficulty'] - difficulty) <= 2]
                if filtered:
                    return random.choice(filtered)
            
            return random.choice(exercises)
        
        # Get from any category
        all_exercises = []
        for exercises in self.code_builder_exercises.values():
            if difficulty:
                all_exercises.extend([ex for ex in exercises if abs(ex['difficulty'] - difficulty) <= 2])
            else:
                all_exercises.extend(exercises)
        
        return random.choice(all_exercises) if all_exercises else None
    
    def get_code_builder_categories(self) -> List[str]:
        """Get list of code builder categories"""
        return list(self.code_builder_exercises.keys())
    
    def get_category_name(self, category: str) -> str:
        """Get display name for a code builder category"""
        names = {
            "basic_functions": "Funciones Básicas",
            "loops_practice": "Práctica de Bucles",
            "list_operations": "Operaciones con Listas",
            "dict_operations": "Operaciones con Diccionarios",
            "classes_basic": "Clases Básicas",
            "error_handling": "Manejo de Errores",
            "file_operations": "Operaciones con Archivos",
            "advanced_concepts": "Conceptos Avanzados"
        }
        return names.get(category, category.replace('_', ' ').title())