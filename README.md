# Multi-Agent Research Paper Assistant with CrewAI + Groq
**Summarize any PDF and interact with it through chat — powered by Groq + CrewAI.**

https://github.com/user-attachments/assets/bc0c51d0-c6d9-42ae-8550-54938b6a1aca


Built with [CrewAI](https://github.com/joaomdmoura/crewai) and [Groq](https://console.groq.com), this multi-agent research assistant:
- Extracts the raw content of a paper (PDF)
- Generates a readable, structured **summary**
- Extracts and evaluates **key quotes** related to your topic
- Lets you **ask questions about the paper** through an LLM-powered CLI chatbot

## Prerequisites

- Python 3.10+
- A [Groq API key](https://console.groq.com/)
- `uv` (recommended for installing CrewAI)
- A PDF to analyze

---


# File Structure Overview:

- `agents.yaml` and `tasks.yaml` define the Agents' roles and their tasks.
- `crew.py` initializes the agents and tasks from the .yaml files
- `main.py` runs the Agent Crew and the LangChain + Groq Chatbot. 
- `/tools`  is where custom tools agents can use can be created
- `/papers` is where the .pdf file(s) is stored.


```
.
├── config/
│   ├── agents.yaml     # Define your agents and their roles/goals
│   └── tasks.yaml      # Define what each agent should do
├── tools/
│   └── custom_tool.py  # PDF text extractor using PyPDF
├── crew.py             # Creates the Crew using the information in the .yaml files
├── main.py             # Runs the full agent workflow, and chat command line interface afterwards
├── papers/
│   └── your-pdf.pdf    # Where your input paper lives
├── .env                # Stores your GROQ_API_KEY
├── .env.example        # Template
├── requirements.txt
├── README.md
│
│   # Will be made after running the crew:
├── summary.md          # Auto-generated summary of paper
├── quotes_raw.md       # Initial selected quotes
├── quotes_rated.md     # Rating each quote
├── quotes_final.md     # Final selected quotes, sorted by rating
└── 
```



# How it works

### agents.yaml
- Define your agents and their roles/goals

```
pdf_to_txt:
  role: >
    PDF to text
  goal: >
    Extract the words from the pdf file.
  backstory: >
    You are a detail-oriented agent that grabs the all of the text from the pdf file.
  llm: groq/meta-llama/llama-4-scout-17b-16e-instruct

reader_summarizer:
  role: >
    {topic} Summarizer
  goal: >
    Extract key insights from research papers and generate concise yet informative summaries, making complex ideas accessible.
  backstory: >
    You are a detail-oriented researcher with a talent for distilling vast amounts of information into clear, structured summaries. 
    Your ability to highlight crucial findings helps researchers and professionals quickly grasp essential knowledge.
  llm: groq/meta-llama/llama-4-scout-17b-16e-instruct

# ...more agents
```

### tasks.yaml
- Define what each agent should do
```
pdf_to_txt_task:
  description: >
    Extract and return all the text content from the PDF file located at {file_path}.
  expected_output: >
    A string containing the full extracted text from the PDF file. This should be a clean and accurate representation of the document content, with all readable text included.
  agent: pdf_to_txt

summary_task:
  description: >
    Summarize the content of the research paper that was extracted in the previous task.
    Focus on key insights, main arguments, and findings. Return it in structured markdown format.
  expected_output: >
    A well-organized summary covering the main points, key findings, and essential takeaways 
    from the research papers, formatted in markdown.
  context:
    - pdf_to_txt_task
  agent: reader_summarizer

# ...more tasks
```

### custom_tool.py
- Custom created CrewAI tool for PDF text extraction using PyPDF

```
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from pypdf import PdfReader
from pathlib import Path
import os

class PDFToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    file_path: str

class PDFTool(BaseTool):
    name: str = "PDFTool"
    description: str = (
        "Get all the text from a PDF file."
    )
    args_schema: Type[BaseModel] = PDFToolInput
    # args_schema: type[BaseModel] = PDFToolInput

    def _run(self, **kwargs) -> str:
        file_path = kwargs.get("file_path")
        print(f"DEBUG: Processing PDF at {file_path}")  # Debugging
        print(f"Current working directory: {os.getcwd()}")
        # Load the PDF
        print("file_path", file_path)
        resolved_path = Path(file_path).resolve()
        print("resolved_path", resolved_path)
        reader = PdfReader(str(resolved_path))
        
        # Extract text from all pages
        text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
        print("Text extracted and returned")
        print(text)
        return text.strip()
```

### crew.py
- Creates the Crew using the information in the .yaml files
```
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from latest_ai_development.tools.custom_tool import PDFTool

@CrewBase
class LatestAiDevelopment():
    """LatestAiDevelopment crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml' 

    @agent
    def pdf_to_txt(self) -> Agent:
        return Agent(
            config=self.agents_config['pdf_to_txt'],
            verbose=True,            
            tools=[PDFTool()]
        )
    
    @agent
    def reader_summarizer(self) -> Agent:
        return Agent(
            config=self.agents_config['reader_summarizer'],
            verbose=True
        )

# ...more agents defined

    @task
        def pdf_to_txt_task(self) -> Task:
            return Task(
                config=self.tasks_config['pdf_to_txt_task']
                # output_file='./papers/output.txt'
            )
        
        @task
        def summary_task(self) -> Task:
            return Task(
                config=self.tasks_config['summary_task'],
                output_file='summary.md'
            )

# ...more tasks defined

        @crew
        def crew(self) -> Crew:
            """Creates the LatestAiDevelopment crew"""
            # To learn how to add knowledge sources to your crew, check out the documentation:
            # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

            return Crew(
                agents=self.agents, # Automatically created by the @agent decorator
                tasks=self.tasks, # Automatically created by the @task decorator
                process=Process.sequential, # the order in which you make the tasks matter
                verbose=True,
                # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
            )
        
        # note that this chat agent takes place after the quote extraction crew
        @agent
        def chat_analyst(self) -> Agent:
            return Agent(
                config=self.agents_config['chat_analyst'],
                verbose=True
            )

```

### main.py
- Runs the full agent workflow, and chat command line interface afterwards
```
import sys
import warnings
import os
from datetime import datetime
from dotenv import load_dotenv
from latest_ai_development.crew import LatestAiDevelopment
from langchain_groq import ChatGroq
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")
load_dotenv()

def run():
    """
    Run the crew.
    """
    inputs = {
        "file_path": 'src/latest_ai_development/papers/1912.01703v1.pdf', # Change the pdf name if needed
        'topic': 'AI LLMs' # Change the topic/argument you want to search for in the PDF
    }
    print("DEBUG: Inputs passed to kickoff:", inputs)  # Debugging
    
    try:
        
        # Step 1: Run the Crew
        LatestAiDevelopment().crew().kickoff(inputs=inputs) 

        # Step 2: Launch interactive chat
        print("\n🎤 Crew run complete! Starting interactive chat...\n")

        llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model_name=os.getenv("MODEL")
        )
                
        context = {
            "summary": open("summary.md").read(),
            "quotes": open("quotes_final.md").read()
        }

        # Format the context into a base prompt
        base_prompt = (
            "You are an expert assistant familiar with the following research paper.\n\n"
            "### Summary:\n"
            f"{context['summary']}\n\n"
            "### Quotes:\n"
            f"{context['quotes']}\n\n"
            "Answer the user's questions clearly and helpfully using this information.\n"
        )

        while True:
            user_input = input("🧑‍💻 Ask a question: ")
            if user_input.lower() in ["exit", "quit"]:
                print("👋 Exiting chat.")
                break

            prompt = base_prompt + f"\nUser: {user_input}\nAssistant:"
            response = llm.invoke(prompt)
            print(f"\n🤖 {response.content.strip()}\n")
            
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

```


# Installation Instructions

## 1. Clone the Repo

```bash
git clone https://github.com/cho-groq/crewai-groq
cd crewai-groq/src/latest_ai_development
```

## 2. Install UV Package Manager (to get CrewAI cleanly)

🖥️ macOS/Linux

`curl -LsSf https://astral.sh/uv/install.sh | sh`

🪟 Windows (PowerShell)

`powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`

Then restart your terminal.

### 3. Install Python Dependencies
```
uv tool install crewai
uv pip install 'crewai[tools]' langchain-groq python-dotenv beautifulsoup4 requests
```


# How to Run it

Go into the `latest_ai_development` folder:

`cd latest_ai_development`

Make sure the .pdf file name in `main.py`'s `run` function matches the file name in the /papers folder, and the essay topic is relevant to your essay.
```
def run():
    """
    Run the crew.
    """
    inputs = {
        "file_path": 'src/latest_ai_development/papers/1912.01703v1.pdf', # <----- Change the pdf name
        'topic': 'AI LLMs' # <-----  Change the topic/argument you want to search for in the PDF
    }
```

From inside the `src/latest_ai_development` folder, run this command:

`crewai run`


## Resources

GitHub Repo: https://github.com/cho-groq/crewai-groq
CrewAI ChatGPT Assistant: https://chatgpt.com/g/g-qqTuUWsBY-crewai-assistant