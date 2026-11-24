const C = document.getElementById('c'), X = C.getContext('2d');
const CY = '#00FBF4', GR = '#AFAFAF', INK = '#F2F2F2', BG = '#0B0C0D';
const FW = 1080, FH = 1920, CX = 540;
const STAGE = { x: 160, y: 620, w: 760, h: 700 };
const CAP = { top: 370, maxW: 800, size: 50, lh: 70 };

const IMG = { full: new Image() };
IMG.full.src = 'assets/logo_full.png';

const clamp = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));
const eo = p => 1 - Math.pow(1 - p, 3);
const prog = (t, at, dur) => eo(clamp((t - at) / dur));

// ---------- chart data ----------
function seq(n, t0, t1) {
  const step = n > 1 ? Math.min(0.3, (t1 - t0 - 0.24) / (n - 1)) : 0;
  return Array.from({ length: n }, (_, i) => t0 + i * step);
}
function cnd(arr, times) {
  return arr.map((a, i) => ({ o: a[0], h: a[1], l: a[2], c: a[3], tb: times[i] }));
}
const CHARTS = {};
function buildCharts() {
  // 1. Hammer
  {
    const s = S('s1'), tp = W('h2', 1);
    const lead = cnd([[80, 84, 74, 76], [76, 79, 70, 72], [72, 77, 70, 75], [75, 76, 66, 67], [67, 69, 60, 62],
      [62, 66, 60, 64], [64, 65, 55, 56], [56, 58, 49, 51]], seq(8, s.start + 0.2, tp - 0.1));
    const ham = { o: 50, h: 53.5, l: 36, c: 53, tb: tp, tl: W('h2', 7), ldur: 0.5 };
    CHARTS.s1 = { lo: 32, hi: 87, offset: 0.3, slots: 12, candles: [...lead, ham], ann: [
      { k: 'label', text: 'Small body', i: 8.38, p: 58.8, align: 'left', lead: [8.2, 53.4], at: W('h2', 1) },
      { k: 'label', text: 'Long wick', i: 7.55, p: 39.5, align: 'right', lead: [7.92, 39.5], at: W('h2', 7) },
      { k: 'arrow', i1: 9.05, p1: 52, i2: 9.05, p2: 38.5, col: GR, at: W('h3', 1) },
      { k: 'capsule', i: 8, p1: 35, p2: 50.2, at: W('h3', 6) },
      { k: 'arrow', i1: 9.6, p1: 38.5, i2: 9.6, p2: 52, col: CY, at: W('h3', 6) },
    ] };
  }
  // 2. Shooting star
  {
    const s = S('s2'), tp = W('r2', 3);
    const lead = cnd([[30, 34, 28, 33], [33, 38, 32, 37], [37, 38, 33, 34], [34, 42, 33, 41], [41, 47, 40, 46],
      [46, 47, 42, 43], [43, 51, 42, 50], [50, 56, 49, 55]], seq(8, s.start + 0.2, tp - 0.1));
    const star = { o: 55.5, h: 72, l: 52.5, c: 53, tb: tp, tu: W('r2', 4), udur: 0.5 };
    CHARTS.s2 = { lo: 20, hi: 76, offset: 0.3, slots: 11.5, candles: [...lead, star], ann: [
      { k: 'arrow', i1: -0.1, p1: 24.3, i2: 7.4, p2: 43, col: GR, at: W('r2', 8), dur: 0.5 },
      { k: 'capsule', i: 8, p1: 55.3, p2: 73, at: W('r3', 4) },
      { k: 'label', text: 'Upper wick', i: 7.5, p: 67, align: 'right', lead: [7.9, 67], at: W('r3', 4) },
      { k: 'arrow', i1: 9.1, p1: 63, i2: 9.1, p2: 51, col: GR, at: W('r3', 7) },
    ] };
  }
  // 3. Engulfing
  {
    const s = S('s3'), tp = W('e2', 0);
    const lead = cnd([[78, 80, 72, 73], [73, 76, 71, 75], [75, 76, 66, 67], [67, 69, 61, 62], [62, 65, 60, 64],
      [64, 65, 55, 56], [56, 57.5, 52, 53]], seq(7, s.start + 0.2, tp - 0.1));
    const big = { o: 52, h: 61, l: 51, c: 60, tb: tp, bdur: 0.7 };
    CHARTS.s3 = { lo: 47, hi: 85, offset: 0.4, slots: 10.2, candles: [...lead, big], ann: [
      { k: 'box', i1: 5.52, i2: 7.48, p1: 51.3, p2: 60.7, at: W('e2', 2) },
      { k: 'arrow', i1: -0.1, p1: 83.2, i2: 5.3, p2: 67.5, col: GR, at: W('e3', 2), dur: 0.5 },
      { k: 'arrow', i1: 8.2, p1: 55, i2: 8.2, p2: 66, col: CY, at: W('e3', 8) },
    ] };
  }
  // 4. Doji
  {
    const s = S('s4'), tp = W('d1', 3);
    const lead = cnd([[50, 56, 48, 55], [55, 57, 50, 51], [51, 58, 50, 57], [57, 61, 55, 60], [60, 61, 54, 55],
      [55, 59, 53, 58]], seq(6, s.start + 0.2, tp - 0.1));
    const doji = { o: 58, h: 64, l: 52, c: 58.3, tb: tp, xi: 6.9 };
    CHARTS.s4 = { lo: 46, hi: 66, offset: 0.3, slots: 9.4, candles: [...lead, doji], ann: [
      { k: 'tick', i: 6.9, p: 58, side: 'L', at: W('d2', 1), meet: W('d2', 5) },
      { k: 'label', text: 'Open', i: 5.95, p: 62.8, align: 'center', lead: [6.2, 58.4], at: W('d2', 1) },
      { k: 'tick', i: 6.9, p: 58.3, side: 'R', at: W('d2', 3), meet: W('d2', 5) },
      { k: 'label', text: 'Close', i: 7.85, p: 62.8, align: 'center', lead: [7.6, 58.7], at: W('d2', 3) },
      { k: 'meet', i: 6.9, p: 58.15, at: W('d2', 5) },
      { k: 'ring', i: 6.9, p: 58.15, r: 0.95, at: W('d3', 0) },
      { k: 'label', text: 'Undecided', i: 6.9, p: 49.4, align: 'center', at: W('d3', 8) },
    ] };
  }
  // 5. Inside bar
  {
    const s = S('s5'), tp = W('i2', 0);
    const lead = cnd([[40, 44, 37, 43], [43, 45, 39, 40], [40, 47, 39, 46], [46, 48, 42, 43], [43, 58, 41, 56]],
      seq(5, s.start + 0.2, tp - 0.1));
    const ins = { o: 52, h: 54.5, l: 47, c: 49, tb: W('i2', 1) };
    const brk = { o: 49.5, h: 66, l: 49, c: 65, tb: W('i3', 6), bdur: 0.55 };
    CHARTS.s5 = { lo: 34, hi: 70, offset: 0.4, slots: 8.2, candles: [...lead, ins, brk], ann: [
      { k: 'box', i1: 3.5, i2: 5.5, p1: 40.5, p2: 58.5, at: W('i2', 4) },
      { k: 'hline', i1: 5.5, i2: 7.3, p: 58.5, at: W('i3', 3) },
      { k: 'hline', i1: 5.5, i2: 7.3, p: 40.5, at: W('i3', 3) },
      { k: 'ring', i: 6, p: 58.5, r: 0.5, at: W('i3', 11), front: true },
    ] };
  }
}

