# 🎮 KeyMaster Pro - Python Mastery

**Aplicación gamificada para memorizar y mecanizar la construcción de código en Python**

## 🌟 Características Principales

### 📚 Modos de Juego

1. **Modo Entrenamiento**
   - Práctica libre con XP y niveles
   - Dificultad adaptativa basada en tu nivel
   - Sin penalización por errores
   - Sistema de combos con multiplicador de XP

2. **Modo Aprendizaje**
   - Rutas estructuradas de aprendizaje de Python
   - 11 categorías: Fundamentos, Estructuras de Datos, Control de Flujo, Funciones, POO, etc.
   - Seguimiento de progreso por concepto
   - Pistas contextuales para cada desafío

3. **Modo Supervivencia**
   - 3 vidas para sobrevivir
   - Dificultad creciente automática
   - Sistema de combos para puntuación extra
   - Récords guardados

4. **Desafíos Diarios**
   - 3 desafíos únicos cada día
   - Bonus de XP por completarlos
   - Sistema de racha diaria

### 🎯 Sistema de Gamificación

#### 💎 Sistema de Progresión
- **Niveles**: Desde Novato (LVL 1) hasta AI Singularity (LVL 100+)
- **Rangos**: 🐣 Novato → 📜 Scripter → 💻 Coder → 🔧 Developer → 🎯 Senior Dev → 🚀 Tech Lead → 🧙 Architect → 👑 Guru → 🌟 Legend → 🤖 AI Singularity
- **XP**: Gana experiencia con cada desafío completado
- **Combos**: Encadena desafíos perfectos para multiplicadores de XP

#### 🏆 Sistema de Logros (25 logros)
- **Velocidad**: Alcanza 30, 50, 80, 100 WPM
- **Nivel**: Llega a nivel 5, 10, 20, 50
- **Precisión**: Completa 10, 50, 100 desafíos perfectos
- **Supervivencia**: Sobrevive a 10, 50 desafíos y alcanza 500 puntos
- **Combos**: Alcanza combo x10, x25, x50
- **Práctica**: Completa 100, 500, 1000 desafíos totales
- **Maestría Python**: Domina diferentes conceptos de Python

#### ⚡ Power-ups
- **💡 Pista** (3 usos): Muestra ayuda contextual para el desafío actual
- **⏭️ Saltar** (2 usos): Salta un desafío sin penalización
- Gana más power-ups al subir de nivel (cada 5 niveles)

#### 🔥 Sistema de Combos
- Encadena desafíos perfectos (sin errores) para aumentar tu combo
- Combo x5+: Obtén multiplicador de XP (10% por combo)
- El combo se reinicia al cometer errores
- Indicador visual cuando el combo está activo

### 📊 Estadísticas Detalladas

El sistema trackea:
- WPM más rápido alcanzado
- Precisión de tipeo (%)
- Total de desafíos completados
- Desafíos perfectos
- Mejor puntuación en Supervivencia
- Combo más alto alcanzado
- Racha de desafíos diarios
- Conceptos de Python dominados
- Logros desbloqueados

### 🎨 Rutas de Aprendizaje

11 rutas estructuradas con 100+ desafíos de Python:

1. **Fundamentos** (basics)
   - Variables y tipos de datos
   - Operaciones básicas
   - Print y output

2. **Estructuras de Datos** (data_structures)
   - Listas y operaciones
   - Diccionarios
   - Sets y tuplas

3. **Control de Flujo** (control_flow)
   - Condicionales (if/else)
   - Bucles (for/while)
   - List comprehensions

4. **Funciones** (functions)
   - Definición de funciones
   - Parámetros y argumentos
   - Lambda functions

5. **Programación Orientada a Objetos** (oop)
   - Clases y objetos
   - Herencia
   - Decoradores

6. **Módulos e Imports** (modules)
   - Import de módulos
   - Estructura de paquetes
   - Main guard

7. **Archivos I/O** (file_io)
   - Lectura de archivos
   - Escritura de archivos
   - Context managers

8. **Manejo de Excepciones** (exceptions)
   - Try/except/finally
   - Raise exceptions
   - Custom exceptions

9. **Conceptos Avanzados** (advanced)
   - Decoradores personalizados
   - Context managers
   - Async/await
   - Unpacking

10. **Biblioteca Estándar** (stdlib)
    - datetime
    - collections
    - json
    - random

11. **Buenas Prácticas** (best_practices)
    - Documentación
    - Comments
    - Assertions
    - Debug

## 🚀 Instalación y Ejecución

### Requisitos
```bash
Python 3.8+
customtkinter
pygame (opcional, para audio)
Pillow (para mostrar el banner)
```

### Instalación
```bash
# Activar entorno virtual
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependencias (si no están instaladas)
pip install customtkinter pygame pillow
```

### Ejecución
```bash
python keymaster.py
```

## 📁 Estructura del Proyecto

