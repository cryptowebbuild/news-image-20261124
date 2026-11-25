import { copyFileSync, existsSync, mkdirSync, statSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const rootDir = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const srcPath = join(rootDir, 'entry.png');
const dstPath = join(outDir, 'entry.png');

if (!existsSync(srcPath)) {
  throw new Error(`Missing source image: ${srcPath}`);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(srcPath, dstPath);

const sizeBytes = statSync(dstPath).size;
console.log(`Wrote ${dstPath} (${sizeBytes} bytes)`);
