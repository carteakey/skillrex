# Gloam pet resume handoff

## Resume point

Resume at **Hatch Pet Gate 3: regenerate the cardinal anchors, then regenerate look rows 9 and 10**.

Do **not** regenerate the base or standard animation rows 0–8. They are approved and preserved in this checkpoint. Do **not** install the current 8×11 candidate: its strict blind QA failed the hard horizontal-cardinal gate.

The shortest safe dependency path is:

1. regenerate and independently verify the four cardinals;
2. regenerate coherent look row 9 and pass its immediate registration/semantic gates;
3. regenerate coherent look row 10 using approved row 9 for scale and wrap continuity;
4. assemble a temporary v2 PNG and rerun blind, labeled, continuity, and final visual QA;
5. only after those gates pass, run the single final despill, encode WebP, validate v2, package, and install Gloam.

## Start a new chat with this

```text
Use $hatch-pet, $imagegen, and Assethetic's hatch-pet-fastpath skill. Read handoffs/gloam/README.md completely and resume Gloam from its preserved checkpoint. Rows 0–8 are approved; do not regenerate them. Start by regenerating and independently verifying the four cardinal anchors, then regenerate coherent look rows 9 and 10. Keep image generation quota-aware: one bounded job at a time and stop immediately at a failed dependency gate. Do not install unless strict blind cardinal QA, labeled semantics, continuity review, final visual QA, despill, and v2 validation all pass.
```

If the new chat is opened outside this repository, give it the absolute handoff path:

```text
/Users/kchauhan/repos/assethetic/handoffs/gloam/README.md
```

## Preserved passing checkpoint

The checkpoint is self-contained for resuming from the v2 look stage:

- `checkpoint/spritesheet-standard.png` and `.webp`: approved `1536×1872` intermediate atlas containing rows 0–8. This is the base atlas for extended assembly, not a packageable v2 pet.
- `checkpoint/review-standard.json`: standard rows pass deterministic frame inspection with no errors or warnings.
- `checkpoint/contact-sheet-standard.png`: approved visual reference for scale, identity, palette, and standard motion.
- `checkpoint/canonical-base.png`: Gloam identity reference.
- `checkpoint/idle-neutral.png`: neutral cell used for look-row registration, target scale, lower-body anchor, and baseline.
- `checkpoint/look-mechanics.md`: the current direction mechanics decision.
- `checkpoint/layout-guides/`: four-cardinal and look-row guides.
- `checkpoint/pet_request.json`: pet id, description, chroma key, dimensions, and row contract.

The original full debug run is still available at:

```text
/Users/kchauhan/Documents/Codex/2026-07-22/hatch-pet-users-kchauhan-codex-skills/work/gloam-ps2-pet-run
```

Prefer the clean checkpoint above. Use the original run only when deeper attempt history is useful.

## What is already good

- Pet id: `gloam`
- Display name: `Gloam`
- Description: `A grim low-poly night hunter rendered like a forgotten PS2 survival-horror character.`
- Visual mode: low-poly late-PS2 gothic survival-horror humanoid, not cute, plush, anime, glossy, painterly, or flat 2D pixel art.
- Rows 0–8: generated, extracted, assembled, visually reviewed, and deterministically approved.
- Standard atlas: `1536×1872`, eight columns by nine rows, `192×208` cells.
- Identity, palette, materials, silhouette, standard motion, and neutral-cell geometry are stable.
- Gloam is **not installed** at `~/.codex/pets/gloam`.

## Why the current look rows are rejected

The final candidate passed source separation, registration, body lock, wrap scale, deterministic despill, and `1536×2288` v2 atlas validation. It still failed a non-overridable semantic gate:

- strict majority blind QA classified source `270` as screen-right instead of screen-left;
- strict majority blind QA classified source `090` as screen-left instead of screen-right.

That is a hard cardinal failure. It cannot be waived, relabeled, reordered, mirrored, or locally patched.

See:

- `evidence/current-blocker.json`
- `evidence/blind-validation-failed.json`
- `evidence/rejected-look-directions.png`
- `evidence/rejected-look-anchors.png`

