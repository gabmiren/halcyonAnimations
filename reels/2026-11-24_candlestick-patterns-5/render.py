"""Render frames from index.html via window.seek(t).
usage: render.py stills out_dir t1 t2 ...   |   render.py frames out_dir [workers]   |   render.py map out.json
"""
import sys, os, json, base64, math
from concurrent.futures import ProcessPoolExecutor
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
URL = 'file://' + os.path.join(HERE, 'page.html')
FPS = 30


def open_page(p):
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--allow-file-access-from-files', '--disable-web-security'])
    pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    pg.goto(URL)
    pg.evaluate('window.ready')
    return b, pg


def grab(pg, t, path):
    data = pg.evaluate(f"(window.seek({t}), document.getElementById('c').toDataURL('image/png'))")
    with open(path, 'wb') as f:
        f.write(base64.b64decode(data.split(',', 1)[1]))


def worker(args):
    out, frames = args
    with sync_playwright() as p:
        b, pg = open_page(p)
        for n in frames:
            grab(pg, n / FPS, os.path.join(out, f'f{n:05d}.png'))
        b.close()
    return len(frames)


if __name__ == '__main__':
    mode, out = sys.argv[1], sys.argv[2]
    if mode == 'map':
        with sync_playwright() as p:
            b, pg = open_page(p)
            json.dump(pg.evaluate('window.timelineMap()'), open(out, 'w'), indent=1)
            b.close()
    elif mode == 'stills':
        os.makedirs(out, exist_ok=True)
        with sync_playwright() as p:
            b, pg = open_page(p)
            for t in sys.argv[3:]:
                name, tt = t.split('=') if '=' in t else (t, t)
                grab(pg, float(tt), os.path.join(out, f'{name}.png'))
            b.close()
    else:
        os.makedirs(out, exist_ok=True)
        workers = int(sys.argv[3]) if len(sys.argv) > 3 else 4
        with sync_playwright() as p:
            b, pg = open_page(p)
            dur = pg.evaluate('TL.duration')
            b.close()
        n = round(dur * FPS)
        chunks = [list(range(i, n, workers)) for i in range(workers)]
        with ProcessPoolExecutor(workers) as ex:
            print(sum(ex.map(worker, [(out, c) for c in chunks])), 'frames', dur, 's')
