// Writes the Run My Agents cooks as SVG from the board's own avatar definitions (services/app/web/src/avatars.ts).
import { mkdirSync, writeFileSync } from "node:fs";
import { join } from "node:path";
const [src, out] = [process.argv[2], process.argv[3]];
const { AGENTS, avatar } = await import(join(src, "services/app/web/src/avatars.ts"));
mkdirSync(join(out, "svg"), { recursive: true });
mkdirSync(join(out, "face"), { recursive: true });
const HAT = `<g><rect x="17" y="-7" width="30" height="12" rx="3" fill="#ffffff" stroke="#d8d8de" stroke-width="1.5"/><circle cx="21" cy="-11" r="8" fill="#ffffff"/><circle cx="43" cy="-11" r="8" fill="#ffffff"/><circle cx="32" cy="-16" r="10" fill="#ffffff"/><rect x="17" y="1" width="30" height="4" fill="#ececf1"/></g>`;
const meta = [];
for (const a of AGENTS) {
	const slug = a.role.toLowerCase();
	const plain = avatar(a, 512).replace(' class="ava"', "").replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ');
	writeFileSync(join(out, "svg", `${slug}.svg`), plain);
	// The cook: the same face with a chef hat on top. The viewBox grows upward so the hat fits.
	const vb = a.extra ? "-18 -30 100 100" : "-15 -30 94 94";
	const inner = plain.replace(/^<svg[^>]*>/, "").replace(/<\/svg>$/, "");
	const cook = `<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="${vb}" role="img" aria-label="${a.role} cook">${inner}${HAT}</svg>`;
	writeFileSync(join(out, "svg", `${slug}-cook.svg`), cook);
	// The face alone (eyes and extra, no body) for the 3D model's texture.
	const face = plain.replace(/^(<svg[^>]*>)(<(circle|rect|path)[^>]*\/>)/, "$1");
	writeFileSync(join(out, "face", `${slug}.svg`), face);
	meta.push({ role: a.role, slug, shape: a.shape, eyes: a.eyes, color: a.color, extra: a.extra ?? null });
}
writeFileSync(join(out, "cooks.json"), `${JSON.stringify(meta, null, 2)}\n`);
console.log(meta.map((m) => `${m.slug}:${m.shape}`).join(" "));
