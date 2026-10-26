# Tokyo 2026 — project knowledge

James Plath's business trip to Tokyo, **Sat Dec 12 – Sat Dec 19, 2026**. Solo. Three full work
days (Tue–Thu) of AI training sessions and 1:1s for the Japan partners and associates — what and
how to sell, and how delivery changes with AI — bracketed by an arrival Sunday, an acclimation
Monday, a flex Friday and a free Saturday morning before a 5:35 PM departure.

This repo is the trip app, built from the Paris-2026 template: a single self-contained
`index.html` (markup + CSS + one `<script>` holding a global `TRIP` object), plus
`site.webmanifest` and `apple-touch-icon.png` for the home-screen install. Pushing to `main`
deploys via GitHub Pages. One phone uses it on the ground — treat it as a live operational
document.

## How to work on this repo

- **Booking confirmations** (flight receipts, hotel confirmations, restaurant bookings from the
  concierge, teamLab tickets): use the `booking-ingest` skill in `.claude/skills/booking-ingest/`.
  The workflow is unchanged from Paris — extract, diff against the plan, apply, validate, deploy,
  report.
- **Data model and deploy pipeline**: `.claude/skills/booking-ingest/references/trip-app.md`.
- **The one hard rule**: `node --check` on the extracted `<script>` block before every push. A
  syntax error ships a blank page.
- **Storage keys** are `tokyo2026.mem.v1`, `tokyo2026.wx.v2`, `tokyo2026.extra.v1` — distinct
  from the Paris keys so both apps can live on the same phone.
- **Single rater.** `RATERS = [{k:'j', name:'James'}]` near `starRow()`. The data model still
  carries `r:{j,b}` so the Paris tooling works unchanged; `b` is simply never set. Add a second
  rater by appending to `RATERS`.
- **Weather** is Open-Meteo with `timezone=Asia%2FTokyo`, Fahrenheit. Section labels that map
  to forecast windows: EARLY MORNING, MORNING, AFTERNOON, EVENING, DEPARTURE. Other labels (the
  "IN THE AIR" section on Dec 13) get no strip, by design.
- **Parts are hardwired** to indices: 0–2 day parts, 3 Bookings, 4 Shopping, 5 Restaurant Ideas,
  6 Contacts, 7 At a Glance. The three day parts are Arrival & Acclimation (days 0–1), Work Week
  (2–4), Wind-down & Home (5–6). Keep exactly three day parts or patch `renderLeft`.