// ---------- chart drawing ----------
function mapper(ch, R) {
  const sw = R.w / ch.slots;
  return { sw, s: R.w / STAGE.w, x: i => R.x + (ch.offset + i + 0.5) * sw, y: p => R.y + (ch.hi - p) / (ch.hi - ch.lo) * R.h };
}
function drawCandle(m, cd, i, t) {
  const pb = prog(t, cd.tb, cd.bdur || 0.24);
  if (pb <= 0) return;
  const col = cd.c >= cd.o ? CY : GR;
  const x = m.x(i), bw = m.sw * 0.58, ww = Math.max(2, 3.6 * m.s);
  const cur = cd.o + (cd.c - cd.o) * pb;
  const top = Math.max(cd.o, cur), bot = Math.min(cd.o, cur);
  const pu = cd.tu !== undefined ? prog(t, cd.tu, cd.udur || 0.24) : pb;
  const pl = cd.tl !== undefined ? prog(t, cd.tl, cd.ldur || 0.24) : pb;
  const fullTop = Math.max(cd.o, cd.c), fullBot = Math.min(cd.o, cd.c);
  X.fillStyle = col;
  if (pu > 0) { const y1 = m.y(top), y2 = m.y(top + (cd.h - fullTop) * pu); X.fillRect(x - ww / 2, y2, ww, y1 - y2); }
  if (pl > 0) { const y1 = m.y(bot), y2 = m.y(bot - (fullBot - cd.l) * pl); X.fillRect(x - ww / 2, y1, ww, y2 - y1); }
  let yt = m.y(top), yb = m.y(bot);
  const minH = Math.max(3, 5 * m.s);
  if (yb - yt < minH) { const mid = (yt + yb) / 2; yt = mid - minH / 2; yb = mid + minH / 2; }
  X.fillRect(x - bw / 2, yt, bw, yb - yt);
}
function arrowHead(x, y, ang, sz) {
  X.beginPath();
  X.moveTo(x, y);
  X.lineTo(x - sz * Math.cos(ang - 0.45), y - sz * Math.sin(ang - 0.45));
  X.lineTo(x - sz * Math.cos(ang + 0.45), y - sz * Math.sin(ang + 0.45));
  X.closePath(); X.fill();
}
function rrect(x, y, w, h, r) {
  X.beginPath(); X.moveTo(x + r, y); X.arcTo(x + w, y, x + w, y + h, r); X.arcTo(x + w, y + h, x, y + h, r);
  X.arcTo(x, y + h, x, y, r); X.arcTo(x, y, x + w, y, r); X.closePath();
}
function drawAnn(m, a, t, opts) {
  const s = m.s;
  if (a.k === 'label') {
    if (!opts.labels) return;
    const p = prog(t, a.at, 0.2); if (p <= 0) return;
    X.save(); X.globalAlpha *= p;
    X.font = `500 ${Math.round(34 * s)}px P`; X.fillStyle = INK; X.textBaseline = 'middle';
    X.textAlign = a.align;
    const x = m.x(a.i), y = m.y(a.p) + (1 - p) * 10;
    X.fillText(a.text, x, y);
    if (a.lead) {
      const tw = X.measureText(a.text).width;
      let lx = x, ly = y;
      if (a.align === 'left') lx = x - 12; else if (a.align === 'right') lx = x + 12; else ly = y + 26 * s;
      X.strokeStyle = GR; X.lineWidth = 2 * s; X.globalAlpha *= 0.8;
      X.beginPath(); X.moveTo(lx, ly); X.lineTo(m.x(a.lead[0]), m.y(a.lead[1])); X.stroke();
    }
    X.restore();
  } else if (a.k === 'arrow') {
    const p = prog(t, a.at, a.dur || 0.38); if (p <= 0) return;
    const x1 = m.x(a.i1), y1 = m.y(a.p1), x2 = m.x(a.i2), y2 = m.y(a.p2);
    const xe = x1 + (x2 - x1) * p, ye = y1 + (y2 - y1) * p, ang = Math.atan2(y2 - y1, x2 - x1);
    const hs = 20 * s;
    X.save(); X.strokeStyle = a.col; X.fillStyle = a.col; X.lineWidth = 4 * s; X.lineCap = 'round';
    X.beginPath(); X.moveTo(x1, y1); X.lineTo(xe - Math.cos(ang) * hs * 0.6, ye - Math.sin(ang) * hs * 0.6); X.stroke();
    arrowHead(xe, ye, ang, hs); X.restore();
  } else if (a.k === 'capsule') {
    const p = prog(t, a.at, 0.28); if (p <= 0) return;
    const x = m.x(a.i), y1 = m.y(a.p2), y2 = m.y(a.p1), w = m.sw * 0.62;
    const sc = 0.85 + 0.15 * p, cy = (y1 + y2) / 2, h = (y2 - y1) * sc, ww = w * sc;
    X.save(); X.globalAlpha *= p;
    rrect(x - ww / 2, cy - h / 2, ww, h, ww / 2);
    X.fillStyle = 'rgba(0,251,244,0.14)'; X.fill();
    X.strokeStyle = CY; X.lineWidth = 3 * s; X.stroke(); X.restore();
  } else if (a.k === 'box') {
    const p = prog(t, a.at, 0.45); if (p <= 0) return;
    const x1 = m.x(a.i1), x2 = m.x(a.i2), y1 = m.y(a.p2), y2 = m.y(a.p1);
    const w = x2 - x1, h = y2 - y1, per = 2 * (w + h);
    X.save();
    X.globalAlpha *= p; X.fillStyle = 'rgba(0,251,244,0.08)'; rrect(x1, y1, w, h, 10 * s); X.fill();
    X.globalAlpha = X.globalAlpha / p;
    X.strokeStyle = CY; X.lineWidth = 3.5 * s; X.setLineDash([per * p, per]);
    rrect(x1, y1, w, h, 10 * s); X.stroke(); X.restore();
  } else if (a.k === 'ring') {
    const p = prog(t, a.at, 0.45); if (p <= 0) return;
    const x = m.x(a.i), y = m.y(a.p), r = a.r * m.sw;
    X.save(); X.fillStyle = 'rgba(0,251,244,0.10)'; X.globalAlpha *= p;
    X.beginPath(); X.arc(x, y, r, 0, Math.PI * 2); X.fill(); X.globalAlpha /= p;
    X.strokeStyle = a.front ? INK : CY; X.lineWidth = 3.5 * s;
    X.beginPath(); X.arc(x, y, r, -Math.PI / 2, -Math.PI / 2 + Math.PI * 2 * p); X.stroke(); X.restore();
  } else if (a.k === 'hline') {
    const p = prog(t, a.at, 0.4); if (p <= 0) return;
    const x1 = m.x(a.i1), x2 = m.x(a.i2), y = m.y(a.p);
    X.save(); X.strokeStyle = GR; X.lineWidth = 2.5 * s; X.setLineDash([12 * s, 10 * s]);
    X.beginPath(); X.moveTo(x1, y); X.lineTo(x1 + (x2 - x1) * p, y); X.stroke(); X.restore();
  } else if (a.k === 'tick') {
    const p = prog(t, a.at, 0.25); if (p <= 0) return;
    const pm = a.meet !== undefined ? prog(t, a.meet, 0.35) : 0;
    const x = m.x(a.i), y = m.y(a.p), bw = m.sw * 0.58, L = m.sw * 0.55;
    const inner = (bw / 2 - 6 * s) * (1 - pm); // distance of the tick's inner end from the candle centre
    X.save(); X.strokeStyle = INK; X.lineWidth = 6 * s; X.lineCap = 'round';
    X.beginPath();
    const dir = a.side === 'L' ? -1 : 1, outer = bw / 2 + L;
    X.moveTo(x + dir * outer, y); X.lineTo(x + dir * (outer - (outer - inner) * p), y);
    X.stroke(); X.restore();
  } else if (a.k === 'meet') { /* handled by the ticks */
  }
}
function drawChart(ch, R, t, opts) {
  const m = mapper(ch, R);
  // annotations that sit behind candles first (capsule/box/ring fills), then candles, then the rest
  ch.ann.filter(a => ['capsule', 'box', 'ring'].includes(a.k) && !a.front).forEach(a => drawAnn(m, a, t, opts));
  ch.candles.forEach((cd, i) => drawCandle(m, cd, cd.xi !== undefined ? cd.xi : i, t));
  ch.ann.filter(a => !['capsule', 'box', 'ring'].includes(a.k) || a.front).forEach(a => drawAnn(m, a, t, opts));
}

