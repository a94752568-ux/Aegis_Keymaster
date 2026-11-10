# STATE.md — Aegis Keymaster (TypingMaster 11 Concept)

**Last updated:** 2026-11-10T14:35:00Z

## Goal
Completely redesign Aegis_Keymaster as a professional touch-typing tutor inspired by TypingMaster 11, built with PySide6 for Lubuntu 26.04. Features light/dark modes, fully responsive UI, Cyberpunk aesthetic (neon glow, pulse, premium animations).

## Done
- Theme system (Light / Dark / Neon) + responsive MainWindow + NeonFrame pulse/glow
- Core Typing Engine (live WPM, accuracy, per-char state)
- Virtual Keyboard with finger legend + neon highlight
- Structured Lesson System (15 progressive lessons + unlock + pass criteria)
- **Weak-key tracking** (`src/core/weak_keys.py`):
  - Per-key attempts / errors / error rate
  - `weak_keys(top_n)` ranked by error rate
  - Adaptive drill generator weighted toward weakest keys
  - Neighbor expansion for more natural practice text
- MainWindow integration:
  - Records every completed exercise into the tracker
  - "Review Weak Keys" button → generates focused drill
  - Live summary line ("Weak: 'e' (40%), 'r' (35%)…")
  - Virtual keyboard marks weak keys with amber border
  - Review mode flag (does not affect lesson pass state)

## Pending (prioritized)
1. Formal timed test mode (1 / 3 / 5 min) + detailed report screen
2. Progress persistence (save LessonManager + WeakKeyTracker to JSON)
3. Sound feedback
4. Optional hand diagram for finger guidance
5. Archive old CustomTkinter modules

## Decisions
- Weak keys require a minimum number of attempts (default 2–3) before appearing, to avoid noise
- Review drills do not count toward lesson pass/fail
- Keyboard shows weak keys with a subtle amber border when not actively highlighted
- Drill generator mixes high-error keys with keyboard neighbors for realistic sequences

## Next step
Implement formal timed test mode (user chooses 1 / 3 / 5 minutes) with a results/report screen showing WPM, accuracy, errors, weak keys from that test, and option to start a review drill.
