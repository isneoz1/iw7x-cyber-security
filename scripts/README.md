# Maintenance scripts

One-off, idempotent helpers used to build and maintain `catalog.json` and the
site. They have already been applied — you normally don't need to re-run them.
Each is safe to re-run (upgrades in place, never duplicates).

| Script | Purpose |
|--------|---------|
| `curate_flagships.py` | Curate the core flagship tools with correct, Kali-ready install/run commands. |
| `curate_more.py` | Second batch of flagship command curation. |
| `curate_essentials.py` … `curate_essentials5.py` | Successive waves that verify well-known tools and fix their commands to be Kali-ready. |
| `curate_thin.py` | Fill the smaller categories (AI/ML, ICS, Satellite, Game Hacking, VoIP, DDoS) with real tools. |
| `dedup_catalog.py` | Remove near-duplicate tools (keeps the best copy); guarantees zero duplicates. |
| `recategorize.py` | Add missing categories and route tools into the right one (dry-run by default; `--save` to apply). |
| `expand_arsenal.py` | Older category-expansion helper. |
| `sync_site_counts.py` | Regenerate the site's category grid counts from `catalog.json`. Run after the catalog grows. |
| `make_preview.py` | Render the real TUI header to `assets/iw7x-preview.svg` (README hero image). |
| `make_og_image.py` | Generate the Open Graph / social-card image (`docs/og-image.png`). |

## Typical flow after adding tools/sources

```bash
python3 neoz.py --update          # or let a curate_*.py add tools
python scripts/dedup_catalog.py   # ensure no duplicates
python scripts/sync_site_counts.py  # refresh the public site grid
```

The single source of truth is always `catalog.json`; the engine (`neoz/`) reads
it directly. Adding a tool never needs a script — one JSON entry is enough.
