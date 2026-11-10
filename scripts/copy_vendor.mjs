// Copies front-end libraries from node_modules into app/static/vendor (served locally).
// Run from the project root: npm run vendor
import { cpSync, mkdirSync } from "node:fs";
import { dirname } from "node:path";

const out = "app/static/vendor";
const copies = [
  ["node_modules/alpinejs/dist/cdn.min.js", `${out}/alpine/alpine.min.js`],
  ["node_modules/@fortawesome/fontawesome-free/css/all.min.css", `${out}/fontawesome/css/all.min.css`],
  ["node_modules/@fortawesome/fontawesome-free/webfonts", `${out}/fontawesome/webfonts`],
  ["node_modules/quill/dist/quill.js", `${out}/quill/quill.js`],
  ["node_modules/quill/dist/quill.snow.css", `${out}/quill/quill.snow.css`],
];

for (const [src, dest] of copies) {
  mkdirSync(dirname(dest), { recursive: true });
  cpSync(src, dest, { recursive: true });
  console.log(`${src} -> ${dest}`);
}
