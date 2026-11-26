# PCE data graph (26 Nov 2026)
- 14.0 s, music only: runaway.mp3 from Gabriel's trending-audio folder (licensed/trending, not in repo). aud/music.wav = the track extended to 14.0 s (extra bar copied at 6.13-8.92, 12 ms crossfades, 1.6 s fade).
- Beats: bars on the piano hits 1.32 / 2.72 / 4.09 / 5.46, drop at 6.13 (flash, shake, trend arrow, HIGHEST SINCE 2023 stamp), 8.92 gap bracket +1.8 pts, 11.70 end card.
- Data (BEA, 25 Nov): headline PCE y/y Jul 3.4%, Aug 3.5%, Sep 3.7% (revised), Oct 3.8%, highest since May 2023; Oct +0.3% m/m; core 3.3% y/y, highest since Nov 2023.
- Background: blurred aisle frames from the PCE 3-things reel (Pexels 29376327, see footage/stock/SOURCES.md).
- Master: volume 5.4 dB, alimiter 0.35, make-up 5.92 dB -> -13.7 LUFS, -2.8 dBTP.

## Variants (one per trending track, 26 Nov)
page.html is a template; build_var.sh <name> writes pce_<name>.html with window.CFG timings from variants.py, cuts the music, mixes and masters.
- runaway (14.0 s): bars 1.32/2.72/4.09/5.46, drop 6.13, gap 8.92, end 11.70
- brokenheart, "a good man with a broken heart" from 3.65 s (15.0 s): bars on the piano chords 1.68/2.71/4.30/5.32, drop on the beat drop 6.80, gap 9.92, end 12.53
- timeless from 1.85 s (15.0 s): bars on beats 2.07/3.08/4.08/5.08, drop on the bar accent 6.08, gap 9.08, end 12.09
- goodsax, "Good Sax End" whole track plus a 0.54 s reverb tail (10.6 s): bars 1.31/2.01/2.62/3.46, drop on the loudest sax stab 4.83, bracket 6.94 (no second kicker, stamp holds), end 8.62
SFX are set relative to the local music level (mix_var.py): bar blips -4 dB, drop thud -5, stamp -7, beeps -6, end thud -7. Master is adaptive: -14 LUFS, true peak about -3 dB.
Background frames now ping-pong (no jump when the 130-frame clip loops at 10.8 s).
