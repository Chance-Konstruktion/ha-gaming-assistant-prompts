🎮 Gaming Assistant - Prompt Packs

The Intelligence Layer for the Home Assistant Gaming Assistant.

This repository contains AI-validated prompt packs following the Justine Standard v4.2 — a strict four-phase workflow ensuring production-ready quality for digital and physical games.
🧠 The Justine Engine

Every pack is architected by Justine, a screen-aware AI agent running on the OpenClaw architecture. Justine operates using a specialized cognitive framework designed for real-time game analysis.
Workflow v4.2 Execution:

    Phase 1: Research Cache — External validation via web sources (min. 3 sources).

    Phase 2: JSON Generation — Creation of 4 synchronized JSONs (base, cheats, secrets, completion).

    Phase 4: Validation & Expansion — Cross-checking data and expanding the system_prompt to a target density of 350-450 words.

    Phase 5: Zero-Waste Delivery — Final validation via python3 -m json.tool.

The Justine Chain-of-Thought:
Step	Function
ERKENNEN	Parse HUD/UI elements: health bars, minimap, quest markers, heat levels.
KATEGORISIEREN	Classify: Combat, Stealth, Exploration, Boss, or Dialog.
ANALYSIEREN	Cross-reference game mechanics with visible player state.
EMPFEHLEN	Deliver pixel-to-action mapping: "Press X now because Y is visible on screen."
📂 Directory Structure

Modular 4-pack system designed for precision and performance:
Folder	Purpose	Example
packs/base/	Core tactics, screen-aware coaching, physical strategies.	chess.json, cyberpunk_2077.json
packs/cheats/	Console commands, trainers, exploits (PC-only).	cyberpunk_2077_cheats.json
packs/secrets/	Easter eggs, cameos, mysteries, hidden content.	hollow_knight_secrets.json
packs/completion/	100% guides, missables, ending routes, collectibles.	elden_ring_completion.json
🃏 Special Focus: Physical Board & Card Games

This project uniquely supports physical gameplay. These packs use "platforms": ["Physical"] and focus on rule interpretation, setup optimization, and probability-based strategy.

    Example (Chess): The assistant analyzes a board photo, identifies the opening, evaluates material balance, and suggests the best move according to FIDE principles.

🛠 Justine Standard v4.2 Requirements
Universal Platforming

One JSON per game—never split by platform.

    Video games: "platforms": ["PC", "PS5", "PS4", "Xbox Series X|S", "Switch"]

    Physical games: "platforms": ["Physical"]

    Strict rule: No hardware-specific filenames (e.g., no ps5_game.json).

Naming Conventions

    Pattern: {game_id}_{type}.json (Note: base has no suffix).

    Game ID: Lowercase, snake_case (e.g., hollow_knight, elden_ring).

    Example: ✅ hades_cheats.json | ⚠️ Hades Cheats.json (Invalid)

Pre-Commit Validation Checklist

Before submitting, run these checks locally:
Bash

# 1. Validate JSON Structure
python3 -m json.tool file.json > /dev/null && echo "✅ JSON Valid"

# 2. Check Word Count (Target: 350-450)
python3 -c "import json; w=len(json.load(open('file.json'))['system_prompt'].split()); print(f'Words: {w}'); assert 350 <= w <= 450"

🤝 Contributing
Option A: Direct PR

    Copy template from packs/_template.json.

    Research your game (min. 3 sources).

    Generate the 4 JSONs following the schema.

    Validate locally (JSON + word count).

    Submit PR with context sources listed.

Option B: Request Justine Generation

Comment on an issue with the following format:

    Game: [Full Name]

    Platforms: [List]

    Needs: [e.g., "Ending guide", "All easter eggs"]

Justine will automatically create the research cache, generate the packs, and submit a PR.
🛡 Spoiler Levels
Level	Behavior
none	No story spoilers, mechanics only.
low	Vague location hints ("check the eastern district").
medium	Standard: Conditional spoilers ("this choice locks ending X").
high	Full disclosure, speedrun-optimized.
📜 License

MIT License — free to use, modify, and distribute.

Maintained by the OpenClaw Architecture. All packs validated via Justine Engine v4.2.
