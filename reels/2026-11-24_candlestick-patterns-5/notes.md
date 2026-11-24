# 5 candlestick patterns every trader should know

Posted Tue 24 Nov 2026, 8:00 PM MYT (7:00 AM ET), Instagram Reel and TikTok. 59.9 s, 1080x1920, 30 fps, -14.3 LUFS.

## What it is
A minimal single-stage chart explainer modelled on @itrades.capital's "5 most important SMC concepts" (77.5K views, 5.1% saves). It deliberately does not use the 90s finance-TV look:
- **Frame 1 is the cheat sheet:** title over a grid of all five patterns. It doubles as the cover, and the same grid returns at the close so people save it.
- **One chart per pattern on one stage,** drawn candle by candle (mixed up and down candles into each pattern). Labels, boxes, rings and arrows land on the spoken word.
- **Word-by-word captions at the top,** key term cyan. Section titles ("1. Hammer") land on the spoken name.
- **No logo until the end card** (Gabriel's call, 24 Nov). The end card is logo_full, Discord pill, LINK IN BIO and the disclaimer. It's the only hard cut.
- Order: hammer, shooting star, engulfing, doji, inside bar.

## Files
- `page.html`, `timing.js`, `reel.js`: the animation, driven by `window.seek(t)`. `vo_words.js` holds the word times (absent, it times a no-VO draft at 150 wpm with 0.5 s holds).
- `tl.json`: the word times for the final (1.1x).
- `align.py`: word timing for the VO. Silence-segmented sherpa-onnx zipformer (gigaspeech) ASR with neighbour-chunk context, phrase starts snapped to the pause ends, a minimum word gap, extra pause at section breaks and after lines short of reading time, and it writes the stretched VO.
- `render.py`: Playwright frames (`frames out_dir 5`, `stills`, `map`).
- `mix.py`: VO + Starlight Trail about 16 dB under + sparse SFX (pop on each title, simplewhoosh at the grid return, appClick on the end card), loudnorm -14, limiter 0.76, 0.4 s fade.
- Voice: `audio/voiceovers/2026-11-24_candlestick-patterns-5_mark.mp3` (raw, ElevenLabs Mark). Final = pauses stretched (0.3 s per section break plus per-line reading-time gaps) then atempo 1.1.

## Lessons
- Mark's natural pauses are too short for the reading-time rule on word-by-word captions. The 65 s cut that met the rule needed about 4.5 s of added pauses. Gabriel then asked for 10% faster, and 12 of 17 lines are now 0.01 to 0.40 s under the rule.
- The transducer stamps the first word after a pause inside the pause. Snap it to the pause end (silencedetect -38 dB), or captions run up to 0.4 s early.
- Dark-to-dark hard cuts don't register in scene detection above about 0.08.

## Reuse
Candle chart drawing (candles with separate body and wick timing, capsule, box, ring, tick-meet, dashed hline, arrows) is all in `reel.js` (`drawCandle`, `drawAnn`). Good base for the "chart patterns traders should know" series.
