# Aegis KeyMaster

Entrenador de Python con modos de tecleo, aprendizaje guiado y constructor de codigo.

## Instalacion

```bash
pip install -r requirements.txt
python keymaster.py
```

## IA local (Ollama) — opcional

1. Instala [Ollama](https://ollama.com)
2. `ollama pull llama3.2` (u otro modelo)
3. Activa **IA local** en la barra superior

### Controles de IA

- **Selector de modelo**: modelos instalados en Ollama
- **Ratio IA (0–100%)**: probabilidad de ejercicio generado vs banco fijo
- **Adaptativo**: prioriza conceptos con mas fallos del perfil

Con adaptativo, el perfil guarda `concept_stats` (intentos, errores, exitos) y alimenta tanto el banco fijo (peso x3) como los prompts de Ollama.

Sin Ollama la app funciona con el banco fijo; el modo adaptativo sigue reforzando conceptos debiles offline.
