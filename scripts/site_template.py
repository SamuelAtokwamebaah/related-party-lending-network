"""Page shell for the Phase 3 map. Kept apart from the drawing code in build_site.py."""

# Palette values are the dataviz reference instance, validated all-pairs in both
# modes for the three slots used here (worst CVD dE 9.2 light / 9.4 dark, worst
# normal-vision dE 24.0 / 20.9). Slot 3 sits at 2.74:1 on the light surface, so
# the relief rule applies: every node is directly labelled and a table view ships.
STYLE = """
:root {
  color-scheme: light;
  --surface-0: #ffffff;
  --surface-1: #fcfcfb;
  --surface-2: #f4f4f1;
  --border:    #e2e2dc;
  --text-primary:   #0b0b0b;
  --text-secondary: #52514e;
  --text-muted:     #78776f;
  --series-1: #2a78d6;
  --series-2: #eb6834;
  --series-3: #1baf7a;
  --edge:     #9a998f;
  --accent:   #2a78d6;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    color-scheme: dark;
    --surface-0: #131312;
    --surface-1: #1a1a19;
    --surface-2: #232322;
    --border:    #34342f;
    --text-primary:   #ffffff;
    --text-secondary: #c3c2b7;
    --text-muted:     #8f8e84;
    --series-1: #3987e5;
    --series-2: #d95926;
    --series-3: #199e70;
    --edge:     #6f6e66;
    --accent:   #3987e5;
  }
}
:root[data-theme="dark"] {
  color-scheme: dark;
  --surface-0: #131312;
  --surface-1: #1a1a19;
  --surface-2: #232322;
  --border:    #34342f;
  --text-primary:   #ffffff;
  --text-secondary: #c3c2b7;
  --text-muted:     #8f8e84;
  --series-1: #3987e5;
  --series-2: #d95926;
  --series-3: #199e70;
  --edge:     #6f6e66;
  --accent:   #3987e5;
}

* { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--surface-0);
  color: var(--text-primary);
  font-family: "IBM Plex Sans", ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
  font-size: 16px;
  line-height: 1.6;
}
.wrap { max-width: 1080px; margin: 0 auto; padding: 0 24px 96px; }
header { padding: 72px 0 8px; }
h1 {
  font-family: Newsreader, ui-serif, Georgia, "Times New Roman", serif;
  font-weight: 500; font-size: clamp(2rem, 4.5vw, 3rem);
  line-height: 1.12; letter-spacing: -0.02em; margin: 0 0 16px;
}
h2 {
  font-family: Newsreader, ui-serif, Georgia, serif;
  font-weight: 500; font-size: 1.7rem; line-height: 1.2;
  margin: 64px 0 4px; letter-spacing: -0.01em;
}
h3 { font-size: 1rem; margin: 32px 0 8px; letter-spacing: -0.01em; }
p { margin: 0 0 16px; max-width: 68ch; color: var(--text-secondary); }
.lede { font-size: 1.12rem; color: var(--text-secondary); max-width: 64ch; }
.section-note { color: var(--text-muted); font-size: 0.9rem; margin: 4px 0 24px; max-width: 68ch; }
a { color: var(--accent); }
strong { color: var(--text-primary); font-weight: 600; }

.banner {
  border: 1px solid var(--border); border-left: 3px solid var(--series-2);
  background: var(--surface-1); border-radius: 3px;
  padding: 14px 18px; margin: 24px 0 8px;
  font-size: 0.92rem; color: var(--text-secondary);
}
.banner strong { color: var(--text-primary); }

.tiles { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1px;
         background: var(--border); border: 1px solid var(--border); border-radius: 4px;
         overflow: hidden; margin: 32px 0 8px; }
.tile { background: var(--surface-1); padding: 18px 20px; }
.tile .n { font-family: "IBM Plex Mono", ui-monospace, monospace;
           font-size: 1.9rem; line-height: 1.1; letter-spacing: -0.03em; }
.tile .k { font-size: 0.78rem; color: var(--text-muted); margin-top: 6px;
           text-transform: uppercase; letter-spacing: 0.06em; }

.legend { display: flex; flex-wrap: wrap; gap: 8px 22px; align-items: center;
          margin: 20px 0 26px; font-size: 0.85rem; color: var(--text-secondary); }
.legend .item { display: flex; align-items: center; gap: 7px; }
.swatch { width: 12px; height: 12px; border-radius: 50%; flex: none; }
.swatch.sq { border-radius: 2px; }
.swatch.ring { background: none !important; border: 2.5px dashed var(--series-3); }
.legend svg { display: block; }

.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 1px;
        background: var(--border); border: 1px solid var(--border); border-radius: 4px;
        overflow: hidden; }
.panel { background: var(--surface-1); padding: 10px 10px 4px; }
.panel .status { font-size: 0.72rem; line-height: 1.45; color: var(--text-muted);
                 border-top: 1px solid var(--border); margin-top: 6px; padding: 8px 4px 4px; }
.panel .status strong { color: var(--series-2); }
.panel .cap { font-size: 0.72rem; color: var(--text-muted); font-family: "IBM Plex Mono", monospace;
              padding: 2px 4px 6px; letter-spacing: 0.02em; }
.panel svg, .case svg { width: 100%; height: auto; display: block; }

.case { background: var(--surface-1); border: 1px solid var(--border);
        border-radius: 4px; padding: 16px; margin: 20px 0 8px; }
.case h3 { margin-top: 0; }

.edge { cursor: pointer; }
.edge:hover line:first-child, .edge:focus line:first-child { stroke: var(--accent); stroke-width: 3; }
.edge:focus { outline: none; }
.edge:focus-visible line:first-child { stroke: var(--accent); }

#cite { position: sticky; bottom: 0; z-index: 5;
        background: var(--surface-2); border: 1px solid var(--border);
        border-radius: 4px; padding: 14px 18px; margin-top: 16px; font-size: 0.9rem; }
#cite[hidden] { display: none !important; }
#cite .meta { font-family: "IBM Plex Mono", monospace; font-size: 0.76rem;
              color: var(--text-muted); margin-bottom: 8px; }
#cite blockquote { margin: 0; padding-left: 12px; border-left: 2px solid var(--series-1);
                   color: var(--text-secondary); }
#cite .hint { color: var(--text-muted); }

table { border-collapse: collapse; width: 100%; font-size: 0.84rem; margin-top: 8px; }
th, td { text-align: left; padding: 7px 10px; border-bottom: 1px solid var(--border);
         vertical-align: top; }
th { color: var(--text-muted); font-weight: 500; font-size: 0.76rem;
     text-transform: uppercase; letter-spacing: 0.05em; white-space: nowrap; }
td.num { font-family: "IBM Plex Mono", monospace; text-align: right; white-space: nowrap; }
.scroll { overflow-x: auto; border: 1px solid var(--border); border-radius: 4px; }
details { margin-top: 12px; }
summary { cursor: pointer; color: var(--accent); font-size: 0.9rem; }

.bars { margin-top: 8px; }
.bar-row { display: grid; grid-template-columns: 190px 1fr 44px; gap: 12px;
           align-items: center; margin-bottom: 7px; font-size: 0.85rem; }
.bar-row .lab { color: var(--text-secondary); text-align: right;
                font-family: "IBM Plex Mono", monospace; font-size: 0.78rem; }
/* Both must be blocks. As inline spans the fill had no width and no height, so
   every bar rendered as an empty track - the chart drew nothing at all. */
.bar-track { display: block; background: var(--surface-2);
             border-radius: 0 3px 3px 0; height: 16px; }
.bar-fill { display: block; background: var(--series-1); height: 100%;
            border-radius: 0 3px 3px 0; }
.bar-row .val { font-family: "IBM Plex Mono", monospace; color: var(--text-secondary); }

footer { margin-top: 72px; padding-top: 24px; border-top: 1px solid var(--border);
         color: var(--text-muted); font-size: 0.85rem; }
@media (max-width: 640px) {
  .bar-row { grid-template-columns: 120px 1fr 40px; }
  header { padding-top: 44px; }
}
"""

SCRIPT = """
(function () {
  var box = document.getElementById('cite');
  var meta = box.querySelector('.meta');
  var quote = box.querySelector('blockquote');
  var src = box.querySelector('.src');
  function show(el) {
    var amount = el.dataset.amount ? ' · ' + el.dataset.amount : '';
    meta.textContent = el.dataset.edge + ' · ' + el.dataset.from + ' → ' + el.dataset.to +
      ' · ' + el.dataset.rel + amount + ' · ' + el.dataset.conf +
      (el.dataset.anchor ? ' · ' + el.dataset.anchor : '');
    quote.textContent = el.dataset.quote || 'No quoted passage: this edge is inferred and is excluded from every figure.';
    src.textContent = el.dataset.source ? 'Passage as published by ' + el.dataset.source + '.' : '';
    box.hidden = false;
  }
  document.addEventListener('mouseover', function (e) {
    var el = e.target.closest('.edge');
    if (el) show(el);
  });
  document.addEventListener('focusin', function (e) {
    var el = e.target.closest('.edge');
    if (el) show(el);
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') box.hidden = true;
  });
})();
"""
