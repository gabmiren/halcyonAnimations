"""Final mix: Mark VO (stretched) + Starlight Trail bed ~16 dB under the voice + sparse SFX.
Loudnorm to -14 LUFS, limiter 0.76, short fade at the end. Audio exactly frames/30 long.
usage: mix_final.py n_frames out.wav"""
import json, subprocess, sys, re
NF = int(sys.argv[1]); OUT = sys.argv[2]
DUR = NF / 30
U = '/mnt/user-data/uploads/'
m = json.load(open('qa_map.json'))
L = {l['id']: l for l in m['lines']}
close = [s for s in m['sections'] if s['id'] == 'close'][0]


def lufs(path):
    o = subprocess.run(['ffmpeg', '-i', path, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', o)[-1])


subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '14', '-t', f'{DUR:.4f}', '-i', U + 'BGM/starlight trail.mp3', '-ar', '48000', '-ac', '2', 'audio/bed_raw.wav'], check=True)
vo_l, bed_l = lufs('vo/vo_fast.wav'), lufs('audio/bed_raw.wav')
bed_gain = (vo_l - 16.0) - bed_l
sfx = [('pop.mp3', L[i]['start'], -22.0) for i in ['h1', 'r1', 'e1', 'd1', 'i1']]
sfx += [('simplewhoosh.mp3', close['start'], -19.8), ('appClick.mp3', m['endcard']['start'], -18.0)]
ins = ['-i', 'vo/vo_fast.wav', '-i', 'audio/bed_raw.wav']
fl = ["[0]aresample=48000,aformat=channel_layouts=stereo[vo]",
      f"[1]volume={bed_gain:.2f}dB,afade=t=in:d=0.4,afade=t=out:st={DUR - 1.5:.3f}:d=1.5[bed]"]
labs = ['[vo]', '[bed]']
for n, (f, t, g) in enumerate(sfx, 2):
    ins += ['-i', U + '_originals/' + f]
    ms = int(round(t * 1000))
    fl.append(f"[{n}]aresample=48000,aformat=channel_layouts=stereo,volume={g}dB,adelay={ms}|{ms}[s{n}]")
    labs.append(f'[s{n}]')
fl.append(''.join(labs) + f"amix=inputs={len(labs)}:normalize=0:duration=longest,apad=whole_dur={DUR:.4f},atrim=0:{DUR:.4f},"
          f"loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000,alimiter=limit=0.76:level=false,afade=t=out:st={DUR - 0.4:.3f}:d=0.4[a]")
subprocess.run(['ffmpeg', '-v', 'error', '-y', *ins, '-filter_complex', ';'.join(fl), '-map', '[a]', '-ar', '48000', '-c:a', 'pcm_s16le', OUT], check=True)
print(f'vo {vo_l} LUFS, bed {bed_l} LUFS, bed gain {bed_gain:.1f} dB, dur {DUR}')
