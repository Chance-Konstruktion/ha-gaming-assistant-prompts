🎮 Gaming Assistant - Prompt Packs

The Intelligence Layer for the Home Assistant Gaming Assistant.

This repository contains community-maintained and AI-generated prompt packs. These packs are the "brain" behind the ha-gaming-assistant, providing deep-dive knowledge for digital and physical games.
🧠 The "Justine" Engine

Most of the data in this repository is architected and validated by Justine, a specialized AI agent. Justine follows a strict cognitive framework to ensure that every prompt pack is not just a collection of data, but a high-level coaching tool.
The "Justine" Skill-Logic:

Every pack generated follows a four-step Chain-of-Thought process:

    ERKENNEN (Recognize): Identifies the current game state via HUD, UI, or camera entities.

    KATEGORISIEREN (Categorize): Sorts information into mechanics, lore, secrets, or tactical advice.

    ANALYSIEREN (Analyze): Cross-references data with the 1.4m+ token context window.

    EMPFEHLEN (Recommend): Delivers a concise, actionable output (approx. 400 words) to the user.

📂 Directory Structure

We use a modular 4-pack system to keep the integration lightweight and the advice precise.
Folder	Purpose	Example
packs/base/	General strategy, tactics, and physical game rules.	the_witcher_3.json, chess.json
packs/cheats/	Console commands, trainers, and mechanical exploits.	cyberpunk_2077_cheats.json
packs/secrets/	Easter eggs, hidden items, and lore-mysteries.	hollow_knight_secrets.json
packs/completion/	100% guides, trophy hunting, and checklist logic.	elden_ring_completion.json
🛠 Standard Workflow (v4.2)

To maintain the highest quality, every entry must follow the Justine Standard:

    Universal Platforming: One JSON for all platforms (PC, Console). For board games, use "platforms": ["Physical"].

    Depth-First Research: Data is validated against external sources before being committed.

    Zero-Waste JSON: Clean structure, no trailing commas, lowercase IDs, and snake_case naming conventions.

🤝 Contributing

Want to add a game? You can either submit a manual PR or use the Justine Template:
1. The Template

Copy packs/_template.json and ensure your system_prompt follows the coaching-expert persona:
JSON

{
  "id": "game_id",
  "name": "Game Name",
  "platforms": ["PC", "PS5", "Xbox", "Physical"],
  "keywords": ["game name", "alias"],
  "system_prompt": "You are a professional coach for [Game]. Use the ERKENNEN-ANALYSIEREN-EMPFEHLEN logic...",
  "spoiler_defaults": {
    "story": "none",
    "mechanics": "high"
  }
}

2. Naming & Validation

    Files must be named game_id.json.

    Suffixes: _cheats, _secrets, _completion (except for base).

    Physical Games: Focus on rules, setup-optimization, and probability-based tactics.

🛡 Spoiler Levels

We respect the player's experience. Every pack supports granular spoiler controls:

    none: No spoilers.

    low: Vague hints only.

    medium: Moderate detail.

    high: Full technical disclosure.

📜 License

This project is licensed under the MIT License. Feel free to use, modify, and distribute these packs to build a better gaming future.

Generated and maintained with the support of Justine (OpenClaw Architecture).
