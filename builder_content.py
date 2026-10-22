"""Code Builder exercise bank."""
BUILDER_EXERCISES = {
  "basic_functions": [
    {
      "title": "Saludo",
      "difficulty": 2,
      "code": "def saludar(nombre):\n    return f'Hola, {nombre}!'",
      "scaffold": "def saludar(nombre):\n    pass",
      "description": "Funcion que reciba nombre y devuelva saludo con f-string",
      "goals": ["def saludar(nombre)", "return con f-string"],
      "concept": "functions"
    },
    {
      "title": "Suma",
      "difficulty": 2,
      "code": "def sumar(a, b):\n    return a + b",
      "scaffold": "def sumar(a, b):\n    pass",
      "description": "Suma dos numeros y devuelve el resultado",
      "goals": ["dos parametros", "return a + b"],
      "concept": "functions"
    },
    {
      "title": "Es par",
      "difficulty": 3,
      "code": "def es_par(n):\n    return n % 2 == 0",
      "scaffold": "def es_par(n):\n    pass",
      "description": "True si n es par",
      "goals": ["operador %", "return booleano"],
      "concept": "functions"
    }
  ],
  "loops_practice": [
    {
      "title": "Imprimir 1 a 10",
      "difficulty": 3,
      "code": "for i in range(1, 11):\n    print(i)",
      "scaffold": "for i in range(1, 11):\n    pass",
      "description": "Imprime 1..10 inclusive",
      "goals": ["range(1, 11)", "print(i)"],
      "concept": "loops"
    },
    {
      "title": "Suma de lista",
      "difficulty": 3,
      "code": "numeros = [1, 2, 3, 4, 5]\ntotal = 0\nfor n in numeros:\n    total += n\nprint(total)",
      "scaffold": "numeros = [1, 2, 3, 4, 5]\ntotal = 0\n# completa\nprint(total)",
      "description": "Suma elementos e imprime total",
      "goals": ["acumulador", "for + total += n"],
      "concept": "loops"
    },
    {
      "title": "While contador",
      "difficulty": 4,
      "code": "c = 0\nwhile c < 5:\n    print(c)\n    c += 1",
      "scaffold": "c = 0\nwhile c < 5:\n    pass",
      "description": "Imprime 0..4 con while",
      "goals": ["while c < 5", "c += 1"],
      "concept": "loops"
    }
  ],
  "list_operations": [
    {
      "title": "Filtrar pares",
      "difficulty": 4,
      "code": "nums = [1, 2, 3, 4, 5, 6]\npares = []\nfor n in nums:\n    if n % 2 == 0:\n        pares.append(n)\nprint(pares)",
      "scaffold": "nums = [1, 2, 3, 4, 5, 6]\npares = []\n# filtra\nprint(pares)",
      "description": "Llena pares con numeros pares",
      "goals": ["if n % 2 == 0", "append"],
      "concept": "lists"
    },
    {
      "title": "List comprehension",
      "difficulty": 5,
      "code": "nums = [1, 2, 3, 4, 5, 6]\npares = [n for n in nums if n % 2 == 0]\nprint(pares)",
      "scaffold": "nums = [1, 2, 3, 4, 5, 6]\npares = []  # comprehension\nprint(pares)",
      "description": "Pares con list comprehension",
      "goals": ["[n for n in nums if ...]"],
      "concept": "comprehensions"
    }
  ],
  "dict_operations": [
    {
      "title": "Crear y acceder",
      "difficulty": 4,
      "code": "persona = {'nombre': 'Ana', 'edad': 25}\nprint(persona['nombre'])\nprint(persona.get('edad'))",
      "scaffold": "persona = {}\n# agrega claves\nprint(persona.get('nombre'))",
      "description": "Dict con nombre y edad",
      "goals": ["literal dict", ".get()"],
      "concept": "dicts"
    },
    {
      "title": "Contar frecuencias",
      "difficulty": 6,
      "code": "words = ['a', 'b', 'a', 'c', 'b', 'a']\nfreq = {}\nfor w in words:\n    if w in freq:\n        freq[w] += 1\n    else:\n        freq[w] = 1\nprint(freq)",
      "scaffold": "words = ['a', 'b', 'a', 'c', 'b', 'a']\nfreq = {}\n# cuenta\nprint(freq)",
      "description": "Cuenta ocurrencias",
      "goals": ["freq[w] += 1"],
      "concept": "dicts"
    }
  ],
  "classes_basic": [
    {
      "title": "Clase Perro",
      "difficulty": 5,
      "code": "class Perro:\n    def __init__(self, nombre):\n        self.nombre = nombre\n\n    def ladrar(self):\n        return f'{self.nombre} dice guau'",
      "scaffold": "class Perro:\n    def __init__(self, nombre):\n        pass\n\n    def ladrar(self):\n        pass",
      "description": "Clase con __init__ y ladrar",
      "goals": ["self.nombre", "return f-string"],
      "concept": "classes"
    }
  ],
  "error_handling": [
    {
      "title": "try/except ValueError",
      "difficulty": 5,
      "code": "try:\n    x = int('abc')\nexcept ValueError:\n    print('error')",
      "scaffold": "try:\n    x = int('abc')\nexcept Exception:\n    pass",
      "description": "Captura ValueError",
      "goals": ["except ValueError", "print error"],
      "concept": "exceptions"
    }
  ],
  "file_operations": [
    {
      "title": "Escribir archivo",
      "difficulty": 5,
      "code": "with open('out.txt', 'w') as f:\n    f.write('hola')",
      "scaffold": "# escribe hola en out.txt\n",
      "description": "with open para escribir",
      "goals": ["with open", "write"],
      "concept": "file_io"
    }
  ],
  "advanced_concepts": [
    {
      "title": "map + lambda",
      "difficulty": 6,
      "code": "nums = [1, 2, 3]\nprint(list(map(lambda x: x * 2, nums)))",
      "scaffold": "nums = [1, 2, 3]\n# duplica con map/lambda\nprint(nums)",
      "description": "Duplica con map y lambda",
      "goals": ["lambda", "list(map(...))"],
      "concept": "lambda"
    }
  ]
}
