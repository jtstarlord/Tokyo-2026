# Trip-app mechanics (Paris-2026 pattern, reused for Tokyo-2026)

The trip app is a single self-contained `index.html`: markup + CSS + one `<script>` holding a
global `TRIP` object and render functions. All ingest edits are data edits to `TRIP` (plus the
occasional stale string elsewhere in the file). No browser storage, no build step. The file also
contains smaller script blocks (version stamps) — always select the block containing
`const TRIP` when validating.

## TRIP shape (the parts ingest touches)

- `TRIP.days[]` — each day: `{date, dayNum, label, sub, theme, sub2, location, special, note, hotel, sections:[{time, entries:[…]}]}`
- `entries[]` fields: `title, addr, metro, walk, tags[], lat, lng, note` plus optional
  `tips` (HTML string shown in the expanded card: `<b>Label:</b> text<br>` lines),
  `dir` (from-hotel directions, eats tab only), and the **state fields**:
  - `bk:"<substring>"` — links the entry to the `TRIP.bookings[]` item whose `.text` contains
    the substring. **Must match exactly one item** — check with a quick find before choosing.
  - `lock:"7:30 PM"` — display time; entry renders as booked/navy when its bk item is
    `done:true` (or unconditionally if no bk).
  - `wl:"8:00 PM"` — pending/waitlist state (slate ⏳) while the bk item is `done:false`;
    flips to lock automatically when the item is marked done.
  - `pend:"~9:15 PM"` / `alert` tag — needs-booking (amber ⚠).
  - The At-a-Glance page, its overview map, and the day cards all derive from these — set the
    fields once and every surface updates.
- `TRIP.bookings[]` — `{text, sub, done}` checklist. Wording conventions from practice:
  `CONFIRMED <ref> · <price> · <party> · cancel terms · phone` for done items;
  `REQUESTED via <platform> — awaiting confirmation email; if quiet, call <phone>` for pending;
  `⚠` prefix for action items (exchanges, cancellations to perform).
- `TRIP.contacts[]` — `{name, num}`.
- `TRIP.eats[]` — the Restaurant Ideas tab; if a booked venue appears here, update its `res`
  string to reflect the booking.

## Conventions

- En-dashes in date ranges (`Sep 6–10`), `→` arrows in transit titles, times as `7:30 PM`
  (or `13:41` for rail). Titles: `Venue — what it is ★ 7:30 PM`; put the *name* first when the
  glance label matters (glance truncates at ` — ` when the first segment is ≥13 chars, and
  strips embedded times).
- `glanceTitle()` strips `★` and times — don't rely on titles to carry state.
- Interactive state (checkboxes, notes) is in-memory only by design; permanent status changes
  are edits to the data (`done:true` in the source, not just a ticked box).

## Edit mechanics

Entries are one line each in the source. The reliable pattern (used dozens of times):

```python
m = re.search(r'^\s*\{title:"<escaped title>".*$', html, re.M)
old = m.group(0); trailing = ',' if old.rstrip().endswith(',') else ''
html = html.replace(old, new_line + trailing)
```

Watch the trailing comma — a doubled comma once shipped a broken page. Never end a replacement
line with `,` yourself; let the `trailing` logic supply it.

## Validate → deploy → verify

```bash
# 1. validate (BEFORE any commit)
python3 - <<'PY'
import re
html = open('index.html').read()
main = [s for s in re.findall(r'<script>(.*?)</script>', html, re.S) if 'const TRIP' in s][0]
open('/tmp/check.js','w').write(main)
PY
node --check /tmp/check.js
# 2. sanity: eval TRIP, print affected day + bookings counts (node -e with the regex
#    /const TRIP = ([\s\S]*?)\n};/ then eval('('+m[1]+'\n})'))
# 3. deploy
git add index.html && git commit -m "..." && git push origin main
# 4. verify with a marker UNIQUE to the new content (e.g. the confirmation code)
curl -s "https://<live-url>/?cb=$(perl -e 'print time')" | grep -c "<unique marker>"
# poll every 10s; Pages rebuilds in ~40-60s. Old-content markers prove nothing.
```

## Judgment notes from real ingests

- SNCF: exchange/refund free until D-7, €19/ticket after; "outbound at 19:38" style times are
  easy to misread as intended — always check arrival time against rental-desk hours (Avignon
  TGV desks close ~21:00–22:00) and hotel check-in rules.
- Zenchef restaurants: three distinct email types (confirmed via card hold / request awaiting
  confirmation / waitlist inscription). Card holds charge in full on no-show; deadlines vary
  wildly (4 AM day-of, 3 PM day-of, 4:45 PM day-of, 7:30 PM the *evening before*) — normalize
  and flag the strict ones.
- Tours with hard entry cutoffs (Paris Muse: no entry 30+ min late, no refund) deserve an
  arrive-by line in tips and a bags/security note.
- A guided visit makes the self-guided version of the same sight redundant — remove it, and
  sweep for references to it elsewhere.
- When a booking replaces a dropped plan, keep the cancellation visible as a completed
  checklist line ("cancelled Aug 28, no charge") — it answers "did we ever cancel X?" weeks
  later on the ground.