Files under `evidence/` are diagnostic only. In particular, `rejected-look-anchors.png` must not be reused as approved direction grounding.

## Regeneration contract

### 1. Rebuild the cardinal basis first

Generate one coherent four-pose strip in this exact order:

```text
000 up, 090 screen-right, 180 down, 270 screen-left
```

Use viewer/image coordinates. At normal pet size, verify the visible lens, mask plane, or other chosen aiming landmark without relying on labels:

- `090`: the readable aiming cue must sit or point unmistakably toward the image's screen-right side;
- `270`: the readable aiming cue must sit or point unmistakably toward the image's screen-left side;
- `000`: unmistakably up;
- `180`: unmistakably down.

Keep boots, pelvis, centered belts, lower coat, torso, and baseline front-facing and registered. Do not create a whole-body turntable. The current mechanics favor the single pale lens as the horizontal cue because head/brim perspective repeatedly caused left/right sign confusion. If that cue is not independently readable at `192×208`, change the cardinal pose-family strategy before generating either look row.

Have a fresh isolated visual worker verify all four anchors at final pet size. Stop here if either horizontal cardinal is wrong or ambiguous.

### 2. Regenerate row 9 as one coherent strip

Exact order:

```text
000, 022.5, 045, 067.5, 090, 112.5, 135, 157.5
```

Ground it in the newly approved cardinal strip, canonical base, standard contact sheet, and row-9 guide. Copy the selected output into `decoded/look-row-9.png`, then immediately run deterministic registration, final-cell edge checks, labeled direction semantics, and continuity review. Do not start row 10 until row 9 clears every hard gate.

### 3. Regenerate row 10 as one coherent strip

Exact order:

```text
180, 202.5, 225, 247.5, 270, 292.5, 315, 337.5
```

Use the newly approved cardinals and completed row 9. Row 10 must match row 9's raw body envelope, planted baseline, center, and full-width frontal body family. `337.5` must land one smooth step before row 9's `000`. Do not narrow into side-profile bodies or rotate the torso.

Immediately run the row-10 final-cell edge, semantics, identity, body-lock, and cross-row wrap checks.

### 4. Final QA and installation

After both complete generated rows pass their immediate gates:

1. assemble a temporary transparent `1536×2288` PNG;
2. create the labeled direction sheet, randomized blind-pair sheet, and continuity report;
3. run three fresh isolated blind reviewers who see only the blind sheet;
4. require hard cardinal consensus: `000 up`, `090 screen-right`, `180 down`, `270 screen-left`;
5. run independent final contact-sheet QA;
6. resolve every major failure before proceeding;
7. run the single final chroma despill;
8. encode lossless WebP and validate with `--require-v2`;
9. package `pet.json` with `spriteVersionNumber: 2` and install only then.

## Quota and tooling gotchas from this run

- The built-in image generator accepts at most five referenced images. A six-reference request was rejected before rendering. Keep each row job at five or fewer image references; text files do not count as attached images.
- A good row-10 reference set is exactly five images: canonical base, standard contact sheet, approved cardinal strip, completed row 9, and the row-10 layout guide.
- Do not ask the image model for exact percentage resizing or exact pixel dimensions as a repair strategy. Those attempts oscillated between undersize wrap pops and edge overflow.
- Do not locally scale, mirror, reorder, relabel, tile, or patch final look cells. Regenerate the complete containing eight-pose row.
- Do not trust a labeled reviewer alone for horizontal cardinals. The previous labeled gate passed while isolated blind majority caught the actual reversal.
- Validate cardinals before paying for row 9, validate row 9 before paying for row 10, and run blind cardinal QA before final despill/WebP work.
- Preserve the successful standard atlas. The only required visual regeneration is the cardinal basis plus coherent rows 9 and 10.

## Completion condition

The handoff is complete only when Gloam has:

- an approved `1536×2288` 8×11 atlas;
- all 16 directions in fixed clockwise order;
- strict blind cardinal validation with `ok: true`;
- labeled per-direction semantics with no hard failure;
- reviewed continuity with no visible snap, reversal, or scale pop;
- one successful final despill and v2 validation;
- `~/.codex/pets/gloam/pet.json` and `spritesheet.webp` installed together.
