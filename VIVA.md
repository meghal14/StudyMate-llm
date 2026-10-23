# StudyMate — Presentation and Viva

## Short introduction

Good morning. My project is StudyMate, an AI study assistant built using Python and a small language model. Students enter a topic to get a simple explanation, revision notes, or practice questions. The model runs locally through Ollama, so the app does not need a paid API key. My work includes the interface, prompt design, backend integration, input validation, and testing.

## Common questions

**What problem does it solve?**
It helps students understand, revise, and practice difficult topics in one simple interface.

**Which model do you use?**
Qwen2.5 0.5B, a small pretrained language model, through Ollama. Its small size suits a basic local demo, but limits answer quality.

**Did you train it?**
No. I integrated a pretrained model and designed study prompts. Training changes model weights; prompting gives instructions during inference.

**What is Ollama?**
Software for running compatible language models locally. My backend communicates with its API.

**Explain the flow.**
The browser sends a topic and mode. Python validates them and constructs messages. Ollama runs the model and returns text. The browser displays it.

**What is a system prompt?**
An instruction describing the assistant's role, answer style, and task. The user message contains the actual question.

**What is temperature?**
A setting controlling randomness. This project uses 0.3 to encourage consistency. Low temperature does not guarantee correctness.

**What is a token?**
A text unit used by the model, such as a word, part of a word, or punctuation. Output is limited to 600 tokens here.

**Is this RAG or a multi-agent system?**
No. It uses one model directly. There is no retrieval of documents and no coordination of multiple agents.

**Why Python?**
It is readable and has built-in support for HTTP, JSON, API requests and testing. This backend needs no extra Python packages.

**What are its limitations?**
Incorrect answers, variable speed, limited instruction-following, no live web information, and no conversation memory. Important answers need verification.

**How did you test it?**
Automated tests check input validation, prompts, model errors, and HTTP integration with mocked model responses. Live answer quality must be checked separately on a machine with Ollama installed.

**What can you improve later?**
Retrieval from class notes, conversation history, streaming, a reviewed evaluation dataset, or a larger model if hardware allows.

## Demonstration

Start Ollama and the app before presenting. Explain a database topic, generate revision notes, then practice questions. Download an answer. Show `llm.py` for prompt design and `app.py` for backend integration. Explain clearly that the pretrained model is reused and the application is your project contribution.
