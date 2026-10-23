# StudyMate — Small Language Model Study Assistant

A simple college mini-project that turns a topic into an explanation, revision notes, or practice questions. A clean cream-and-green browser interface talks to a small model running locally through Ollama.

**Stack:** Python 3.10+ · HTML/CSS/JavaScript · Ollama · Qwen2.5 0.5B

## Features

- Simple explanations with examples.
- Concise revision notes.
- Five practice questions with an answer key (model output may vary).
- Download answers as text files.
- Local model status and useful setup/error messages.
- No API key, paid API, or third-party Python packages.

This is an **application using a pretrained small language model**. It does not train a new LLM or fine-tune weights. The optional Modelfile customizes instructions only. Model weights are downloaded by Ollama, not stored in GitHub.

## Quick start

1. Install [Python](https://www.python.org/downloads/) 3.10+ and [Ollama](https://ollama.com/download). On Windows, select **Add Python to PATH**.
2. Open Ollama. If needed, run `ollama serve` in a separate terminal. An address-in-use message can mean Ollama is already running.
3. Download the model once:

   ```sh
   ollama pull qwen2.5:0.5b
   ```

4. Download this repository using **Code → Download ZIP** and extract it, or clone:

   ```sh
   git clone https://github.com/meghal14/LLM-tae2.git
   cd LLM-tae2
   ```

5. In the folder containing `app.py`, run:

   ```sh
   python app.py
   ```

   On macOS/Linux, use `python3 app.py` if needed. No pip installation is required.
6. Open **http://127.0.0.1:8000**, choose a mode, and enter a topic.

Internet is needed for initial downloads. After installation, the app calls local Ollama only. Keep Ollama running. Response speed and memory use depend on your laptop; the first response may take longer while the model loads.

## Demo topics

- Explain primary keys and foreign keys with an example.
- Object-oriented programming: classes, objects, inheritance and polymorphism.
- SQL joins for a beginner.

Try each mode, then click **Save .txt**. Each question starts fresh; no conversation memory or saved answer history is used. Reloading clears the displayed result.

## Architecture

The browser sends a topic and mode to Python. The backend validates input, constructs a system instruction and user message, calls Ollama's `/api/chat`, then returns the generated text to the browser. Text is displayed safely without interpreting it as HTML.

| File | Purpose |
|---|---|
| `app.py` | Local HTTP server and routes |
| `llm.py` | Prompt design, validation, Ollama calls and errors |
| `static/index.html` | Page structure |
| `static/style.css` | Responsive interface |
| `static/script.js` | Submission, model status and download |
| `Modelfile` | Optional custom model instructions |
| `tests/test_app.py` | Unit and HTTP integration tests |
| `VIVA.md` | Presentation introduction and viva answers |

## Optional named model

From the project folder:

```sh
ollama create studymate -f Modelfile
```

Run the app using it:

Windows PowerShell:

```powershell
$env:STUDYMATE_MODEL="studymate"
python app.py
```

macOS/Linux:

```sh
STUDYMATE_MODEL=studymate python3 app.py
```

This does not retrain Qwen. The application also supplies task-specific instructions with each request.

## Testing

```sh
python -m unittest discover -s tests -v
```

Tests cover inputs, all prompt modes, model response parsing, connection errors, missing models, HTTP requests and static routes. They mock Ollama and do not measure model accuracy.

For a live smoke test, install the model and generate an answer in each mode. Check relevance, the text download, and the error shown when Ollama is stopped. Live inference was not tested in the development environment because Ollama and model weights were unavailable.

## Troubleshooting

| Problem | Fix |
|---|---|
| Cannot reach Ollama | Open Ollama or run `ollama serve` |
| Model missing | Run `ollama pull qwen2.5:0.5b`, then Recheck |
| Python not found | Try `py app.py` on Windows or `python3 app.py` on macOS/Linux |
| Port busy | Run `python app.py --port 8001`, then open that port |
| Slow output | Close other apps and wait for the model to load |
| Incomplete answer | Ask a narrower question; generation is limited to 600 tokens |
| Wrong answer | Check class notes; small language models have limited accuracy |

## Limitations

Local educational prototype, not a production web service. The server binds to your machine only. There is no authentication, database, document retrieval, web search, fine-tuning, or multi-agent system. The app does not save questions or answers. Small models can make factual errors or fail to follow a requested format. Review generated study material.

## References

- [Ollama documentation](https://docs.ollama.com/)
- [Ollama chat API](https://docs.ollama.com/api/chat)
- [Qwen2.5](https://github.com/QwenLM/Qwen2.5)
- [Qwen2.5 on Ollama](https://ollama.com/library/qwen2.5)
- Scope inspiration: [AI Gym Diet Planner](https://github.com/Bhavya-wq/Diet-Planner-AI-Model). StudyMate is an independent implementation and does not copy its code.
