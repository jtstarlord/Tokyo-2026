---
name: booking-ingest
description: Ingest travel booking confirmations — restaurant reservations (Zenchef, TheFork, Reserve with Google), trains (SNCF), flights, hotels, rental cars (Hertz/Avis/etc.), tours, museum tickets, cruises — from PDFs, forwarded emails, or screenshots, extract every decision-relevant fact (date/time, party, status, confirmation code, price/holds, cancellation deadline, meeting point, contacts), diff it against the live trip itinerary, and apply it to the trip dashboard (entry + bookings checklist + contacts + glance state) with validation and deploy. Use this whenever James attaches or mentions a booking/reservation confirmation, says "booked X, see attached", "can you add this to the itinerary", "made a reservation", forwards a confirmation/exchange/cancellation/waitlist email, or asks to update the trip site from any booking document — even if he doesn't say "ingest". Also for booking STATUS changes: exchanges, cancellations, waitlist notices, "awaiting confirmation" emails.
---

# Booking Ingest — the confirmation email is the ground truth

This skill captures a workflow refined across ~15 real bookings for the Paris/Provence 2026
trip. Its costly near-misses were all the same species: **the document said something the plan
didn't expect, and the interesting work was noticing.** A TGV "booked as planned" turned out to
depart 19:38 — after the rental desks close, stranding the whole Provence arrival. A "Septime
waitlist" was for Monday, not the Sunday the itinerary assumed. An Orsay booking arrived for
Wednesday when Orsay anchored Tuesday — and rebuilding two days was the actual task. A Zenchef
"reservation request awaiting confirmation" is *not* a reservation. Read the document as the
authority — over the itinerary, and over the user's own message when they differ — and treat
every mismatch as the headline, not a footnote.

## Current trip (edit this block when the trip changes)

- App file: `index.html` at the root of this repo (all data in the `TRIP` object). In local
  sessions the clone lives at `~/Documents/Claude/Projects/Tokyo-2026/`; in cloud sessions
  (claude.ai/code) work in the session's clone — same file, same workflow.
- Live site: `https://jtstarlord.github.io/Tokyo-2026/` once the repo exists (GitHub Pages from
  `main`, rebuild ~60s; commit + push IS the deploy). Single rater (James); see CLAUDE.md.
- Data model + deploy mechanics: read `references/trip-app.md` before editing.

## Step 1 — Extract

Run the bundled extractor on the attachment:

```bash
python3 <skill-dir>/scripts/extract_pdf.py "<path to pdf>"
```

It prints all pages' text. Confirmation PDFs are usually Gmail print-outs: the payload page is
often page 2–3, wrapped in legal boilerplate — read past the headers. For screenshots, read the
image directly; for pasted text, use it as-is. If extraction yields nothing useful, say so and
ask for a screenshot rather than guessing.

## Step 2 — The booking sheet

Assemble every decision-relevant fact. The set that has mattered in practice:

- **Vendor / venue** and booking **type** (restaurant, train, flight, hotel, car, tour, cruise, museum, event, insurance)
- **Date, time, duration/end time** — copy from the document, then sanity-check the weekday matches the date
- **Party** (names, count), **status** — one of: `confirmed` / `requested — awaiting vendor confirmation` / `waitlist` / `exchanged` / `cancelled`. Zenchef sends distinct emails for each; the "awaiting confirmation" one says so explicitly.
- **Reference / confirmation code**, order numbers, barcode numbers, e-ticket location (app, wallet, email)
- **Money**: price paid, card hold / imprint / deposit, exchange fees
- **Cancellation policy, normalized to an absolute deadline** ("free until Sep 7, 7:30 PM"). Flag anything stricter than day-of — deadlines the evening before, 72-hour tiers, non-refundable — prominently: these are the facts that cost money when forgotten.
- **Logistics**: address, phone, email, meeting point (quote it exactly — "under the central arch, back to the pyramid"), arrive-by time, late-arrival rules, luggage/bag rules, dress notes.

## Step 3 — Diff against the plan (this is the real work)

Before writing anything, load the current `TRIP` data and compare:

- Does the **date/day/time** match where the plan expects this item? If it lands on a different
  day than assumed, say so first and plan the restructure.
- Does it **collide** with anything booked or planned that day (including travel time between
  locations)? Check what's before and after; compute realistic transit.
- Does it make anything **redundant** (a guided tour replacing a self-guided visit) or
  **impossible** (an evening arrival vs. a rental-desk closing time, a dinner vs. a cruise)?
- Does the arrival/end time still work with **fixed downstream constraints** (check-in windows,
  vendor opening hours, next morning's departure)?

Then choose the path:

- **Contained** (fits its slot, moves nothing else): apply directly — the user attaching a
  confirmation with "add this" is the instruction.
- **Structural** (forces changes to other entries or other days): apply the booking itself
  faithfully, propose the restructure in the same breath, and carry it out — but if the
  restructure would *discard* something the user chose (not merely reshuffle it), present the
  conflict and let them decide.
- **Broken** (the booking as ticketed doesn't work — wrong time, impossible connection): still
  record it truthfully as booked, add a prominent ⚠ action item to fix it (note free-change
  deadlines — SNCF is free until D-7), and lead the reply with the problem. Never quietly
  "fix" the itinerary around a booking the user probably wants to change instead.

## Step 4 — Apply

Full mechanics in `references/trip-app.md`. The checklist that keeps the app coherent:

1. **Day entry**: title carries venue + time; `bk` links it to its checklist item (substring
   must match that item's text uniquely); state via `lock` (confirmed, shows time),
   `wl` (waitlist / awaiting confirmation), or the item's done-flag. Tips carry the
   confirmation details, cancellation deadline, and getting-there/away logistics; note stays
   narrative.
2. **Bookings checklist item**: CONFIRMED/REQUESTED/WAITLIST wording, reference code, price,
   cancellation deadline, phone. `done:true` only for genuinely confirmed.
3. **Contacts**: add new vendor phone numbers worth having on the ground.
4. **Stale-reference sweep**: grep the whole file for the venue name and for whatever plan this
   booking replaces — day notes, other entries' tips, header subtitles, and the eats tab all
   accumulate forward-references. A booking that changes the plan usually invalidates prose in
   two or three other places.
5. If a booking **removes** a plan (cancellation, replacement): log the cancellation as a
   checklist line (with "no charge" or what it cost) rather than deleting history the user may
   need.

## Step 5 — Validate BEFORE pushing, deploy, verify

A syntax error here once shipped a blank page to the live site because validation ran chained
with the push. Order matters:

1. Extract the main `<script>` (the one containing `const TRIP`) → `node --check`.
2. Eval the `TRIP` literal and print the affected day's sections + booking counts — eyeball
   that the structure is what you intended.
3. Only then commit and push.
4. Poll the live URL until a string **unique to the new content** appears (a confirmation code
   works well). A marker that already existed in the old version proves nothing.

## Step 6 — Report

Lead with what's now locked and its time. Then: the cancellation deadline if it's unusual, any
conflicts found and how they were resolved, the confirmed-count, and the remaining
needs-booking radar so the user always knows what's still open. If the booking created a new
user action (cancel the old place, await a vendor email, exchange a ticket), make it an
explicit checklist item AND say it in the reply — items on a list get forgotten; sentences
with deadlines don't.
