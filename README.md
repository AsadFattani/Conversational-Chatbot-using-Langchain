# Conversational Chatbot Using LangChain

A Streamlit-based conversational chatbot powered by Google Gemini and LangChain, with a British-style persona and a custom red-themed chat UI.

## Current Context

This project includes:

- Streamlit chat interface with a styled, red-gradient UI
- Gemini model picker in the sidebar (models are fetched from your key)
- Enter-to-send chat form behavior
- British-slang personality system prompt
- Structured response cleanup (shows user-facing text and hides model "thinking" blocks)

## Tech Stack

- Python
- Streamlit
- LangChain (`langchain`, `langchain-core`)
- Google Gemini (`langchain-google-genai`)
- `python-dotenv` for local key loading

## Project Structure

```
app.py
README.md
requirements.txt
LICENSE
```

## Setup

1. Clone the repository:

```bash

```

2. Create and activate a virtual environment.

PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Add your Gemini API key in a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_api_key_here
```

5. Run the app:

```bash
streamlit run app.py
```

## How To Use

1. Pick a model from the sidebar (if available for your API key).
2. Type your message in the input box.
3. Press Enter or click Send.
4. Read the chatbot response in the message area.

## Notes

- If the app says API key is missing, verify `GOOGLE_API_KEY` (or `GEMINI_API_KEY`) is set.
- Some Gemini models can return structured output. The app now extracts and displays only the final readable text.
- The model list depends on what your current API key can access.

## Contributing

Contributions are welcome. Feel free to fork the repo and open a pull request.

## License


