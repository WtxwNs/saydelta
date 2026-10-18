"""Download public model files with bounded retries; never disable TLS checks."""
import concurrent.futures
import pathlib
import urllib.request

FILES = {
    'kokoro/kokoro-v1.0.onnx': 'https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx',
    'kokoro/voices-v1.0.bin': 'https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin',
    **{f'small.en/{name}': f'https://huggingface.co/Systran/faster-whisper-small.en/resolve/main/{name}?download=true' for name in ['config.json','model.bin','tokenizer.json','vocabulary.txt']},
}

def download(item):
    name, url = item
    target = pathlib.Path('.models', name)
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        return f'Already downloaded: {name}'
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=20) as src, target.with_suffix('.download').open('wb') as dst:
                total = 0
                while chunk := src.read(1024 * 1024):
                    dst.write(chunk)
                    total += len(chunk)
                length = src.headers.get('Content-Length')
                if length and int(length) != total:
                    raise RuntimeError(f'Incomplete transfer: {total}/{length}')
            target.with_suffix('.download').replace(target)
            return f'Downloaded {name}: {total} bytes'
        except Exception as exc:
            print(f'{name}: attempt {attempt+1} failed: {exc}', flush=True)
    return f'FAILED: {name}'

if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for result in pool.map(download, FILES.items()):
            print(result, flush=True)
