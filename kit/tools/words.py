import sherpa_onnx, soundfile as sf, numpy as np, json
z="/home/claude/models/sherpa-onnx-zipformer-en-2023-06-26/"
zr=sherpa_onnx.OfflineRecognizer.from_transducer(encoder=z+"encoder-epoch-99-avg-1.int8.onnx",decoder=z+"decoder-epoch-99-avg-1.int8.onnx",joiner=z+"joiner-epoch-99-avg-1.int8.onnx",tokens=z+"tokens.txt",num_threads=2,decoding_method="modified_beam_search")
a,sr=sf.read('aud/vo16.wav',dtype='float32')
st=zr.create_stream(); st.accept_waveform(16000,np.concatenate([a,np.zeros(8000,np.float32)])); zr.decode_stream(st)
W=[]
for tk,t in zip(st.result.tokens,st.result.timestamps):
    if tk.startswith(('▁',' ')) or not W: W.append([tk.replace('▁','').strip().lower().replace("'",''),float(t)])
    else: W[-1][0]+=tk.lower().replace("'",'')
json.dump(W,open('heard.json','w'))
print(' '.join(f"{w}@{t:.2f}" for w,t in W))
