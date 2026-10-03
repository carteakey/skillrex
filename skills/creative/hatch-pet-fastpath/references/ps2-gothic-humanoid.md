# PS2 Gothic Humanoid Preset

Use this preset when the user wants a severe retro console hunter, occult wanderer, or gothic survival-horror humanoid rather than flat pixel art.

## Visual Contract

- Render an original late-PS2-era low-poly game character model.
- Use adult or slightly compact adult proportions: small head, longer limbs, narrow torso, grounded boots, and restrained hands.
- Show visible faceted polygon planes, angular joints, limited-bone posing, and a deliberately modest polygon budget.
- Use low-resolution nearest-neighbor textures, compressed cloth and leather detail, jagged alpha edges, dithered value transitions, and baked vertex-style lighting.
- Favor soot black, dried-blood burgundy, tarnished iron, dirty bone, and one small high-value eye or lens cue.
- Hide most of the face with a severe hat, cowl, mask, or high collar while keeping gaze landmarks readable at pet size.
- Keep the silhouette compact and symmetric when mirroring is desired. Prefer a sheathed or body-centered tool over a handheld weapon.
- Use a perfectly flat chroma background with no floor, contact shadow, scenery, fog, glow, or detached particles.

## Hard Avoids

Avoid chibi proportions, oversized head or eyes, plush softness, rounded toy anatomy, anime linework, cel shading, glossy collectible materials, modern PBR, realistic cinematic rendering, smooth high-poly cloth, painterly concept art, and clean vector pixel art.

“Pixelated PS2” means low-poly 3D geometry plus crunchy low-resolution textures. It does not mean a two-dimensional pixel sprite.

## Base Prompt Core

Use language equivalent to:

```text
One original late-PS2 survival-horror gothic hunter rendered as an in-game low-poly character model. Severe adult proportions, small obscured head, long angular limbs, narrow layered coat, rigid boots, faceted polygon planes, crunchy low-resolution nearest-neighbor textures, dithered baked lighting, jagged silhouette edges, soot-black and dried-burgundy palette, one restrained pale eye or lens cue. Symmetric readable full-body design with no handheld prop. Perfectly flat chroma background, no floor or shadow. Not cute, chibi, anime, plush, toy-like, painterly, cel-shaded, glossy, modern-PBR, or 2D pixel art.
```

Keep each row prompt shorter than the base prompt. Preserve the approved reference and name only the state action, geometry, gutters, and hard production hazards that apply to that row.

## Direction Cues

Lock the pelvis, boots, centered belt, torso, and lower coat broadly front-facing across both look rows. A low-poly humanoid prompt can drift into a turntable sequence; reject any row that reveals the back or keeps yawing past the side cardinal. Direction describes attention, not a 360-degree model spin.

- `000 up`: raise the eye line, hat brim, mask plane, chin, and upper-head pitch together.
- `090 right`: move the nose or mask projection and readable eye clearly across the head center toward screen-right; reveal the left side of the head.
- `180 down`: lower the eye line, tuck the chin, deepen the brim occlusion, and pitch the mask plane downward.
- `270 left`: move the nose or mask projection and readable eye clearly across the head center toward screen-left; reveal the right side of the head.
- Diagonals: interpolate both axes evenly; do not jump between unrelated three-quarter portraits.

After `090`, progressively reduce rightward head yaw while increasing downward pitch so `157.5` approaches the front-facing `180` family. After `270`, progressively reduce leftward yaw while increasing upward pitch so `337.5` approaches the front-facing `000` family.

At `192x208`, dark materials can erase direction cues. Preserve one pale eye/lens accent and a readable mask or nose plane, but do not enlarge them into cute facial features.