// ---------- text ----------
function layoutWords(words, size, weight, maxW) {
  X.font = `${weight} ${size}px P`;
  const sp = X.measureText(' ').width, lines = [[]];
  let w = 0;
  words.forEach((wd, i) => {
    const ww = X.measureText(wd).width;
    if (lines[lines.length - 1].length && w + sp + ww > maxW) { lines.push([]); w = 0; }
    const ln = lines[lines.length - 1];
    if (ln.length) w += sp;
    ln.push({ i, wd, x: w, w: ww }); w += ww;
  });
  return lines.map(l => ({ items: l, width: l.length ? l[l.length - 1].x + l[l.length - 1].w : 0 }));
}
function inKey(key, i) { return key.some(r => i >= r[0] && i <= r[1]); }
function drawCaption(L, t, alpha) {
  const lines = layoutWords(L.words, CAP.size, 500, CAP.maxW);
  X.save(); X.textBaseline = 'alphabetic'; X.textAlign = 'left'; X.font = `500 ${CAP.size}px P`;
  lines.forEach((ln, li) => {
    const x0 = CX - ln.width / 2, y = CAP.top + CAP.size + li * CAP.lh;
    ln.items.forEach(it => {
      const p = clamp((t - L.times[it.i][0]) / 0.07); if (p <= 0) return;
      X.globalAlpha = alpha * p;
      X.fillStyle = inKey(L.key, it.i) ? CY : INK;
      X.fillText(it.wd, x0 + it.x, y);
    });
  });
  X.restore();
}
function drawTitle(sec, L, t, alpha) {
  const size = 72; X.save(); X.font = `700 ${size}px P`; X.textBaseline = 'alphabetic';
  const a = sec.num + ' ', b = sec.title, wa = X.measureText(a).width, wb = X.measureText(b).width;
  const x0 = CX - (wa + wb) / 2, y = CAP.top + size;
  const pa = clamp((t - L.times[0][0]) / 0.1), pb = clamp((t - L.times[sec.titleWord][0]) / 0.1);
  X.textAlign = 'left'; X.fillStyle = CY;
  X.globalAlpha = alpha * pa; X.fillText(a, x0, y);
  X.globalAlpha = alpha * pb; X.fillText(b, x0 + wa, y);
  X.restore();
}

