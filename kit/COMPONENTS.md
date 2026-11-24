# 90s set pieces

These are reusable building blocks for the 90s finance-TV look. Every piece lives inside a reel's `page.html`; copy its CSS and draw function from there.

**Rule:** each new reel should bring at least two set pieces no earlier reel has used, and shouldn't repeat the previous reel's main set pieces.

## Always-on chrome (the house style, reuse every time)
| Piece | What it is | Where |
|---|---|---|
| Chyron header | White tag ("BREAKING · NASDAQ") over a cyan uppercase bar. A bigger 3-line version runs during the hook | all reels (`.chy`) |
| Ticker crawl | Black strip at y 1340 with a cyan top rule and scrolling facts | all reels (`.tick`) |
| Word-by-word captions | Grey to white, key words cyan, y 1176 | all reels (`caps()`) |
| VHS overlays | Scanlines, vignette, animated noise canvas, rolling bright band on footage | all reels |
| Channel-change static | Noise burst on every hard cut (`#burst`) | all reels |
| TV switch-off and end card | Screen collapses to a line, then a question + Discord pill + LINK IN BIO + disclaimer | all reels |

## Set pieces and where they've been used
| Piece | Description | Used in |
|---|---|---|
| LED dot-matrix board | Beveled panel with rivets. Text is drawn small offscreen, then each lit pixel becomes a round glowing LED | Anthropic (closing board), Nvidia (market board) |
| Win95 window | Teal title bar, grey bevel, chunky progress bars | Anthropic (ROTATION.EXE), Nvidia (NASDAQ-100.EXE with weight tiles) |
| CRT desk + screen canvas | `ant90_desk.png` with a 244x196 pixel canvas mapped onto the monitor, camera push-in, screen-off | Anthropic (teletext NQ line), Nvidia (candles, drawdown) |
| Teletext chart | Cyan header band, chunky pixel line, dotted reference lines | Anthropic |
| Drawdown battery or bar | Segmented battery that drains, or a bar next to a big candle | Anthropic, Nvidia |
| Company name tag | Boxed name + big glowing % + ticker line | Nvidia |
| Hook sticker | Rotated cyan circle sticker ("WED 8:30 AM ET") | PCE |
| Analog gauge | Metal panel with screws, semicircle dial, hatched zone, glowing target notch, needle with overshoot, digital readout | PCE (inflation gauge) |
| VFD register display | Cash-register vacuum fluorescent dot display. Blinking text, FORECAST / ACTUAL rows, hotter/softer lights | PCE |
| Split-flap board | Departure-board flaps that cycle characters and settle, with a clack sound per flap | PCE (release board) |
| Chart recorder | Scrolling graph paper, pen head drawing the line, labels that scroll with the paper, rubber-stamp slam | PCE (Nasdaq Fri/Mon) |

## Minimal chart pieces (single-stage explainer, not the 90s look)
| Piece | Description | Used in |
|---|---|---|
| Cheat-sheet grid cover | Title over a 2-2-1 grid of mini charts with labels; frame 1, the cover and the closing frame | 5 candlestick patterns |
| Candle-by-candle stage chart | Canvas candles (cyan up, grey down) with separate body and wick timing, plus capsule, box, ring, open/close tick-meet, dashed range lines and arrows that land on spoken words | 5 candlestick patterns |

## Not used yet (ideas for next time)
Fax machine printing a headline, pager or beeper message, rotary phone ringing with an on-screen caller ID, 7-segment calculator, dot-matrix printer tearing off a strip, cassette or VHS tape label for the title, newspaper spinning in, Rolodex card flip, stock-quote tape machine (ticker tape), weather-map-style heat map, old Bloomberg-style amber terminal.

## Sound per piece (in each `mix.py`)
Thud on the key number, synthesized static on cuts, LED count blips, register beeps, flap clacks, needle swish, pen scratch, CRT power-down. The music is Starlight Trail, about 12 dB under the voice and ducked 2 dB while it speaks.
