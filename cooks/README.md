# Run My Agents cooks

The agents of [Run My Agents](https://github.com/flisk-sh/run-my-agents) as emoji and 3D models: 12 cooks, each with its own shape, colour and face, drawn from the board's own avatar code, so they match the chefs in its Kitchen tab.

<p align="center"><img src="png/planner-cook-64.png" width="56" alt="Planner cook"><img src="png/code-cook-64.png" width="56" alt="Code cook"><img src="png/design-cook-64.png" width="56" alt="Design cook"><img src="png/chores-cook-64.png" width="56" alt="Chores cook"><img src="png/video-cook-64.png" width="56" alt="Video cook"><img src="png/seo-cook-64.png" width="56" alt="SEO cook"><img src="png/social-cook-64.png" width="56" alt="Social cook"><img src="png/calls-cook-64.png" width="56" alt="Calls cook"><img src="png/calendar-cook-64.png" width="56" alt="Calendar cook"><img src="png/bug-cook-64.png" width="56" alt="Bug cook"><img src="png/refactor-cook-64.png" width="56" alt="Refactor cook"><img src="png/feature-cook-64.png" width="56" alt="Feature cook"></p>

| | Role | Name | Files |
|---|---|---|---|
| <img src="png/planner-cook-64.png" width="40"> | Planner | `planner-cook` | [svg](svg/planner-cook.svg) · [png](png/planner-cook-128.png) · [3D](3d/planner.glb) |
| <img src="png/code-cook-64.png" width="40"> | Code | `code-cook` | [svg](svg/code-cook.svg) · [png](png/code-cook-128.png) · [3D](3d/code.glb) |
| <img src="png/design-cook-64.png" width="40"> | Design | `design-cook` | [svg](svg/design-cook.svg) · [png](png/design-cook-128.png) · [3D](3d/design.glb) |
| <img src="png/chores-cook-64.png" width="40"> | Chores | `chores-cook` | [svg](svg/chores-cook.svg) · [png](png/chores-cook-128.png) · [3D](3d/chores.glb) |
| <img src="png/video-cook-64.png" width="40"> | Video | `video-cook` | [svg](svg/video-cook.svg) · [png](png/video-cook-128.png) · [3D](3d/video.glb) |
| <img src="png/seo-cook-64.png" width="40"> | SEO | `seo-cook` | [svg](svg/seo-cook.svg) · [png](png/seo-cook-128.png) · [3D](3d/seo.glb) |
| <img src="png/social-cook-64.png" width="40"> | Social | `social-cook` | [svg](svg/social-cook.svg) · [png](png/social-cook-128.png) · [3D](3d/social.glb) |
| <img src="png/calls-cook-64.png" width="40"> | Calls | `calls-cook` | [svg](svg/calls-cook.svg) · [png](png/calls-cook-128.png) · [3D](3d/calls.glb) |
| <img src="png/calendar-cook-64.png" width="40"> | Calendar | `calendar-cook` | [svg](svg/calendar-cook.svg) · [png](png/calendar-cook-128.png) · [3D](3d/calendar.glb) |
| <img src="png/bug-cook-64.png" width="40"> | Bug | `bug-cook` | [svg](svg/bug-cook.svg) · [png](png/bug-cook-128.png) · [3D](3d/bug.glb) |
| <img src="png/refactor-cook-64.png" width="40"> | Refactor | `refactor-cook` | [svg](svg/refactor-cook.svg) · [png](png/refactor-cook-128.png) · [3D](3d/refactor.glb) |
| <img src="png/feature-cook-64.png" width="40"> | Feature | `feature-cook` | [svg](svg/feature-cook.svg) · [png](png/feature-cook-128.png) · [3D](3d/feature.glb) |

## Use them

- **Emoji:** the square `png/<name>-128.png` files work as Slack and Discord custom emoji (`:code-cook:`). `32`, `64` and `512` px are there too. `<name>` is the cook (with a hat) or the face alone (`code`).
- **3D:** `3d/<role>.glb` opens in Blender, Quick Look, three.js, `<model-viewer>` and most viewers. Each model is a rounded body in the agent's shape and colour, its face on the front, and a chef hat, about 270 KB.
- **SVG:** `svg/` is the source for the PNGs, any size.

```html
<script type="module" src="https://cdn.jsdelivr.net/npm/@google/model-viewer@3.5.0/dist/model-viewer.min.js"></script>
<model-viewer src="3d/code.glb" camera-orbit="18deg 78deg 105%" auto-rotate camera-controls style="width:240px;height:240px"></model-viewer>
```

## Rebuild

`scripts/build.sh /path/to/run-my-agents` regenerates every file here from the board's `services/app/web/src/avatars.ts` (needs bun, rsvg-convert and python3). `cooks.json` lists each agent's shape, eyes, colour and extra.

Same licence as the rest of this repo: MIT, see [../LICENSE](../LICENSE).