// ---------- grid ----------
const GRID = [
  { k: 's1', label: '1. Hammer' }, { k: 's2', label: '2. Shooting star' }, { k: 's3', label: '3. Engulfing' },
  { k: 's4', label: '4. Doji' }, { k: 's5', label: '5. Inside bar' }];
function gridCells(top, rowH = 262, ch = 188) {
  const cw = 385, xs = [140, 555];
  return GRID.map((g, n) => {
    const row = Math.floor(n / 2), col = n % 2;
    const x = n === 4 ? CX - cw / 2 : xs[col];
    return { ...g, R: { x: x + 14, y: top + row * rowH, w: cw - 28, h: ch }, lx: x + cw / 2, ly: top + row * rowH + ch + 48 };
  });
}
function drawGrid(alpha, top, rowH, ch) {
  X.save(); X.globalAlpha = alpha;
  gridCells(top, rowH, ch).forEach(c => {
    drawChart(CHARTS[c.k], c.R, 1e9, { labels: false });
    X.font = '700 36px P'; X.textAlign = 'center'; X.textBaseline = 'alphabetic'; X.fillStyle = INK;
    X.fillText(c.label, c.lx, c.ly);
  });
  X.restore();
}
function drawCoverTitle(alpha) {
  X.save(); X.globalAlpha = alpha; X.textAlign = 'center'; X.textBaseline = 'alphabetic';
  let size = 74; X.font = `700 ${size}px P`;
  while (X.measureText('every trader should know').width > 800) { size -= 2; X.font = `700 ${size}px P`; }
  X.fillStyle = CY; X.fillText('5 candlestick patterns', CX, 360 + size);
  X.fillStyle = INK; X.fillText('every trader should know', CX, 360 + size + size * 1.18);
  X.restore();
}

