# Contributing

Thanks for contributing to the Gaming Assistant prompt packs.

## Quick Start

1. Copy `packs/_template.json`.
2. Create your pack files in `packs/base`, `packs/cheats`, `packs/secrets`, and `packs/completion`.
3. Follow naming rules:
   - lowercase only
   - snake_case
   - no platform prefixes (`pc_`, `ps5_`, etc.)
4. Validate locally before opening a PR.

## Local Validation

```bash
# naming check (required)
python3 scripts/validate_packs.py

# strict check (recommended)
python3 scripts/validate_packs.py --strict
```

## Prompt Quality

Recommended checks for each generated file:

```bash
python3 -m json.tool file.json > /dev/null && echo "✅ JSON Valid"
python3 -c "import json; w=len(json.load(open('file.json'))['system_prompt'].split()); print(f'Words: {w}'); assert 350 <= w <= 450"
```

## Pull Request Checklist

- [ ] Naming convention followed
- [ ] Validation script executed
- [ ] Sources documented in PR description
- [ ] New/updated packs explain platform support clearly
