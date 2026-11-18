// Entry program for make.fun's "Sum up 17 November's world news in one
// image" contest (news-image-20261117). The picture itself is entry.png
// beside this file — drawn from scratch by draw.py — and this program's
// whole job is to place it where the grader looks: /output/entry.png
// (or $MAKEFUN_OUTPUT_DIR when set, for local runs).
//
// Node 22, standard library only; the grading sandbox has no network.

import { copyFileSync, openSync, readSync, closeSync, statSync } from 'node:fs';
import { join } from 'node:path';

const source = new URL('./entry.png', import.meta.url);
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const target = join(outDir, 'entry.png');

const { size } = statSync(source);
if (size === 0 || size > 1_048_576) {
  throw new Error(`entry.png is ${size} bytes; the gate allows at most 1 MiB`);
}

// The gate tells PNG from JPEG by the first bytes; refuse anything else
// before copying, so a corrupt asset fails loudly here instead of there.
const head = Buffer.alloc(8);
const fd = openSync(source, 'r');
readSync(fd, head, 0, 8, 0);
closeSync(fd);
const isPng = head.subarray(0, 4).equals(Buffer.from([0x89, 0x50, 0x4e, 0x47]));
const isJpeg = head[0] === 0xff && head[1] === 0xd8;
if (!isPng && !isJpeg) {
  throw new Error('entry.png is neither a PNG nor a JPEG');
}

copyFileSync(source, target);
console.log(`entry.png (${size} bytes) -> ${target}`);
