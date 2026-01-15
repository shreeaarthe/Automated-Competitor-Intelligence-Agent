# Code Modernizer Agent

An intelligent agent that migrates legacy code (Java -> Python) and automatically fixes syntax errors using a self-correcting feedback loop.

## 🚀 Features

- **Automated Translation**: Converts Java code to Python using Groq Llama 3.3.
- **Self-Healing**: If the generated code has syntax errors, the agent detects them and retries the translation with error context.
- **Syntax Validation**: Uses `py_compile` (and optionally `pylint`) to ensure code validity.

## 🛠️ Tech Stack

- **LangGraph**: Orchestrates the cyclic workflow (Translate -> Review -> Fix).
- **Groq (Llama 3)**: High-speed LLM for code generation.
- **Python**: Core runtime.

## ⚡ Installation

1. Navigate to the project folder:
   ```bash
   cd code-modernizer
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure API Key:
   Ensure `.env` contains your `GROQ_API_KEY`.

## ▶️ Usage

1. Run the agent:
   ```bash
   python main.py
   ```
2. Paste your Java code snippet.
3. Press `Ctrl+Z` then `Enter` (Windows) or `Ctrl+D` (Linux/Mac) to submit.
4. The agent will output the migrated Python code.

## 🔄 Workflow

1. **Translator Node**: Converts input code to target language.
2. **Reviewer Node**: Checks for syntax errors.
3. **Loop**: If errors found -> Send back to Translator with error message -> Repeat (max 3 times).
