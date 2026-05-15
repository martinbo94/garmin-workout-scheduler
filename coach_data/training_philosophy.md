# Training Philosophy

The framework the coach reasons within. Drawn from Marius Bakken's
Norwegian threshold method, adapted for amateur volume (the Norwegian
Singles variant — single sub-threshold sessions every other day rather
than the elite double-threshold day). This file is **strategic** — how
to think about training. It changes rarely, only when the methodology
itself shifts.

This doc is intentionally generic — no personal HR numbers, paces, or
test data live here. For your specific bpm bands, easy run cap, target
paces, and current calibrations, see **`coach://user_profile`**. For *where
you are right now* (goal race, block phase, weekly schedule), see your
`plan.json`.

---

## The core principle

> "Intensity must be precise enough to be tolerated and repeated. You do
> not improve by training as hard as possible. You improve by training
> hard enough, often enough, for long enough."
> — Bakken

The whole framework follows from this. Most coaching mistakes come from
crossing the line where training stops building you up and starts
breaking you down. The signature Bakken move is to **stay just under that
line, repeatedly**, week after week. Repeatability is the goal; any
session that costs too much undoes the next one.

This implies an inversion of conventional advice:
- Threshold work is the **engine**, not a sprinkle on top of easy mileage.
- Threshold intensity is **lower** than most people run it.
- Easy is **truly easy** — no productive middle ground between easy and
  threshold.
- VO2max work is **supplemental**, not central to distance development.

---

## "Threshold" vs "threshold work" — terminology trap

These get conflated all the time, so be explicit. Bakken himself flags
this directly in *Løping!* (chapter on Den gylne sonen):

> *"Når jeg bruker ordet terskeltrening her, mener jeg i praksis trening
> opp til, men ikke for mye rett på eller over terskelen."*
> — Bakken
> (When I use the word "threshold training" here, I mean in practice
> training up to, but not too much directly at or over the threshold.)

- **Threshold (LT2 / MLSS / OBLA) ≈ 4.0 mmol/L lactate.** Both
  conventional sports science and Bakken agree on this. A fixed
  physiological landmark — the highest steady-state effort before lactate
  accumulates uncontrollably. The 4.0 number itself is a pedagogical
  simplification standardized since the 1970s.
- **"Threshold work" — the session — means different things to different
  coaches.** This is where the confusion lives.
  - Conventional plans: "threshold work" = sessions *at* ~4 mmol (one
    hard session per week, costs a lot of recovery).
  - Bakken: "threshold work" = sessions *below* threshold, at ~2.3-3.0
    mmol with individual variation 2.0-3.5 mmol ("Den gylne sonen" — the
    Golden Zone). Lower per-session stimulus but much higher repeatable
    weekly volume.

Bakken doesn't redefine threshold — he just deliberately trains under it.
The trade is net-positive over weeks: at-threshold once a week vs
sub-threshold 2-3× a week is much higher weekly stimulus with less
recovery cost per session.

**We're training under Bakken's framework**, so when this doc or the
plan.json says "threshold session" or "terskelintervaller," that means
**sub-threshold in the Golden Zone (2.3-3.0 mmol / 80-87% max HR)**, not
at-threshold at 4 mmol.

### The Golden Zone vs other zones — Bakken's figur 1.2

Direct comparison from the book:

| | Rolig | Grå sone | **Den gylne sonen** | Høyintensitet |
|---|---|---|---|---|
| **Talk test** | Can speak freely | Whole sentences | **3-5 words per breath** | Single words |
| **% max HR** | < 70% | 70 – 80% | **80 – 87%** | > 90% |
| **Lactate** | Low | Limited | **2-3 mmol/L** | Accumulates |
| **Training effect** | Low | Limited | **High ✓** | High |
| **Muscular load** | Low ✓ | Moderate | **Moderate ✓** | High |
| **Recovery time** | Short ✓ | Medium | **Medium ✓** | Long |
| **OK for frequent training** | Yes ✓ | No | **Yes ✓** | No |

The point of the table: the gray zone (70-80% max HR, where many runners
default) has limited training effect AND moderate cost — worst of both
worlds. The Golden Zone has high training effect at a recoverable cost.
That's why Bakken says **"Du øker via volumet, ikke intensiteten"** —
you progress by accumulating more time in this zone, not by going harder.

### Deriving your sub-threshold band