- **Shopping locations** are `tsukiji`, `ginza`, `hnd`, `hotel` (the last means "pack before
  departure"); the filter bar is Tsukiji / Ginza / Airport. Categories keep the Paris keys; the
  `antiques` key is labelled "Kitchen, Craft & Paper".
- **Rating dimension sets**: `flightNight`, `flightDay`, `hotel`, `restaurant` (Drink, Counter &
  room, Sense of place), `table` (team dinners — Host-worthy?), `spa` (new: Therapist, Room &
  quiet, Effect next morning, Value, Would I rebook?), `transit`, `bikeshare`.
- **Writing style** in replies and card copy: no "honest" qualifier tic, no contrastive negation
  ("not X, but Y"), no two-word punch sentences, no "that changes everything" framing. Say the
  thing directly.
- Interactive checkboxes are in-memory by design; permanent status changes are edits to the data.
  Trip memories (`MEM`) buffer to `localStorage` as a crash buffer only — committed values in
  `TRIP` (`entry.r`, `entry.dr`, `entry.imp`, `entry.at`, `entry.cost`, `day.dayR`, `day.dayImp`)
  are the record. Field order when committing: `r, dr, cost, at, imp`; day fields `dayR, dayImp`
  go before `dayNum`.

## The shape of the trip

| Day | Date | Theme | Fixed points |
|---|---|---|---|
| 1 | Sun Dec 13 | Boston → Tokyo | Sat DL1748 BOS→DTW 9:05 First (2D); DL275 DTW→HND 2:05 PM Delta One; land 5:45 PM; EDITION check-in; bed by 22:00 |
| 2 | Mon Dec 14 | Acclimation | Tsukiji 7:30; Hamarikyu matcha; rest to 14:00; scout the office walk + Atago steps; Spa 15:00; teamLab 17:00; Azabudai dinner |
| 3 | Tue Dec 15 | Work day 1 | Sessions 9:30–17:30; team dinner yakitori (Birdland / Torishige) |
| 4 | Wed Dec 16 | Work day 2 | Sessions; crab in a private room (Kani Doraku) |
| 5 | Thu Dec 17 | Work day 3 | Last sessions; sushi (Kyubey); spa or in-room shiatsu late |
| 6 | Fri Dec 18 | Work morning, free afternoon | Sessions to 12:30; Ginza lunch sushi 13:30; Itoya hour; massage 17:00; Hikiniku to Come Shibuya 19:00 |
| 7 | Sat Dec 19 | Home | Tsukiji round two 7:30; check-out 12:00 (14:00 asked); taxi 13:15; Ariso Sushi T3 4F landside 14:00; DL274 HND 5:35 PM → DTW 3:35 PM → DL1707 → BOS 8:51 PM |

## Open questions (as of Oct 25, 2026)

1. **DL1707 on Dec 19** carries a schedule-change flag that James should accept in My Trips.
2. **Hotel confirmation** — rate, room category, Marriott confirmation number.
3. **Office reception floor and badge routine** at Atago Green Hills MORI Tower, from the Japan
   team.
4. **Hikiniku to Come Shibuya's street address** goes on the Friday card once the TableCheck or
   Advance Priority Ticket confirmation is ingested.

Resolved Oct 25: the office is **2-5-1 Atago (Atago Green Hills MORI Tower)**, and **Friday Dec 18
is a work morning with the afternoon free**. Resolved Oct 26: the Delta receipt (conf **HSI4WS**,
eTicket 0067566409871) — DL1748 BOS 9:05 AM → DTW 11:29; DL275 DTW 2:05 PM → HND 5:45 PM +1;
DL274 HND 5:35 PM → DTW 3:35 PM; DL1707 DTW 6:52 PM → BOS 8:51 PM. The return is DL274, not the
DL276 the first build assumed. Seats (from James, Oct 26): 2D, 7A, 3D, 2D.

## Decisions already made

- **One hotel, six nights, no train commute.** The EDITION Toranomon is a 10-minute walk from the
  office and 5 minutes from teamLab at Azabudai Hills. Transit is taxis to Ginza (10–12 min) and
  the Hibiya line from Kamiyacho when he wants it.
- **Monday is built around jet lag, not against it.** The 5 AM wake goes to Tsukiji (which is
  open Mondays; many stalls close Sunday and Wednesday). The 11:00–14:00 window is guarded rest
  with a 90-minute nap cap. Evening is short (teamLab, casual dinner, bed by 22:00).
- **Team dinners are the Japan team's call.** The three cards (yakitori Tue, crab Wed, sushi Thu)
  are James's asks and the fallbacks if the hosts do not pick. If a partner insists on hosting,
  accept and let that card become the backup. The private-room crab night is deliberately the
  mid-week one for the full group.
- **Massage: legitimate venues only.** The Spa on EDITION 31F and licensed in-room shiatsu
  through the concierge, with Hotel Okura's spa as the overflow. James asked about soaplands and
  delivery-health services; those are sex-industry services and are not sourced here. The guide
  carries two massage slots (Mon 15:00, Thu/Fri evening).
- **Sushi tiering.** Kyubey is the booked-for-certain reliable room; Yoshitake and Kanesaka are
  splurge options only if James says so this week (1–2 month lead); Ginza Iwa is the lunch value
  play for Friday or Saturday.
- **No day trips.** Kamakura, Nikko and Hakone were not considered — a work week with one open
  afternoon does not support them.
- **Yakitori ladder, best first:** Birdland Ginza (phone, 6 weeks) → Yakitori Imai (online from
  abroad, the surest great one) → Torishige Shimbashi (concierge) → Kushiwakamaru Nakameguro
  (walk-in clipboard). Torishiki is off the table: December seats were released Oct 1. Hold
  Birdland and Imai in parallel and release one.
- **Hikiniku to Come is Friday night** (Shibuya branch, reservation-only). The Advance Priority
  Ticket on the official site is the safe route; TableCheck opens the following week on Fridays
  at 9:00 JST. Fallback is yakitori under the Yurakucho tracks.
- **7-Eleven is a card, not a footnote** — Sunday evening after check-in, with the Seven Bank ATM
  as the week's cash machine.
- **Saturday lunch is at Haneda:** Ariso Sushi, T3 4F Edo Koji, landside, open 24 h. Listings
  disagree on whether it still has a conveyor belt; it reads as tablet-ordered counter service.
  Ganso Sushi on T2 3F is the true belt, reachable by the free shuttle at the cost of Sky Club time.

## How James travels — carried over from Paris & Provence (Sep 2026)

These are the observed patterns from ten rated days in France. They drove the Tokyo choices
and should drive any edits.

- **Experiential, outdoor, guided, physical → 5s.** The Lime e-bikes, the Seine cruise, the
  Luberon drives, the market mornings and the one guided tour all scored 5. teamLab, Tsukiji on
  foot and the Atago steps are the Tokyo equivalents.
- **Curated retail and reputation rooms → 1s and 2s.** "I am not a shopping guy." Merci, the
  concept stores and the famous-for-being-famous rooms underperformed. Hence named targets only
  (Itoya, Ippodo, the knife shop) with a one-hour cap, and a Shopping tab that is mostly gifts.
- **Rest beats a scheduled park.** The Wednesday midday rest and the empty Saturday afternoon
  were the best-rated non-events of the trip. Monday's guarded window and Friday's light
  afternoon follow that.
- **Churches 2/5 and 3/5.** Meiji Jingu is on Friday as a forest walk with a shrine at the end,
  flagged skippable.
- **Wine 5/5 correlated with the best nights.** Drink quality is a rating dimension on every
  restaurant and team-dinner card (sake and beer here).
- **Flights.** Westbound day flight in Comfort+ scored 5s; the eastbound redeye scored Sleep
  2/5. The Delta One suite is the fix; the DL275 card carries an explicit sleep plan and the
  `flightNight` dims (Seat, Cabin, Sleep, Crew, Food, Worth the suite?). Rate both legs.
- **Flex fares and cancel-the-table-last.** Three train changes in one Provence day taught the
  rule: settle transport first, then the dinner table. Applies to any Friday/Saturday reshuffle.
- **Arrival-day hotel scores are provisional.** Rate the EDITION on Tuesday, then again on
  Saturday with all six dimensions.
- **Room beats hotel.** Ask for the Tokyo Tower side, high up, at check-in.
- **Impressions are his words.** Transcribe verbatim into `imp`; a time in the impression beats
  the arrival stamp; absence in the log means unrated; half-point ratings round up and say so.
- **Business-trip framing (new).** Mornings are for notes, not sightseeing. Lunch is the hosts'.
  Nightcaps are one drink. The log entry each night is the one thing that must happen.

## Gotchas worth remembering

- Tsukiji Outer Market: many stalls close Sunday and Wednesday; best 7:00–10:30; cash-first.
- Hikiniku to Come Shibuya takes no walk-ins; Kichijoji takes no online bookings (same-day ticket
  at 9:00, closed Wed). Prices and fees in third-party listings drift; trust the official site.
- Birdland Ginza is phone-only, ~6 weeks out, closed Sun/Mon — the first concierge call.
- Kani Doraku Ginza Hacchome: 10 private rooms, parties to 28, +81 3 3572 7272; the address
  block number differs between listings (8-7 vs 8-9 Ginza) — it is on Ginza Nine Bldg 2, 2F by
  Shimbashi subway exit 1.
- teamLab Borderless sells out by date; December has closure days — check before buying.
- EDITION check-out is 12:00; late check-out is on request only. Blue Room breakfast 7:00–10:30.
- Delta Sky Club HND is on T3 5F, entry within 3 hours of departure.
- Visit Japan Web is optional and free; no visa or JESTA for a US passport in Dec 2026 (JESTA is
  slated for 2028).
- Tokyo is UTC+9: 14 hours ahead of Boston in December.
- The live site, when it exists, is not reachable from the cloud sandbox — verify deploys through
  the GitHub Actions "pages build and deployment" run, not the URL.