// ---------- end card ----------
function drawDots() {
  X.save(); X.fillStyle = 'rgba(255,255,255,0.045)';
  for (let y = 24; y < FH; y += 48) for (let x = 24; x < FW; x += 48) { X.beginPath(); X.arc(x, y, 1.6, 0, 6.3); X.fill(); }
  const g = X.createRadialGradient(CX, 760, 40, CX, 760, 520);
  g.addColorStop(0, 'rgba(0,251,244,0.05)'); g.addColorStop(1, 'rgba(0,251,244,0)');
  X.fillStyle = g; X.fillRect(0, 0, FW, FH); X.restore();
}
function drawEndCard() {
  X.fillStyle = '#07090C'; X.fillRect(0, 0, FW, FH);
  drawDots();
  const lw = 420, lh = lw * IMG.full.naturalHeight / IMG.full.naturalWidth;
  X.drawImage(IMG.full, CX - lw / 2, 520, lw, lh);
  const pw = 580, ph = 106, py = 820;
  rrect(CX - pw / 2, py, pw, ph, ph / 2); X.strokeStyle = CY; X.lineWidth = 4; X.stroke();
  X.font = '700 48px P'; X.fillStyle = INK; X.textAlign = 'center'; X.textBaseline = 'middle';
  X.fillText('Ask us in our Discord', CX, py + ph / 2 + 2);
  X.font = '600 32px P'; X.font = '700 32px P'; X.fillStyle = GR;
  if ('letterSpacing' in X) X.letterSpacing = '9px';
  X.fillText('LINK IN BIO', CX + 4, 983);
  if ('letterSpacing' in X) X.letterSpacing = '0px';
  X.font = '400 30px P'; X.fillStyle = GR;
  X.fillText('Halcyon offers simulated educational accounts.', CX, 1092);
  X.fillText('Results not guaranteed. T&C apply.', CX, 1136);
}