Two rules, which should converge:

1. **From a lactate test** (most precise): interpolate where 2.3 and 3.0
   mmol fall on your HR curve. Those bpm values are your sub-threshold
   band's lower and upper bounds.
2. **Without a test** (approximation): **80 – 87% of max HR**.

Add a hard cap a few bpm below your classical LT2 (≈ 91-93% of max HR or
the 4 mmol point on a test) to leave buffer for HR lag. Above that cap
you've slipped into at-threshold territory.

Your specific bpm band lives in **`coach://user_profile`** under "Quality
session HR targets." Look it up before any threshold workout.

### Same HR target regardless of rep length

The whole point of Bakken's short reps (45/15, 30/15) is to hit a *higher
pace* at the *same sub-threshold HR/lactate*, not to push HR higher. The
short rests let you maintain lactate control while running faster. Rep
length is a pace lever, not an intensity lever.

| Session type | Target HR | What changes vs long reps |
|---|---|---|
| **Long reps** (5×6 min, 4×8 min, 5×1k) | sub-threshold band (see user_profile) | Default. 2× per week. |
| **Short reps** (45/15, 30/15, 400-1000m) | same sub-threshold band | Pace faster because of short rests. |
| **VO2 / X element** (1× per 7-10 days, when fresh) | ~92-96% of max HR | Separate stimulus, only when rested. |

**Subjective feel** for sub-threshold work: "controlled, sustainable, I
could keep doing this much longer than I am." Bakken's specific talk
test: **you should be able to get 3-5 words out per breath**. If you can
speak in whole sentences without strain, you're too slow. If you can only
manage single words, you're at-threshold or above — slow down.

If HR drifts above the sub-threshold band's upper bound on later reps:
cut pace, not the session. The target is repeatability across weeks, not
making each session as hard as possible.

The point is *repeatability*, not heroics. A session that wrecks the next
one is a net loss.

---

## Rep-length pace adjustment (within the same HR target)

Same Golden Zone HR target, different paces depending on rep design.
Bakken's specific rule, scaled relative to a runner's standard T-pace:

| Rep length | Pace adjustment |
|---|---|
| Short reps (1-3 min) | T-pace + ~10-25 sec/km — faster end |
| Medium reps (4-8 min) | T-pace + ~25-32 sec/km — the baseline |
| Long reps (8-12 min) | T-pace + ~32-39 sec/km — slower end |

True short reps (45/15, 30/30, etc.) sit at or slightly faster than the
"short reps" line above because the brief work bursts don't accumulate
fatigue the way 1-3 min reps do.

The athlete's actual numbers are in `coach://user_profile` under "Session
pace estimates."

## Session formats

Bakken's three threshold session types, all done as **intervals with
recovery** (not continuous):

| Type | Rep length | Recovery | Lactate target | Notes |
|---|---|---|---|---|
| **Long reps (sustained)** | 6 – 10 min | 60 – 90 s | At or just below 3.0 | Most common; e.g. 5×6 min, 4×8 min, 5×1000 m |
| **Short reps (over/under)** | 45 s – 1 min | 15 – 30 s | At or slightly above threshold | 45/15, 30/15, etc. Higher turnover at same lactate band |
| **Float / progression** | 6 – 10 min | minimal | Build from 2.0 → 3.0 across the set | Slightly faster each rep |

Why intervals beat continuous: short rests let muscle tone reset, keeping
lactate controllable. Bakken's stronger claim (chapter 3, *Løping!*):
**continuous threshold runs are inferior to interval threshold work** at
the same intensity because (a) intervals let you accumulate more total
time at the target HR before hitting the wall, and (b) the brief rests
prevent the slow drift into supra-threshold that ruins a continuous
tempo. The exception is marathon-specific prep — 20-40 min continuous
tempo blocks become useful in the final weeks before a marathon, but
they're an exception, not the default.

### Variation within sub-threshold work

Bakken's third "frame" is to vary *inside* the Golden Zone over a block:

- **Rep length variation:** rotate short (1-3 min), medium (4-8 min),
  long (8-12 min) reps across weeks so the body sees different stimuli at
  the same HR target.
- **Intensity micro-variation:** progress sessions across a block from
  the lower end of the sub-threshold band (~180 bpm) toward the upper
  end (~188 bpm).
