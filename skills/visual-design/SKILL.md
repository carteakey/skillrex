---
name: visual-design
description: "Unified skill for visual creation: Generative AI (ComfyUI), Diagramming (Excalidraw), Web/UI Design (Design.md, Claude Design), and Digital Art (ASCII, Manim, P5js, Infographics)."
---

# Visual Design & Creative Tools

A comprehensive suite for everything from generative AI workflows to formal design specifications and digital art.

## 1. Generative AI (ComfyUI)
Use this for advanced Stable Diffusion, Flux, or video generation workflows.
- **Setup & Lifecycle:** `comfy-cli` installation and launch.
- **Execution:** Running workflows with parameter injection.
- **Monitoring:** Real-time WebSocket monitoring and error logging.
- **Reference:** See `references/comfyui/` for detailed API and workflow guides.

## 2. Diagramming & Schematics
Create structural and flow diagrams.
- **Excalidraw:** Hand-drawn style diagrams for rapid prototyping.
- **Architecture Diagrams:** Formal structural layouts.
- **Reference:** See `references/excalidraw/` and `references/architecture_diagram/`.

## 3. Web & UI Design
Design systems, web layouts, and UI components.
- **DESIGN.md:** Google's spec for formal design tokens and accessibility.
- **Claude Design:** Rapid HTML/CSS artifact prototyping.
- **Popular Web Designs:** Implement real-world design systems (Stripe, Vercel, etc.).
- **Sketch:** Throwaway HTML mockups for comparison.
- **Reference:** See `references/design_md/`, `references/claude_design/`, `references/popular_web_designs/`, and `references/sketch/`.

## 4. Digital Art & Animation
Creative coding and automated visual generation.
- **Infographics (Baoyu):** High-density information visualization.
- **ASCII Art/Video:** Text-based visual art.
- **Manim Video:** Mathematical and algorithmic animations.
- **P5.js:** Creative coding and interactive sketches.
- **Reference:** See `references/baoyu_infographic/`, `references/ascii_art/`, `references/ascii_video/`, `references/manim_video/`, and `references/p5js/`.

## Pitfalls
- **ComfyUI:** Always check hardware (VRAM) before running heavy models.
- **DESIGN.md:** Ensure token references use `{path.to.token}` syntax.
- **Workflow:** Use the correct tool for the task (e.g., `sketch` for quick ideas, `design-md` for formal specs).
