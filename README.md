# crewai-groq


https://github.com/user-attachments/assets/bc0c51d0-c6d9-42ae-8550-54938b6a1aca


Given a link to a pdf, 

summarize the thing and provide quotes that may pertain to your topic.

https://openaccess.thecvf.com/content_CVPR_2020/papers/He_Momentum_Contrast_for_Unsupervised_Visual_Representation_Learning_CVPR_2020_paper.pdf

pip install beautifulsoup4 requests groq 

## How to install Crew AI

install UV to get crew
mac
curl -LsSf https://astral.sh/uv/install.sh | sh

windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

(then make a new terminal to refresh it)

cd latest_ai_development folder

## install crew

cd latest_ai_development
uv tool install crewai
uv pip install langchain-groq python-dotenv
pip install 'crewai[tools]'
crewai run

note: also maybe have a chat agent

source .venv/bin/activate (optional, if you want a virtual env)

this crewai chatgpt assistant was helpful: https://chatgpt.com/g/g-qqTuUWsBY-crewai-assistant