- **Recovery variation:** longer rests (90-120s) for the harder end of
  the band, shorter rests (30-45s) for the easier end or for short reps.
- **Terrain variation:** track, road, light trail, hill — same HR target,
  different load profiles.

The point: monotony at sub-threshold intensity is what causes both
plateaus and burnout. Variation keeps adaptation moving without escalating
intensity.

### Smart Strides (optional session-end protocol)

Bakken's protocol for keeping neuromuscular speed sharp without adding
load: after the main set, 2-3 min easy jog, then **5-6 × ~100 m strides
slightly above threshold pace**. Controlled, not sprints. Walk/jog between.
Total cost ~5 min, kept rare on the hardest days. Useful for runners who
otherwise lose top-end feel on a heavy-sub-threshold block.

### Example sessions the user has used or might use

- 5 × 6 min @ sub-threshold HR, 1 min jog rest — classic Bakken long-rep
- 4 × 8 min @ sub-threshold HR, 90 s rest — slightly longer reps
- 10 × 1 km @ sub-threshold pace, 60-90 s jog — high-turnover
- 15 × 3 min @ sub-threshold HR, 30-60 s rest — Bakken's example for
  "increase total dragtid" when threshold feels too easy
- 45/15 × 20-30 min — short on/off at sub-threshold HR, not all-out

### 45/15 deserves a special note

Bakken treats 45/15 as the **single most versatile threshold format**.
Time-efficient (~30 min for a full session), low cognitive load (you don't
have to think about pacing 6-min reps), and unusually easy to recover from
because each work bout is short.

Specific protocol variants from the book:
- **Standard:** 15-20 reps at sub-threshold pace, controlled.
- **Pyramid:** 20 / 25 / 30 / 25 / 20 reps as continuous sets with
  short rest between, or one long block with internal feel-based pacing.
- **Block:** 3 × (10 × 45/15) with 3-5 min easy between blocks.

**Where 45/15 specifically shines:** weeks with limited time, return from
illness or injury (you can do half the reps and still get useful stimulus),
and as a variation lever inside a longer training block to break monotony
on weeks where longer reps feel stale.

**Progression rule** (from HK Lab + Bakken): when threshold feels too
easy, do NOT make it faster. Instead:
- Increase total threshold time (work up to 30-50 min cumulative)
- Lengthen individual reps (4 → 6 → 8 min)
- Shorten recovery (60s → 45s → 30s)

Faster pace at the same HR is what improvement *looks* like. It happens
on its own; don't chase it.

**Within-session progression** (Bakken, "konservativ tilnærming"):
**make every session progressive** — start the first rep at the slow end
of your sub-threshold band, build to the middle by mid-session, and only
push the upper end on the final rep if you're feeling strong.
> *"Det er bedre å avslutte med følelsen av at du kunne gjort mer, enn å
> ha presset deg for hardt i starten, for så å måtte redusere
> intensiteten senere."*

(Better to finish feeling you could have done more than to push too hard
early and need to scale back later.)

---

## VO2max work ("X element")

Bakken treats VO2max as one weekly "X element," not as a primary stimulus:

> "The mechanical benefit you get from running faster on sessions cannot
> be compared to the increase in performance you'll get from optimizing
> the anaerobic threshold."

Where VO2 work fits depends on what's actually limiting performance:

- **If raw VO2max is the limiter** (low VO2max for the volume you train),
  occasional VO2 sessions may matter more in the mix.
