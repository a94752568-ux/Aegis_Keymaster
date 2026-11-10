# Aegis Keymaster

**Professional Touch Typing Tutor for Lubuntu**  
Inspired by TypingMaster 11 · Built with PySide6 · Cyberpunk Neon UI

Aegis Keymaster is a modern, adaptive touch-typing trainer designed for Linux (Lubuntu 26.04+).  
It combines structured lessons, intelligent review of weak keys, real-time statistics, and a premium Cyberpunk visual experience with neon glow, pulse effects, and fluid animations.

## Core Features

- **Adaptive Lessons** — Start from the home row and progressively unlock the full keyboard. Lessons adapt to your speed and accuracy.
- **Weak Key Detection** — Automatically identifies difficult keys and generates targeted drills.
- **Typing Tests** — Measure WPM, accuracy, and consistency. Detailed post-test reports.
- **Virtual Keyboard** — Real-time finger guidance and key highlighting.
- **Progress Tracking** — Graphs, statistics, and session history.
- **Light / Dark / Neon modes** — Full theme support with high-quality neon glow and pulse animations.
- **Fully Responsive** — Adapts cleanly to any screen size and resolution.
- **Linux-first** — Optimized for Lubuntu / Ubuntu desktop environments.

## Visual Style

Cyberpunk aesthetic with:
- Deep space backgrounds
- Electric cyan & magenta neon accents
- Soft pulse animations on interactive elements
- Glow effects on active keys and focus states
- Premium, fluid transitions

## Requirements

- Python 3.10+
- Lubuntu 26.04 (or any modern Linux with Qt support)
- PySide6

```bash
pip install -r requirements.txt
```

## Run

```bash
python -m src.main
# or
python src/main.py
```

## Project Structure

```
Aegis_Keymaster/
├── src/
│   ├── main.py                 # Entry point
│   ├── app.py                  # Application class
│   ├── ui/
│   │   ├── main_window.py
│   │   ├── typing_area.py
│   │   ├── virtual_keyboard.py
│   │   ├── themes.py
│   │   └── widgets/
│   ├── core/
│   │   ├── engine.py           # Typing engine (WPM, accuracy, errors)
│   │   ├── lessons.py
│   │   └── stats.py
│   └── utils/
├── styles/                     # QSS / theme resources
├── data/                       # Lessons, user profiles
├── assets/
├── resources/
├── STATE.md
└── requirements.txt
```

## Development Status

See `STATE.md` for current progress and next steps.

---

*Aegis Keymaster — Type with precision. Glow with style.*
