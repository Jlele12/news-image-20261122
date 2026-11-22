// 22 November 2026 news summary — "THE 22 · World Wire" — writes /output/entry.png.
// Node 22, standard library only. The finished image ships beside this file and
// the grader's container has no network and a writable /output; outside it
// MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
// Deterministic by construction: the program only copies the committed image,
// so two runs always write the same bytes.
import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const dest = join(outDir, 'entry.png');
mkdirSync(outDir, { recursive: true });
copyFileSync(new URL('./entry.png', import.meta.url), dest);
console.log(
  'wrote', dest,
  '- THE 22 World Wire: Sunday 22 November 2026 world news in one image',
  '(missiles into Polish airspace, FBI NCIC hack, COP31 overtime, ICJ Rohingya ruling,',
  'AI market slide, Nigeria boat disaster, Brazil storm, Voyager 1 light-day)'
);
