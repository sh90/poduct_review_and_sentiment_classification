# AI Coding Assistant with Memory
### IDE 
Download Pycharm: https://www.jetbrains.com/pycharm/download/?section=windows or https://www.jetbrains.com/pycharm/download/?section=mac 

### How to use Pycharm
1. Open pycharm and create new project
 <img width="248" height="310" alt="image" src="https://github.com/user-attachments/assets/bddc76a3-f0b5-4c47-b74d-2a6be0dff2c9" />

2. Create Virtual env with python3.12
<img width="637" height="320" alt="image" src="https://github.com/user-attachments/assets/a338e946-785d-4caa-9d2e-6beb5a93a6b9" />



### Setup
1. Open Pycharm and create virtual environment using python3.12
2. `pip install -r requirements.txt`
3. [Get OpenAI API key](https://platform.openai.com/)
4. `set OPENAI_API_KEY="sk-..."`  in your .env
5. `streamlit run main.py`


### Features

- Codebase ingestion to chromadb vector store https://docs.trychroma.com/docs/overview/introduction, https://docs.trychroma.com/docs/overview/getting-started
- Search (RAG) : https://python.langchain.com/docs/concepts/rag/ and https://python.langchain.com/docs/how_to/code_splitter/
- Answers code queries, explains, or edits code
- Maintains chat and project context
- Lets you run or save code edits directly from the assistant

### Example queries
#generate code to identify emails from text paragraphs