- **If utilization rate is the limiter** (you've got plenty of aerobic
  ceiling but can't sustain a high % of it at threshold), more threshold
  work closes that gap better than more VO2 work.
- **If both are reasonable already**, the question is what you've
  *responded* to historically — runners who've done a lot of interval
  work may have less to gain from more of it, vs. runners new to
  high-intensity who might still get fast gains from VO2.

See your test report (if you have one) or your race time vs aerobic
ceiling to judge which camp you're in. Default in this framework: keep
VO2 work modest unless there's a clear reason it's the bottleneck.

**X-element guidelines:**
- 0 – 1 session per week, on a rested day.
- HR target: roughly 92 – 96% of max HR (top of Z5). See
  `coach://user_profile` for your specific band.
- Formats: 4 × 4 min steady, 5 × 3 min, 4 × 6 min 30/15 in hills, or
  shorter (1 – 2 min) high-effort reps.
- Skip it in weeks where two threshold sessions already feel taxing —
  threshold takes priority.

---

## Easy runs

The discipline is non-negotiable: **easy is truly easy**.

> "I would entirely stay away from the zone in between very easy running
> and the threshold."  — Bakken

Bakken's elites run easy below 70% of max HR, but amateur economy makes
that effectively walking pace. Practical interpretation:

- **Aim for average HR in Z1 or low-mid Z2.** Upward drift on long runs
  is normal.
- **Hard cap: LT1** (≈ 84% of max HR untested). Routine drift above LT1
  is the gray zone — too hard to recover from, too easy to drive
  adaptation.
- **Purpose:** aerobic base, economy, recovery — not a moderate workout.

See `coach://user_profile` for your easy-cap bpm. The real signal isn't
the number; it's whether you feel recovered the next morning.

---

## Long runs

In this framework, long runs are aerobic base — **not quality**.

- Run them at easy pace (Z1 / low Z2, same discipline as a regular easy
  run).
- No progression, no surges, no marathon-pace finishes (in this block).
- Duration: typically 90 – 120 min, less if weekly volume is low.
- Frequency: weekly, but can be skipped during heavy threshold blocks.

The deliberate choice not to make long runs "progressive" or "marathon
pace" in this block keeps total quality stress concentrated in the actual
threshold sessions. Long runs build durability without spending the
recovery budget that threshold work needs.

---

## Weekly structure: Norwegian Singles adaptation

The full Bakken method runs **double-threshold days** (two threshold
sessions in one day, ~6-8 h apart) on Tuesdays and Thursdays/Saturdays.
That's elite practice — 4 threshold sessions per week, 150-220 km total.

For amateurs (the Norwegian Singles adaptation that emerged on forums),
the structure preserves the framework but reduces frequency:

- **2-3 threshold sessions per week**, single sessions (not doubles).
- Every other day = a quality day; alternate days = easy.
- Most other runs are truly easy.
- 1 long run weekly (easy pace).
- 0-1 X-element session weekly (VO2max).

### Adjusted intensity distribution for 4-6 hour weekly volume

Bakken's chapter 7 ("Mosjonisten som vil mer") gives concrete targets
specifically for amateurs at this volume — the conventional 80/20 split
is too easy-heavy for this dose. The adjusted distribution:

| Intensity | % of weekly run time | At 5 h/week |
|---|---|---|
| Z1-Z2 (easy / aerobic base) | **60-65%** | ~3-3:15 hours |
| Z3-Z4 (sub-threshold, the Golden Zone) | **20-30%** | ~1:00-1:30 hours |
| Z5 (true high intensity) | **5-10%** | ~20-30 min |

These are the bands Claude should check against when reviewing weekly
summaries. They override the looser "Z1-2: 60-80% / Z3-4: 20-35% / Z5:
0-5%" target in `coach://classification` for athletes at this volume —
the sub-threshold floor is *higher* (20% minimum vs 20%) and the Z5
allowance is *higher* (5-10% vs 0-5%) because amateurs need a slightly
larger quality fraction to drive adaptation than elites do.

### Sample week template (Bakken, 5-hour reference week)

This is the book's concrete chapter 7 layout, lightly adapted:

| Day | Session | Notes |
|---|---|---|
| Mon | **Rest** | Full recovery from weekend training. |
| Tue | **Threshold "støtte" session** | E.g. 6×6 min sub-threshold, or 10×3 min with 1 min jog. Variations in rep length OK; same HR target. |
| Wed | Easy 40-60 min | Truly easy — *"så slakk at den nesten føles feil"*. Hard cap at LT1. |
| Thu | **Threshold "hoved" session** | E.g. 3-4×10 min, or another long-rep variation. Different format than Tuesday. The most balanced session of the week. |
| Fri | **Rest** or short easy | Strategic rest before weekend. Skip if 4 rest days in a row feels off. |
| Sat | **X-økt (flex slot)** | See below — varies week to week. |
| Sun | **Long easy** | 60-120 min depending on block. Distance-specific (longer for HM/marathon goals). |

Two threshold sessions (Tue / Thu) + one flex slot (Sat) + one long
(Sun) is the working structure. Strength training fits as a separate
add-on, typically Mon, Wed or Fri.

### The X-økt — Saturday's flex slot

Bakken calls Saturday the "X-økt" — a flexible third quality slot whose
character changes week to week and across the block:

- **45/15 session** when you want short-rep variation or have less time
- **Hills / strides / Smart Strides** when neuromuscular freshness matters
- **Race-specific work** (closer to race day): mile reps, 6×1k at goal
  pace, or a tune-up effort
- **Extra easy / skipped entirely** in deload weeks or when recovery is
  marginal

The X-økt is *not* a fixed third threshold. Two threshold sessions plus
a third hard session is too much sustained quality for most amateurs.
Treat the X-økt as the variation lever — what you cycle through that
keeps the framework from going stale across a 12-week block.

### Advanced variant: double-threshold days (NOT current default)

**⚠ Gatekept. Default is Norwegian Singles. Don't recommend
double-threshold without explicit user confirmation.**

The elite protocol clusters two sub-threshold sessions into the same day
(6-8 h apart): morning long reps (5×6 min, 4×8 min), evening short reps
(10×1k or 45/15). Both in the Golden Zone — neither at-threshold. Muscle
tone recovers enough between sessions that the second lands on fresh
legs despite partial glycogen depletion, compounding weekly threshold
volume well beyond singles.

Why gatekept: Bakken's reference athletes ran 150-220 km/week with 5+
years of consistent volume. Below ~80 km/week the base isn't there;
recovery infrastructure (sleep, nutrition, lifestyle fit) starts
mattering much more than for singles.

Preconditions before recommending:
- Sustained 70+ km/week (ideally 100+).
- ≥ 8-12 weeks of consistent sub-threshold singles.
- Goal race ≥ 10k (less benefit for pure 5k focus).
- User explicitly wants to try it.

If any fail, stay on Singles. Adopt gradually via Bakken's ramp (see
*Løping!* ch. 7): start with easy+threshold on the same day before any
true double, modulate the first true doubles 10-15 sec/km slower than
normal sub-threshold pace.

