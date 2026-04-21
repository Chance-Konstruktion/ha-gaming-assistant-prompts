# 🎮 Gaming Assistant – Prompt Packs

[Deutsche Version](./README.md)

The **intelligence layer** for the Home Assistant [Gaming Assistant](https://github.com/Chance-Konstruktion/ha-gaming-assistant).

This repository contains AI-validated prompt packs following the **Justine Standard v4.2**.

---

## 🧠 Justine Engine

Each pack is built by **Justine**: a screen-aware AI agent on the OpenClaw architecture for real-time gameplay analysis.

### Workflow v4.2

1. **Phase 1 – Research Cache**
   * External validation using web sources (minimum 3 sources).
2. **Phase 2 – JSON Generation**
   * Build 4 synchronized JSONs: `base`, `cheats`, `secrets`, `completion`.
3. **Phase 4 – Validation & Expansion**
   * Cross-check data and expand `system_prompt` to 350–450 words.
4. **Phase 5 – Zero-Waste Delivery**
   * Final validation via `python3 -m json.tool`.

### Justine Chain-of-Thought

| Step | Function |
|---|---|
| **DETECT** | Parse HUD/UI elements: health bars, minimap, quest markers, heat levels |
| **CATEGORIZE** | Classify into combat, stealth, exploration, boss, or dialog |
| **ANALYZE** | Cross-reference mechanics with visible player state |
| **RECOMMEND** | Deliver pixel-to-action mapping (“Press X now because Y is visible.”) |

---

## 📂 Directory Structure

| Folder | Purpose | Example |
|---|---|---|
| `packs/base/` | Core tactics, screen-aware coaching, physical-game strategies | `chess.json`, `cyberpunk_2077.json` |
| `packs/cheats/` | Console commands, trainers, exploits (PC-only) | `cyberpunk_2077_cheats.json` |
| `packs/secrets/` | Easter eggs, cameos, hidden content | `hollow_knight_secrets.json` |
| `packs/completion/` | 100% guides, missables, ending routes, collectibles | `elden_ring_completion.json` |

---

## 🧾 Naming Convention (standardized)

**Single naming standard for all files:**

* lowercase only
* `snake_case`
* no platform prefixes in filenames (e.g., no `pc_`)
* no mixed variants such as `UNO_cheats` vs `uno_cheats`

### Schema

* **Base:** `{game_id}.json`
* **Typed packs:** `{game_id}_{type}.json`

Examples:

* ✅ `counter_strike_2.json`
* ✅ `dota_2.json`
* ✅ `uno_cheats.json`
* ✅ `dead_island_secrets.json`
* ⚠️ `pc_counter_strike2.json` (legacy)
* ⚠️ `UNO_cheats.json` (legacy)

---

## 🃏 Physical Board & Card Games Support

These packs use `"platforms": ["Physical"]` and focus on rule interpretation, setup optimization, and probability-based strategy.

**Example (Chess):**
From a board photo, the assistant identifies the opening, evaluates material balance, and recommends the best move based on FIDE principles.

---

## ✅ Pre-Commit Checks

```bash
# 0) Pack validator (naming required, strict recommended)
python3 scripts/validate_packs.py
python3 scripts/validate_packs.py --strict

# 1) Validate JSON
python3 -m json.tool file.json > /dev/null && echo "✅ JSON Valid"

# 2) Check word count (target: 350-450)
python3 -c "import json; w=len(json.load(open('file.json'))['system_prompt'].split()); print(f'Words: {w}'); assert 350 <= w <= 450"
```

---

Contribution guide: [CONTRIBUTING.md](./CONTRIBUTING.md)

## 🤝 Contributing

### Option A: Direct PR

1. Copy the template from `packs/_template.json`.
2. Research your game (minimum 3 sources).
3. Generate the 4 JSON files according to schema.
4. Validate locally (JSON + word count).
5. Open a PR and list your research sources.

### Option B: Request Justine Generation

Use this issue-comment format:

* `Game: [Full Name]`
* `Platforms: [List]`
* `Needs: [e.g. "Ending guide", "All easter eggs"]`

Justine will then generate the research cache, prompt packs, and PR.

---

## 🛡 Spoiler Levels

| Level | Behavior |
|---|---|
| `none` | No story spoilers, mechanics only |
| `low` | Vague hints (“check the eastern district”) |
| `medium` | Conditional spoilers (“this choice locks ending X”) |
| `high` | Full disclosure, speedrun-optimized |

---

## 📜 License

MIT License — free to use, modify, and distribute.

Maintained by OpenClaw Architecture. All packs validated via Justine Engine v4.2.
