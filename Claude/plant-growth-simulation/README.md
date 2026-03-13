# Plant Growth SVG Animation

A self-contained browser demo that simulates a plant growing from the ground using SVG and vanilla JavaScript — no build tools, no external dependencies.

## Demo

Open `index.html` directly in any modern browser.

## What It Does

- A stem grows upward via a quadratic bezier curve, clipped each frame using De Casteljau subdivision
- Leaves sprout at regular intervals along the stem and unfurl with springy physics (overshoot + bounce)
- Wind causes gentle sway with unique phase offsets per leaf; random gusts add extra amplitude
- After full growth the plant fades out, resets, and loops forever

## Animation Phases

| Phase | Duration | Description |
|-------|----------|-------------|
| GROWING | ~7s | Stem extends, leaves spawn |
| SETTLING | 3s | Springs settle, wind sways |
| IDLE | 2s | Fully grown plant sways |
| RESETTING | 1.6s | Fade out → clear DOM → fade in → restart |

## Technical Details

- **Stem:** Single quadratic bezier `P0(200,550) → P1(160,320) → P2(205,95)`, subdivided via De Casteljau each frame
- **Leaves:** Cubic bezier blade shape with a midrib; rotation driven by a damped spring (`k=0.055, d=0.80`)
- **Wind:** `sin(t * 0.0008 + leafId * 0.7) * 6°` base sway + gust events decaying at 0.98/frame
- **`dt` clamping:** `Math.min(dt, 50ms)` prevents spring explosion when the tab loses focus

## File Structure

```
plant-growth-simulation/
└── index.html   # Everything: SVG markup, CSS, and JavaScript
```
