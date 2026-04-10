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

## Available Games

See the [`packs/`](packs/) directory for all available prompt packs.

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

### 2. Naming Convention

- File name: `your_game_id.json` (lowercase, underscores)
- Variant packs use suffixes: `your_game_id_cheats.json`, `your_game_id_secrets.json`, `your_game_id_completion.json`

### 3. Pack Types

| Suffix | Purpose |
|--------|---------|
| *(base)* | General coaching and tips |
| `_cheats` | Cheat codes and exploits |
| `_secrets` | Hidden content and easter eggs |
| `_completion` | 100% completion guides |

### 4. Submit a Pull Request

1. Fork this repository
2. Add your pack to the `packs/` directory
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