```
Aegis_Keymaster/
├── keymaster.py              # Aplicación principal
├── sound_engine.py           # Motor de audio procedural
├── profile_manager.py        # Sistema de perfil y progresión
├── content_generator.py      # Generador de desafíos y ejercicios
├── achievements.py           # Sistema de logros
├── tips_system.py            # Sistema de notas educativas "Sabías que..."
├── splash_screen.py          # Pantalla de bienvenida con banner
├── assets/
│   └── banner.png            # Banner cyberpunk "Master the Digital Realm"
├── keymaster_profile.json    # Datos del perfil (generado automáticamente)
└── README.md                 # Este archivo
```

## 🎮 Cómo Jugar

### Controles

**Modos Entrenamiento, Aprendizaje, Supervivencia, Diario:**
- **Escribir**: Tipea el código exactamente como aparece
- **Enter**: Saltar desafío (gratis en Entrenamiento, cuesta vida en Supervivencia)
- **Escape**: Saltar desafío
- **💡**: Usar power-up de pista
- **⏭️**: Usar power-up de saltar

**Modo Constructor de Código:**
- **Escribir**: Escribe código con múltiples líneas
- **Enter**: Nueva línea (NO cambia de ejercicio)
- **Ctrl+Enter**: Verificar código completo
- **Shift+Enter**: Nueva línea alternativa

### Consejos
1. **Empieza en Modo Entrenamiento** para familiarizarte sin presión
2. **Usa el Modo Aprendizaje** para dominar conceptos específicos de Python
3. **Practica sin errores** para mantener combos y ganar más XP
4. **Completa Desafíos Diarios** para mantener tu racha y ganar bonus
5. **Usa Power-ups estratégicamente** en Modo Supervivencia
6. **Observa los conceptos** que se repiten para mejorar tu memoria muscular

## 🎯 Objetivos de Aprendizaje

Esta aplicación está diseñada para ayudarte a:

1. **Memorizar** sintaxis común de Python a través de repetición
2. **Mecanizar** patrones de código mediante práctica constante
3. **Desarrollar memoria muscular** para construcciones frecuentes
4. **Mejorar velocidad de tipeo** de código
5. **Aprender conceptos** de manera estructurada y progresiva

## 📈 Sistema de Progresión

### Niveles y XP
- XP necesaria = Nivel × 100
- Ejemplo: Nivel 5 requiere 500 XP total
- Gana XP por cada desafío completado
- XP base = 10 + longitud del código
- XP con combo = base × multiplicador de combo

### Dificultad Adaptativa
- **Modo Entrenamiento**: Dificultad = Nivel ÷ 2 (máx 10)
- **Modo Aprendizaje**: Dificultad = 2 + (Nivel ÷ 3) (máx 8)
- **Modo Supervivencia**: Aumenta cada 5 desafíos completados

## 🔊 Audio

El juego incluye efectos de sonido procedurales:
- ✅ Click satisfactorio en tecla correcta
- ❌ Buzz en error
- 🎵 Melodía ascendente en level up
- 💔 Sonido descendente en game over
- 🏆 Fanfarria en logro desbloqueado
- 🔥 Hit rápido en combo
- ⚡ Sonido de power-up

## 🎨 Interfaz

- **Tema oscuro** para reducir fatiga visual
- **Colores codificados** para feedback inmediato:
  - 🟢 Verde: Correcto
  - 🔴 Rojo: Error
  - 🔵 Azul: Información
  - 🟡 Dorado: Logros y bonus
  - 🟠 Naranja: Power-ups
- **Fuentes monoespaciadas** (JetBrains Mono) para código
- **Indicadores visuales** de progreso y estado

## 💾 Datos Guardados

Todo tu progreso se guarda automáticamente en `keymaster_profile.json`:
- Nivel y XP
- Estadísticas de juego
- Logros desbloqueados
- Conceptos dominados
- Mejor puntuación
- Racha diaria
- Power-ups disponibles

## 🔄 Mejoras Futuras Posibles

- [ ] Modo multijugador / competitivo
- [ ] Tablas de clasificación
- [ ] Más rutas de aprendizaje (Django, FastAPI, etc.)
- [ ] Personalización de temas visuales
- [ ] Modo de práctica con errores comunes
- [ ] Integración con GitHub para snippets reales
- [ ] Estadísticas gráficas de progreso
- [ ] Exportar progreso y estadísticas

## 📝 Notas de Desarrollo

### Arquitectura Modular
El código ha sido refactorizado en módulos para mejor mantenibilidad:

- **sound_engine.py**: Generación procedural de audio
- **profile_manager.py**: Gestión de datos del jugador
- **content_generator.py**: Banco de desafíos organizados
- **achievements.py**: Sistema completo de logros
- **keymaster.py**: Interfaz gráfica y lógica de juego

### Extensibilidad
Es fácil agregar:
- Nuevos desafíos en `content_generator.py`
- Nuevos logros en `achievements.py`
- Nuevos power-ups en `profile_manager.py`
- Nuevos modos de juego en `keymaster.py`

## 📜 Licencia

Este proyecto es de código abierto. Siéntete libre de modificarlo y mejorarlo.

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Ideas para contribuir:
- Agregar más desafíos de Python
- Nuevos logros
- Mejoras en la UI
- Optimizaciones de rendimiento
- Corrección de bugs

---

**¡Disfruta mejorando tus habilidades de Python! 🐍💻🚀**