import os, subprocess, psutil
from pathlib import Path
from datetime import datetime
from flask import Flask, render_template, request, jsonify, Response, stream_with_context
import anthropic

app = Flask(__name__)
SCRIPTS = Path('/data/scripts')
LOGS    = Path('/data/logs')
SCRIPTS.mkdir(parents=True, exist_ok=True)
LOGS.mkdir(parents=True, exist_ok=True)
client = anthropic.Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))
MODEL  = os.environ.get('CLAUDE_MODEL', 'claude-sonnet-4-6')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

@app.route('/api/stats')
def stats():
    d = psutil.disk_usage('/data')
    return jsonify({
        'cpu': psutil.cpu_percent(0.5),
        'ram': psutil.virtual_memory().percent,
        'disk_used_gb': round(d.used/1e9, 2),
        'disk_total_gb': round(d.total/1e9, 2)
    })

@app.route('/api/scripts')
def list_scripts():
    return jsonify({'scripts': sorted([f.name for f in SCRIPTS.glob('*.py')])})

@app.route('/api/scripts/save', methods=['POST'])
def save():
    d = request.get_json()
    name = d.get('name', '').strip()
    if not name.endswith('.py'):
        name += '.py'
    (SCRIPTS / name).write_text(d.get('content', ''))
    return jsonify({'ok': True, 'name': name})

@app.route('/api/scripts/load/<name>')
def load(name):
    p = SCRIPTS / name
    return jsonify({'content': p.read_text()}) if p.exists() else ('', 404)

@app.route('/api/scripts/delete/<name>', methods=['DELETE'])
def delete(name):
    p = SCRIPTS / name
    if p.exists():
        p.unlink()
    return jsonify({'ok': True})

@app.route('/api/run/<name>')
def run(name):
    p = SCRIPTS / name
    if not p.exists():
        return jsonify({'error': 'ikke fundet'}), 404
    def gen():
        yield f'▶ Starter {name}...\n'
        proc = subprocess.Popen(
            ['python3', str(p)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        for line in proc.stdout:
            yield line
        proc.wait()
        yield f'\n✅ Afsluttet (kode {proc.returncode})\n'
    return Response(stream_with_context(gen()), mimetype='text/plain')

@app.route('/api/claude', methods=['POST'])
def claude():
    d = request.get_json()
    def gen():
        with client.messages.stream(
            model=MODEL,
            max_tokens=2048,
            system='Du er en Python-ekspert på en Raspberry Pi. Svar på dansk.',
            messages=d.get('messages', [])
        ) as s:
            for t in s.text_stream:
                yield t
    return Response(stream_with_context(gen()), mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
