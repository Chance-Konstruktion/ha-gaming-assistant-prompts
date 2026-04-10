# Gaming Assistant - Prompt Packs

Community-maintained prompt packs for the [Home Assistant Gaming Assistant](https://github.com/Chance-Konstruktion/ha-gaming-assistant) integration.

## What are Prompt Packs?

Prompt packs are JSON files that provide game-specific AI coaching knowledge. Each pack contains:

- **Keywords** for automatic game detection
- **System prompts** with expert coaching instructions
- **Spoiler defaults** to control hint detail levels
- **State schemas** for real-time game state analysis

## Installation

Prompt packs are **automatically downloaded** by the Gaming Assistant integration. No manual setup required.

The integration fetches the latest packs on startup and caches them locally.

## Directory Structure

```
packs/
├── base/           # General coaching and tips
├── cheats/         # Cheat codes, console commands, exploits
├── secrets/        # Hidden content, easter eggs, collectibles
├── completion/     # 100% completion guides
└── _template.json  # Template for new packs
```

| Folder | Purpose | Example |
|--------|---------|---------|
| `base/` | General game coaching and strategy tips | `elden_ring.json` |
| `cheats/` | Cheat codes, console commands, trainers | `elden_ring_cheats.json` |
| `secrets/` | Hidden content, easter eggs, secret areas | `elden_ring_secrets.json` |
| `completion/` | 100% completion guides, all collectibles | `elden_ring_completion.json` |

## Contributing

Want to add a new game or improve an existing pack? Follow these steps:

### 1. Use the Template

Copy [`packs/_template.json`](packs/_template.json) and fill in your game's details:

```json
{
  "id": "your_game_id",
  "name": "Your Game Name",
  "keywords": ["game name", "alternate name"],
  "system_prompt": "You are an expert coach for Your Game...",
  "spoiler_defaults": {
    "story": "none",
    "items": "medium",
    "enemies": "medium",
    "bosses": "low",
    "locations": "medium",
    "lore": "none",
    "mechanics": "high"
  },
  "additional_context": "Extra context about the game."
}
```

### 2. Place in the Right Folder

- **Base pack** (general coaching): `packs/base/your_game.json`
- **Cheats pack**: `packs/cheats/your_game_cheats.json`
- **Secrets pack**: `packs/secrets/your_game_secrets.json`
- **Completion pack**: `packs/completion/your_game_completion.json`

### 3. Naming Convention

- File name: `your_game_id.json` (lowercase, underscores)
- Use suffixes matching the folder: `_cheats`, `_secrets`, `_completion`

### 4. Submit a Pull Request

1. Fork this repository
2. Add your pack to the correct `packs/` subfolder
3. Validate your JSON (no trailing commas!)
4. Submit a PR with a brief description

## Spoiler Levels

| Level | Description |
|-------|-------------|
| `none` | No spoilers at all |
| `low` | Vague hints only |
| `medium` | Moderate detail |
| `high` | Full information |

## License

MIT License - see [LICENSE](LICENSE) for details.
