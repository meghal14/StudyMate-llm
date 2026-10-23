"""Small, local Ollama client and study prompts (standard library only)."""
import json
import os
import socket
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

MODEL = os.getenv('STUDYMATE_MODEL', 'qwen2.5:0.5b')
OLLAMA_URL = 'http://127.0.0.1:11434'
MODES = {
    'explain': 'Explain the topic in simple English, give one everyday example, then three key points.',
    'notes': 'Write concise revision notes with a definition, key points and a short summary.',
    'quiz': 'Write exactly five short practice questions. Put a numbered answer key at the end.',
}

class ModelError(Exception):
    """A model failure that can be displayed to the student."""


def build_messages(data):
    if not isinstance(data, dict):
        raise ValueError('Send a JSON object.')
    topic = data.get('topic', '')
    mode = data.get('mode', 'explain')
    if not isinstance(topic, str) or not 1 <= len(topic.strip()) <= 1000:
        raise ValueError('Enter a topic or question between 1 and 1,000 characters.')
    if not isinstance(mode, str) or mode not in MODES:
        raise ValueError('Choose Explain, Revision notes, or Practice questions.')
    return [
        {'role': 'system', 'content': (
            'You are StudyMate, a patient college study assistant. '
            'Use simple English and plain text with short headings and numbered lists. '
            'Do not use Markdown tables. Be accurate; admit uncertainty. '
            'Do not invent references. Keep the answer under 350 words. ' + MODES[mode]
        )},
        {'role': 'user', 'content': topic.strip()},
    ]


def ollama_request(path, payload=None, timeout=180):
    body = None if payload is None else json.dumps(payload).encode('utf-8')
    request = Request(OLLAMA_URL + path, data=body, headers={'Content-Type': 'application/json'})
    try:
        with urlopen(request, timeout=timeout) as response:
            result = json.load(response)
        if not isinstance(result, dict):
            raise ValueError('Invalid response')
        return result
    except HTTPError as exc:
        if exc.code == 404:
            raise ModelError(f'Model not found. Run: ollama pull {MODEL}') from exc
        raise ModelError(f'Ollama returned HTTP {exc.code}. Check the Ollama application.') from exc
    except (TimeoutError, socket.timeout) as exc:
        raise ModelError('Generation timed out. Try a shorter question or close other applications.') from exc
    except URLError as exc:
        raise ModelError('Cannot reach Ollama. Open Ollama or run: ollama serve') from exc
    except (ValueError, UnicodeError) as exc:
        raise ModelError('Ollama returned an unreadable response. Please try again.') from exc


def generate(data):
    messages = build_messages(data)
    result = ollama_request('/api/chat', {
        'model': MODEL, 'messages': messages, 'stream': False,
        'options': {'temperature': 0.3, 'num_predict': 600, 'num_ctx': 4096},
    })
    message = result.get('message')
    answer = message.get('content') if isinstance(message, dict) else None
    if not isinstance(answer, str) or not answer.strip():
        raise ModelError('The model returned an empty answer. Please try again.')
    return {'answer': answer.strip(), 'model': MODEL,
            'truncated': result.get('done_reason') == 'length'}


def status():
    result = ollama_request('/api/tags', timeout=3)
    models = result.get('models', [])
    names = {m.get('name') for m in models if isinstance(m, dict)} if isinstance(models, list) else set()
    ready = MODEL in names or (':' not in MODEL and MODEL + ':latest' in names)
    return {'ready': ready, 'model': MODEL,
            'message': 'Model ready' if ready else f'Run: ollama pull {MODEL}'}
