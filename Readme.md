# AI Coding Assistant with Memory

### Setup
0. Open Pycharm and create virtual environment using python3.12
1. `pip install -r requirements.txt`
2. [Get OpenAI API key](https://platform.openai.com/)
3. `set OPENAI_API_KEY="sk-..."`  in your .env
4. `streamlit run main.py`
5. Use the sidebar to ingest a project, then ask coding questions!

### Features

- Codebase ingestion & search (RAG)
- Answers code queries, explains, or edits code
- Maintains chat and project context
- Lets you run or save code edits directly from the assistant

### Example queries
#generate code to identify emails from text paragraphs
