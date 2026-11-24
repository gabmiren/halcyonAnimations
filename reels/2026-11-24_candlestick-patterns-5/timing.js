// Script and timeline. Draft: synthetic word timings at 150 wpm with holds.
// Final: set window.VO_WORDS = {lineId: [[start,end],...]} (from forced alignment) before this runs.
const WPM = 150, HOLD = 0.5, SEC_HOLD = 0.7, LEAD = 0.15, COMMA_PAUSE = 0.18;
const ENDCARD_LEN = 4.55; // disclaimer (12 words) needs 4.44s of reading time

const SCRIPT = [
  { sec: 'hook', lines: [
    { id: 'k1', text: 'Here are five candlestick patterns every trader should know.', caption: false, start: 0.25 } ] },
  { sec: 's1', num: '1.', title: 'Hammer', titleWord: 3, lines: [
    { id: 'h1', text: 'Number one, the hammer.', title: true },
    { id: 'h2', text: 'A small body up top and a long wick below.', key: [[1, 2], [7, 8]] },
    { id: 'h3', text: 'Sellers pushed price down, and buyers pushed it right back.', key: [[6, 9]] } ] },
  { sec: 's2', num: '2.', title: 'Shooting star', titleWord: 3, lines: [
    { id: 'r1', text: 'Number two, the shooting star.', title: true },
    { id: 'r2', text: "It's the hammer flipped upside down, after a rally.", key: [[2, 2], [4, 5]] },
    { id: 'r3', text: 'Buyers tried to go higher, and sellers said no thanks.', key: [[7, 9]] } ] },
  { sec: 's3', num: '3.', title: 'Engulfing', titleWord: 3, lines: [
    { id: 'e1', text: 'Number three, the engulfing candle.', title: true },
    { id: 'e2', text: 'Its body swallows the body before it.', key: [[2, 2]] },
    { id: 'e3', text: 'After a drop, it can be a sign buyers are back.', key: [[8, 10]] } ] },
  { sec: 's4', num: '4.', title: 'Doji', titleWord: 3, lines: [
    { id: 'd1', text: 'Number four, the doji.', title: true },
    { id: 'd2', text: 'The open and close are almost the same price.', key: [[5, 7]] },
    { id: 'd3', text: 'Nobody won that candle, so the market is undecided.', key: [[8, 8]] } ] },
  { sec: 's5', num: '5.', title: 'Inside bar', titleWord: 3, lines: [
    { id: 'i1', text: 'Number five, the inside bar.', title: true },
    { id: 'i2', text: 'A candle that fits completely inside the one before it.', key: [[4, 5]] },
    { id: 'i3', text: 'The market is pausing, and a bigger move often follows the break.', key: [[9, 11]] } ] },
  { sec: 'close', lines: [
    { id: 'c1', text: 'Each pattern is a clue. It matters most at a key level.', key: [[10, 11]] } ] },
];

function syl(w) {
  w = w.toLowerCase().replace(/[^a-z]/g, '');
  if (!w) return 1;
  let m = (w.match(/[aeiouy]+/g) || []).length;
  if (w.length > 3 && /e$/.test(w) && !/le$/.test(w) && m > 1) m--;
  return Math.max(1, m);
}

function buildTimeline() {
  const TL = { lines: {}, sections: [], words: [] };
  let t = 0;
  for (const s of SCRIPT) {
    const sec = { id: s.sec, start: t, lines: [] };
    if (s.sec !== 'hook') t += LEAD;
    s.lines.forEach((ln, li) => {
      if (ln.start !== undefined) t = ln.start;
      const words = ln.text.split(' ');
      let times;
      if (window.VO_WORDS && window.VO_WORDS[ln.id]) {
        times = window.VO_WORDS[ln.id];
      } else {
        const dur = words.length / (WPM / 60);
        const commas = words.filter(w => /,$/.test(w)).length;
        const speech = dur - commas * COMMA_PAUSE;
        const wts = words.map(w => syl(w) + 0.35);
        const tot = wts.reduce((a, b) => a + b, 0);
        times = []; let c = t;
        words.forEach((w, i) => {
          const d = speech * wts[i] / tot;
          times.push([c, c + d]);
          c += d + (/,$/.test(w) ? COMMA_PAUSE : 0);
        });
      }
      const L = { id: ln.id, sec: s.sec, text: ln.text, words, times, key: ln.key || [], title: !!ln.title,
        caption: ln.caption !== false, start: times[0][0], end: times[times.length - 1][1] };
      TL.lines[ln.id] = L; sec.lines.push(L);
      words.forEach((w, i) => TL.words.push({ line: ln.id, i, w, s: times[i][0], e: times[i][1] }));
      const last = li === s.lines.length - 1;
      t = L.end + (last ? SEC_HOLD : HOLD);
    });
    sec.end = t;
    Object.assign(sec, { num: s.num, title: s.title, titleWord: s.titleWord });
    TL.sections.push(sec);
  }
  if (window.VO_WORDS) {
    // VO mode: sections are cut from the voice itself. Each section opens LEAD before its first word
    // and the one before it ends there; the close holds SEC_HOLD after the last word.
    TL.sections.forEach((sec, k) => { if (k > 0) sec.start = sec.lines[0].start - LEAD; });
    TL.sections.forEach((sec, k) => {
      const nx = TL.sections[k + 1];
      const lastL = sec.lines[sec.lines.length - 1];
      // the close holds until its caption has had its reading time: max(1.0, 0.6 + 0.32 x words)
      sec.end = nx ? nx.start : Math.max(lastL.end + SEC_HOLD, lastL.start + Math.max(1.0, 0.6 + 0.32 * lastL.words.length) + 0.05);
    });
    t = TL.sections[TL.sections.length - 1].end;
  }
  TL.endcard = { start: t, end: t + ENDCARD_LEN };
  TL.duration = t + ENDCARD_LEN;
  return TL;
}
const TL = buildTimeline();
window.TL = TL;
// Word start time helper: W('h2', 7)
function W(id, i) { return TL.lines[id].times[i][0]; }
function S(id) { return TL.sections.find(s => s.id === id); }
