---
name: hatch-pet-fastpath
description: Add quota-aware staging, early visual approval, repair routing, and final-QA ordering to Codex v2 animated pet production. Use with hatch-pet when the user wants a fast or low-waste pet workflow, wants to approve a base before full animation, mentions limited image-generation quota, requests a retro low-poly or PS2-style pet, or wants to avoid repeated full-atlas rebuilds.
---

# Hatch Pet Fastpath

Use this skill as a scheduling and convergence addendum to `$hatch-pet`. Load and follow `$hatch-pet` and `$imagegen`; keep Hatch Pet's v2 geometry, animation rows, visual provenance, and acceptance criteria authoritative. Apply the stricter staging and QA order below without weakening any final gate.

## Lock The Production Contract

Before generating, write a compact contract containing:

- `visual_mode`: `2d-pixel`, `low-poly-ps2`, `prerendered-low-res-3d`, or another explicit medium
- `subject`: creature, object, or humanoid; include age/proportion cues
- `silhouette`: the few identity features that must survive at `192x208`
- `mirror_safe`: yes or no, with markings, props, lighting, and handedness evidence
- `palette_and_materials`: stable colors and surface treatment
- `direction_mechanics`: the landmarks that will carry up, down, screen-left, and screen-right
- `avoid`: the user's rejected qualities plus production hazards
- `approval_policy`: explicit checkpoint or pre-authorized completion when every contract check passes

Do not treat “pixelated” as a sufficient mode. Resolve whether it means flat pixel art, low-poly 3D with pixelated textures, or low-resolution pre-rendered 3D. If the user's surrounding language resolves the choice, record it without asking again.

For a retro low-poly gothic humanoid, read [references/ps2-gothic-humanoid.md](references/ps2-gothic-humanoid.md) before preparing prompts.

## Use Three Spend Gates

### Gate 1: Base

Generate exactly one base image. Check the locked medium, proportions, silhouette, full-body framing, chroma background, mirror safety, and avoid list.

- Stop for user approval when the user requested a preview or the result is subjective or borderline.
- Continue without another turn only when the user pre-authorized completion and every contract check clearly passes.
- Reject before row generation if the base is cute, anime, plush, painterly, or otherwise contrary to a severe dark-humanoid contract.

Expected spend: one visual generation.

### Gate 2: Motion Proof

Generate and validate `idle` and `running-right` only. Use them to prove identity retention, scale, spacing, cadence, and directional readability. Decide whether `running-left` can be derived safely.

Do not start the remaining standard rows until both proof rows pass. If either fails, repair that row and re-check instead of opening more generation jobs.

Expected cumulative spend: about three visual generations.

### Gate 3: Full V2

Generate the remaining standard rows, cardinals, and two coherent look rows only after Gate 2 passes. A mirror-safe design normally needs about twelve total visual generations including the base; a non-mirror-safe design normally needs thirteen before repairs.

Never describe these estimates as guarantees. Count every repair and report material budget drift.

## Design For Extraction

- Keep each figure roughly 10–15% smaller than the guide's maximum safe bounds.
- Leave wide, uniform chroma gutters between poses and clear padding at every canvas edge.
- Prefer mirror-safe base designs when speed matters: centered costume, symmetric markings, no handheld weapon, no side-specific glow, and no directional text.
- Treat a handheld prop, asymmetric cape, one-sided marking, or directional lighting as non-mirror-safe unless visual inspection proves otherwise.
- Require every source pose and attached body part to remain completely inside its original invisible slot before framewise mirroring. A strip may pass pose-group extraction while still being unsafe to mirror inside fixed source slots; regenerate `running-left` when mirrored contact-sheet review shows sliced or displaced limbs.
- Use explicit screen-coordinate landmarks in direction prompts. For faces, name nose-tip, visible eye, pupils, muzzle or chin, and head center.
- Make `000` and `180` differ through the full head/face construction, not pupil movement alone.
- Match look row 10's raw source-pixel body height and maximum silhouette width to approved row 9. The assembler intentionally reuses row 9's scale; row 10 cannot rely on independent normalization, so a larger hat, shoulders, coat, or boots can pass source spacing yet fail the final-cell edge gate.

## Route Repairs By Failure Class

Classify a failure before spending another generation:

- `geometry` or `extraction`: use Hatch Pet's deterministic scripts first. If the source touches a canvas edge or poses merge, regenerate the complete strip with smaller poses and wider gutters.
- `single-cardinal canvas mismatch`: never feed an arbitrary portrait repair canvas directly to a cell composer. Deterministically extract and normalize it to the expected anchor contract when possible; otherwise regenerate the coherent four-cardinal strip.
- `identity` or `style`: repair the smallest complete affected row while preserving the approved base.
- `direction semantics`: strengthen screen-left/screen-right or up/down landmarks and resynthesize the complete containing look row. Do not patch a final cell.
- `chroma`: defer ordinary edge contamination to the single final despill. Regenerate only when the source subject itself uses or merges with the key color.
- `continuity metric warning`: inspect the normal-size ordered loop. Do not regenerate without a visible snap, scale pop, registration jump, broken attachment, wrong quadrant, or reversal.
- `alpha-hole warning`: distinguish exterior negative space from a genuine hole inside the filled silhouette before deciding.

After the same root failure recurs twice, change strategy rather than rewording the same prompt.

If a coherent row-scale repair oscillates twice between cell-edge failure and a visible undersize pop, stop visual generation. Preserve the best edge-safe candidate, finish all zero-cost QA, and ask the user whether to accept the nonconformant preview or authorize another attempt. Do not imply that an image model can reliably obey exact pixel dimensions; resume only with an approved deterministic coherent-row scale normalizer or explicit user consent to spend another generation.

## Run QA In Cost-Saving Order

Use this order:

1. Incrementally extract and validate each generated standard row.
2. Review the complete temporary `0–8` atlas and motion previews.
3. Generate and approve the four cardinal anchors.
4. Generate, register, and semantically review look row 9.
5. Generate, register, and semantically review look row 10.
6. Assemble a temporary transparent PNG v2 atlas.
7. Run blind direction QA, labeled normal-size semantics, continuity measurements, and final visual QA against the temporary PNG-derived sheets.
8. Resolve every major failure.
9. Run the single final despill, encode WebP, validate v2 geometry, package, and install.

Use PNG for intermediate assembly and QA. Treat WebP as the final delivery encode. Do not despill or finalize WebP before blind and labeled visual QA, because a later row repair would force duplicate cleanup and encoding.

## Preserve Evidence And Permissions

- Keep selected generated sources until they are copied into the run folder and their dependent checks pass.
- Treat cleanup of generated-image cache files as optional housekeeping; never block delivery on deletion permissions.
- Request permission for `${CODEX_HOME:-$HOME/.codex}/pets/<id>` only after the pet passes every local gate.
- Keep blind QA isolated from labels and answer keys as required by `$hatch-pet`.
- Record accepted metric or intermediate-direction warnings rather than silently discarding them.

## Completion Contract

Finish only when `$hatch-pet` acceptance passes: `1536x2288`, `spriteVersionNumber: 2`, all eleven rows, deterministic v2 validation, one successful final despill, explicit direction semantics, blind cardinal validation, reviewed continuity, final contact-sheet QA, and a staged `pet.json` plus `spritesheet.webp`.
