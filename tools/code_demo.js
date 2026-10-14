/*
 * Makes src/partials/code-demo.html: example labels with real, scannable codes, drawn with
 * Label Maker's own QR and barcode encoders (Qr.gs and Barcode.gs from the label-addon repo).
 *   node tools/code_demo.js path/to/Qr.gs path/to/Barcode.gs
 */
const vm = require('vm'), fs = require('fs'), path = require('path');
const ctx = {}; vm.createContext(ctx);
for (const f of process.argv.slice(2)) vm.runInContext(fs.readFileSync(f, 'utf8'), ctx);

function qrSvg(text, px) {
  const q = ctx.qrEncode(text, 'M');
  const n = q.size, quiet = 2, size = n + quiet * 2;
  let d = '';
  q.modules.forEach((row, y) => row.forEach((on, x) => { if (on) d += `M${x + quiet} ${y + quiet}h1v1h-1z`; }));
  return `<svg class="qr" viewBox="0 0 ${size} ${size}" width="${px}" height="${px}" shape-rendering="crispEdges" role="img" aria-label="QR code for ${text}"><rect width="${size}" height="${size}" fill="#fff"/><path d="${d}" fill="#111"/></svg>`;
}
function barSvg(mods, label, w, h) {
  const quiet = 10, total = mods.length + quiet * 2;
  let d = '';
  mods.forEach((m, i) => { if (m) d += `M${i + quiet} 0h1v${h}h-1z`; });
  return `<svg class="bar" viewBox="0 0 ${total} ${h}" width="${w}" height="${Math.round(w * h / total)}" preserveAspectRatio="none" shape-rendering="crispEdges" role="img" aria-label="Barcode ${label}"><rect width="${total}" height="${h}" fill="#fff"/><path d="${d}" fill="#111"/></svg>`;
}
const c128 = ctx.code128Modules('ORD-20417').modules;
const ean = ctx.ean13Modules('400638133393').modules;

const html = `<div class="code-demo">
  <figure class="code-label wide"><div class="cl-body"><div class="cl-text"><b>Priya Raman</b><span>218 Alder Street, Unit 4B</span><span>Portland, OR 97214</span></div>${qrSvg('https://northpineapps.com/', 64)}</div>
    <figcaption><strong>QR code from a column</strong>Each label gets its own link, such as a guest's RSVP page. Try scanning this one.</figcaption></figure>
  <figure class="code-label wide"><div class="cl-body col"><div class="cl-text"><b>Ship to: Marcus Whitfield</b><span>1905 N Lake Shore Dr, Chicago, IL 60614</span></div>${barSvg(c128, 'ORD-20417', 210, 40)}<span class="hr">ORD-20417</span></div>
    <figcaption><strong>Code 128 barcode</strong>Order numbers, member IDs, asset tags. Any letters and numbers.</figcaption></figure>
  <figure class="code-label wide"><div class="cl-body"><div class="cl-text"><b>Hand-poured candle</b><span>Pine and cedar, 8 oz</span><span>Northside Candle Co.</span></div><div class="ean">${barSvg(ean, '4006381333931', 104, 60)}<span class="hr">4 006381 333931</span></div></div>
    <figcaption><strong>EAN-13 product barcode</strong>The standard shop barcode, from a 12 or 13 digit number.</figcaption></figure>
</div>
`;
const out = path.join(__dirname, '..', 'src', 'partials', 'code-demo.html');
fs.mkdirSync(path.dirname(out), { recursive: true });
fs.writeFileSync(out, html);
console.log('wrote', out, html.length);