// ---------- frame ----------
function secAlpha(sec, t) {
  if (t < sec.start || t >= sec.end) return 0;
  if (sec.id === 'close') return clamp((t - sec.start) / 0.35); // close holds to the hard cut
  return clamp((sec.end - t) / 0.3);
}
function drawLogoTop() {
  const lw = 200, lh = lw * IMG.full.naturalHeight / IMG.full.naturalWidth;
  X.drawImage(IMG.full, CX - lw / 2, 264, lw, lh);
}
function render(t) {
  X.setTransform(1, 0, 0, 1, 0, 0);
  X.globalAlpha = 1; X.fillStyle = BG; X.fillRect(0, 0, FW, FH);
  if (t >= TL.endcard.start) { drawEndCard(); return; }
  const sec = TL.sections.find(s => t >= s.start && t < s.end);
  if (!sec) return;
  const a = secAlpha(sec, t);
  if (sec.id === 'hook') { drawCoverTitle(a); drawGrid(a, 580); return; }
  if (sec.id === 'close') {
    drawGrid(a, 625, 248, 172);
    drawCaption(sec.lines[0], t, 1);
    return;
  }
  // caption slot: the latest line that has started
  let L = null; for (const l of sec.lines) if (t >= l.start) L = l;
  if (!L) L = sec.lines[0];
  if (L.title) drawTitle(sec, L, t, a); else drawCaption(L, t, a);
  X.save(); X.globalAlpha = a; drawChart(CHARTS[sec.id], STAGE, t, { labels: true }); X.restore();
}

buildCharts();
window.seek = t => { render(t); return true; };
window.ready = Promise.all([document.fonts.load('500 50px P'), document.fonts.load('700 50px P'), document.fonts.load('400 30px P'),
  new Promise(r => IMG.full.complete ? r() : (IMG.full.onload = r))]).then(() => document.fonts.ready).then(() => { render(0); return true; });
// Export the timeline map for QA
window.timelineMap = () => ({
  duration: TL.duration, endcard: TL.endcard,
  sections: TL.sections.map(s => ({ id: s.id, start: s.start, end: s.end })),
  lines: Object.values(TL.lines).map(l => ({ id: l.id, text: l.text, start: l.start, end: l.end, words: l.words.length })),
  events: Object.entries(CHARTS).flatMap(([k, ch]) => [
    ...ch.candles.map((c, i) => ({ sec: k, kind: 'candle', i, at: c.tb, tu: c.tu, tl: c.tl })),
    ...ch.ann.map(a => ({ sec: k, kind: a.k, text: a.text || '', at: a.at }))]),
});
