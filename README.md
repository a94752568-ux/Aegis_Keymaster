# Aegis KeyMaster

Entrenador de Python con modos de tecleo, aprendizaje guiado y constructor de codigo.

## Instalacion

```bash
pip install -r requirements.txt
python keymaster.py
```

## IA local (Ollama) — opcional

Mejora ejercicios dinamicos y feedback guiado con un LLM en tu maquina.

1. Instala [Ollama](https://ollama.com)
2. Descarga un modelo ligero: `ollama pull llama3.2`
3. Asegurate de que el servicio corre (`ollama serve` si hace falta)
4. Abre KeyMaster y activa el switch **IA local (Ollama)**

Con IA activa:
- ~55% de los retos de Aprendizaje/Constructor se generan al momento
- En Constructor, **Tutor IA** da pistas sin revelar la solucion
- Si fallas al verificar, el tutor explica el error en espanol

Sin Ollama la app funciona igual con el banco fijo de ejercicios.

Modelos recomendados (rapidos): `llama3.2`, `qwen2.5-coder:3b`, `phi3:mini`.
