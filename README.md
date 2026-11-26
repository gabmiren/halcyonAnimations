# Halcyon animations library

Everything we make for Halcyon's 90s finance-TV reels lives here, so a new reel can start from what we already have. That covers footage, stills, voiceovers, set pieces and the build tools.

**Before you start a new reel**, check `kit/COMPONENTS.md` to see which set pieces earlier reels already used. Keep each new reel looking different within the same style.

## Folders

| Folder | What's in it |
|---|---|
| `footage/ai/` | Higgsfield video clips (Kling 3.0, 5 s, 9:16, silent). These are ours, so reuse them freely. |
| `footage/stock/` | Free stock clips. **These stay local and aren't committed, because the repo is public.** `SOURCES.md` lists the links and licences. |
| `images/ai/` | Higgsfield stills (GPT Image 2.6, 9:16). They're the start frames for the clips, and some are backdrops (the CRT desk, for example). |
| `audio/voiceovers/` | Mark voice (Eleven v4 via Higgsfield), the raw files before speed-up. |
| `audio/music/`, `audio/sfx/` | Local only (licensed). See the README in each. |
| `kit/` | Fonts (Poppins, OFL), build tools and the component catalogue. |
| `reels/<date>_<slug>/` | One folder per reel: `page.html` (the animation), `tl.js` (caption timing), `mix.py` (sound design), `prep.sh` (rebuilds graded frames), `final.mp4`, `cover.jpg`, `notes.md`. |

## Asset catalogue

### AI footage (`footage/ai/`)
| File | What it shows | Made | Used in |
|---|---|---|---|
| `ant90_pit.mp4` | 90s futures trading pit, crowd shouting, paper slips | 20 Nov, Kling 3.0 std | Anthropic IPO (hook) |
| `ant90_street.mp4` | Night street, glowing restaurant with a queue, dark shops either side | 20 Nov, Kling 3.0 std | Anthropic IPO (analogy) |
| `nvh_room.mp4` | Trading room cheering at amber/cyan quote boards | 23 Nov, Kling 3.0 std | Nvidia (behind the LED board) |
| `nvh_chip.mp4` | Macro GPU chip on a green board, light sweep, fan spinning | 23 Nov, Kling 3.0 std | Nvidia (hook) |

### AI stills (`images/ai/`)
| File | What it shows | Used in |
|---|---|---|
| `ant90_pit.png` | Trading pit still (also the blurred backdrop) | Anthropic, Nvidia |
| `ant90_street.png` | Restaurant queue street still | Anthropic |
| `ant90_desk.png` | Trader's desk at night, beige CRT facing camera with a blank screen. The screen sits at x 327, y 536, 489 x 393 on a 1080 canvas | Anthropic, Nvidia |
| `nvh_room.png` | Trading room with quote boards | Nvidia |
| `nvh_chip.png` | GPU chip close-up | Nvidia |

### Free stock (`footage/stock/`, local only)
| File | Source | Used in |
|---|---|---|
| `pexels_29376327_aisle.mp4` | Pexels 29376327, supermarket aisle POV with cart, no people | PCE (hook, backgrounds) |
| `pexels_29068393_cart.mp4` | Pexels 29068393, cart-handle POV through an aisle | PCE (backgrounds) |

### Voiceovers (`audio/voiceovers/`)
| File | Reel | Speed used |
|---|---|---|
| `2026-11-20_anthropic-ipo_mark.mp3` | Anthropic IPO | 1.0x |
| `2026-11-23_nvidia-huang-back_mark.mp3` | Nvidia / Huang back | 1.07x |
| `2026-11-25_pce-3-things_mark.mp3` | PCE 3 things | 1.10x |
| `2026-11-24_candlestick-patterns-5_mark.mp3` | 5 candlestick patterns | pauses stretched, then 1.10x |

## Reels
| Reel | Posted | Length | Credits | Set pieces |
|---|---|---|---|---|
| `2026-11-20_anthropic-ipo` | Fri 20 Nov, 8 PM MYT | 35 s | 24.03 | LED closing board, ROTATION.EXE window, CRT desk teletext chart, drawdown battery |
| `2026-11-23_nvidia-huang-back` | Tue 24 Nov, 12:40 AM MYT | 37 s | 28.52 | NVIDIA ▲33% tag, LED board, NASDAQ-100.EXE window, CRT candles, drawdown bar |
| `2026-11-25_pce-3-things` | planned Wed 25 Nov, 7 AM ET | 38.6 s | ~3 (voice only) | Hook sticker, inflation gauge, VFD register display, split-flap board, chart recorder + stamp |
| `2026-11-26_pce-data-graph` | draft, not scheduled | 10.6 to 15 s (4 audio variants) | 0 | Phosphor terminal bar chart, kicker-slot stamp; trending audio (runaway.mp3, local only) |
| `2026-11-24_candlestick-patterns-5` | Tue 24 Nov, 8 PM MYT | 59.9 s | 0 (ElevenLabs voice from Gabriel) | Not 90s style: single-stage candle chart explainer, cheat-sheet grid cover, word-by-word captions on top |

## Build a reel (summary)
1. Copy the closest reel folder, then write the script and get the voice (Higgsfield `elevenlabs_v4`, Mark preset `27c04473-84a9-4b60-a41f-c8e8458bd4f1`).
2. Put footage in `footage/`. Then grade it: `kit/tools/grade.sh hook|blur|still <in> <out>`.
3. Word times: `python3 kit/tools/words.py` (needs the sherpa-onnx zipformer model). Then `make_tl.py` builds `tl.js`.
4. Edit `page.html` (everything is driven by `window.seek(t)`). Check stills with `node kit/tools/snap.js page.html snaps 0.5 3 ...`.
5. Render with `bash kit/tools/go.sh page.html <seconds> 6` (Playwright, 1080x1920, 30 fps). Then run `python3 mix.py aud/mix_pre.wav` followed by `bash kit/tools/master.sh <video> <out>`. Target -14 LUFS, true peak ≤ -2 dB.
6. QA: `qa2.py` (stills per scene, strips at every cut), `qa_tx.py` (transcript diff), plus the ffmpeg black, freeze, scene and silence sweeps.

The style rules are dark grounds only, cyan `#00FBF4` as the one accent, Poppins, and no emojis on graphics. AI and stock footage always goes through the VHS grade. The 1080x1920 safe zone is x 60–940, y 250–1470.
