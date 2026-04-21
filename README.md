# 🎮 Gaming Assistant – Prompt Packs

[English version](./README.en.md)

Der **Intelligence Layer** für den Home Assistant [Gaming Assistant](https://github.com/Chance-Konstruktion/ha-gaming-assistant).

Dieses Repository enthält AI-validierte Prompt-Packs nach dem **Justine Standard v4.2**.

---

## 🧠 Justine Engine

Jeder Pack wird von **Justine** aufgebaut: ein screen-aware AI-Agent auf der OpenClaw-Architektur für Echtzeit-Spielanalyse.

### Workflow v4.2

1. **Phase 1 – Research Cache**
   * Externe Validierung über Webquellen (mindestens 3 Quellen).
2. **Phase 2 – JSON Generation**
   * Erstellung von 4 synchronisierten JSONs: `base`, `cheats`, `secrets`, `completion`.
3. **Phase 4 – Validation & Expansion**
   * Gegenprüfung der Daten + Ausbau des `system_prompt` auf 350–450 Wörter.
4. **Phase 5 – Zero-Waste Delivery**
   * Finaler Check mit `python3 -m json.tool`.

### Justine Chain-of-Thought

| Schritt | Funktion |
|---|---|
| **ERKENNEN** | HUD/UI-Elemente parsen: Health Bars, Minimap, Quest Marker, Heat Levels |
| **KATEGORISIEREN** | Einordnung in Combat, Stealth, Exploration, Boss oder Dialog |
| **ANALYSIEREN** | Spielmechaniken mit sichtbarem Spielerzustand abgleichen |
| **EMPFEHLEN** | Pixel-zu-Aktion-Mapping liefern („Drücke X jetzt, weil Y sichtbar ist.“) |

---

## 📂 Ordnerstruktur

| Ordner | Zweck | Beispiel |
|---|---|---|
| `packs/base/` | Core-Taktiken, screen-aware Coaching, physische Strategien | `chess.json`, `cyberpunk_2077.json` |
| `packs/cheats/` | Console Commands, Trainer, Exploits (PC-only) | `cyberpunk_2077_cheats.json` |
| `packs/secrets/` | Easter Eggs, Cameos, Hidden Content | `hollow_knight_secrets.json` |
| `packs/completion/` | 100%-Guides, Missables, Endings, Collectibles | `elden_ring_completion.json` |

---

## 🧾 Naming-Konvention (vereinheitlicht)

**Einheitlicher Standard für alle Dateien:**

* nur `lowercase`
* `snake_case`
* keine Plattform-Präfixe im Dateinamen (z. B. kein `pc_`)
* keine gemischten Varianten wie `UNO_cheats` vs `uno_cheats`

### Schema

* **Base:** `{game_id}.json`
* **Typed Packs:** `{game_id}_{type}.json`

Beispiele:

* ✅ `counter_strike_2.json`
* ✅ `dota_2.json`
* ✅ `uno_cheats.json`
* ✅ `dead_island_secrets.json`
* ⚠️ `pc_counter_strike2.json` (alt)
* ⚠️ `UNO_cheats.json` (alt)

---

## 🃏 Fokus: Physical Board & Card Games

Diese Packs nutzen `"platforms": ["Physical"]` und fokussieren sich auf Regeln, Setup-Optimierung und Wahrscheinlichkeitsstrategie.

**Beispiel (Chess):**
Aus einem Brettfoto erkennt der Assistent die Eröffnung, bewertet Materialbalance und empfiehlt den besten Zug nach FIDE-Prinzipien.

---

## ✅ Pre-Commit Checks

```bash
# 1) JSON validieren
python3 -m json.tool file.json > /dev/null && echo "✅ JSON Valid"

# 2) Wortanzahl prüfen (Ziel: 350-450)
python3 -c "import json; w=len(json.load(open('file.json'))['system_prompt'].split()); print(f'Words: {w}'); assert 350 <= w <= 450"
```

---

## 🤝 Contributing

### Option A: Direkter PR

1. Template aus `packs/_template.json` kopieren.
2. Spiel recherchieren (mind. 3 Quellen).
3. 4 JSONs gemäß Schema erzeugen.
4. Lokal validieren (JSON + Wortanzahl).
5. PR mit Quellenkontext einreichen.

### Option B: Justine-Generierung anfragen

Issue-Kommentarformat:

* `Game: [Full Name]`
* `Platforms: [List]`
* `Needs: [z. B. "Ending guide", "All easter eggs"]`

Dann erstellt Justine automatisch Research Cache, Packs und PR.

---

## 🛡 Spoiler-Level

| Level | Verhalten |
|---|---|
| `none` | Keine Story-Spoiler, nur Mechanik |
| `low` | Vage Hinweise („prüfe den östlichen Distrikt“) |
| `medium` | Standard: bedingte Spoiler („diese Entscheidung sperrt Ending X“) |
| `high` | Volle Offenlegung, speedrun-optimiert |

---

## 📜 License

MIT License — frei nutzbar, veränderbar und verteilbar.

Maintained by OpenClaw Architecture. Alle Packs validiert via Justine Engine v4.2.