**Frequency cap once adopted:** at most 2 double-days per week, with
full easy days between. Bakken calls the format "forførende" — feeling
good every day tempts a third double, which breaks the recovery loop.

---

## Recovery and the "traffic light" check

Bakken used a traffic-light system to decide whether a planned hard
session should go ahead. Adapted for this setup, before each threshold
or VO2 day:

- **🟢 Green:** Low morning resting HR, low warm-up HR, lactate climbs
  easily at fast paces, legs feel responsive → run the session as
  planned, maybe push the upper end of the band.
- **🟡 Yellow:** Normal warm-up HR, normal feel → standard session.
- **🔴 Red:** Elevated resting/warm-up HR, can't drive lactate up despite
  effort, legs heavy → **scale back or skip**. Cut volume by 30-50%,
  lower target HR by 2-3 bpm, OR convert to easy. The next session
  matters more than this one.

Concrete signals to watch (via `morning_check_in` tool):
- **Training readiness** (Garmin) score → low score = consider yellow/red
- **HRV** trending below baseline → yellow/red
- **Resting HR** elevated by 5+ bpm above your typical → yellow/red
- **Sleep** under 6 hrs or poor quality → yellow at minimum
- **Body battery** low at wake → adjust

If two consecutive yellow/red days, skip the planned quality session;
the framework only works if you can repeat sessions.

---

## How to react to a missed or off session

- **Missed entirely** (skipped because of recovery / life): don't try to
  cram it in later in the week. Roll on. Compliance is about the *trend*,
  not single-week perfection.
- **Did but felt off** (HR too high for the pace, couldn't hold target):
  log it, take an extra easy day, drop intensity on the next threshold
  slightly. Don't compensate by making the next session harder.
- **Did and felt great** (under HR target, easy effort): note it, but
  resist the urge to push pace faster. Progress in this method comes from
  *more time at the same controlled effort*, not from squeezing each
  session.

---

## What this framework is NOT

- **Not "polarized 80/20"** — the hard portion is sub-threshold, not
  VO2max. Closer to 70-30 with the 30% being controlled threshold.
- **Not "more easy volume = better"** — at amateur volume, easy km don't
  substitute for threshold quality.
- **Not "long runs as quality"** — pure aerobic base, no fast finishes.
- **Not "harder is better"** — slightly under target HR is often better;
  over target is a problem.

---

## When this file gets out of date

Edit when methodology itself shifts (e.g., away from Bakken). Do NOT
edit for week-level adjustments — those go in `plan.json`.
