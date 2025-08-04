# AI Coding Assistant with Memory

### Setup
1. Open Pycharm and create virtual environment using python3.12
2. `pip install -r requirements.txt`
3. [Get OpenAI API key](https://platform.openai.com/)
4. `set OPENAI_API_KEY="sk-..."`  in your .env
5. `streamlit run main.py`
6. Use the sidebar to ingest a project, then ask coding questions!

### Features

- Codebase ingestion & search (RAG)
- Answers code queries, explains, or edits code
- Maintains chat and project context
- Lets you run or save code edits directly from the assistant

### Example queries
#generate code to identify emails from text paragraphs
