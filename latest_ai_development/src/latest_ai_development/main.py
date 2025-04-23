#!/usr/bin/env python
import sys
import warnings
import os
from datetime import datetime
from dotenv import load_dotenv
from latest_ai_development.crew import LatestAiDevelopment
from langchain_groq import ChatGroq
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information
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


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "file_path": './papers/1912.01703v1.pdf',
        "topic": "AI LLMs"
    }
    try:
        LatestAiDevelopment().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        LatestAiDevelopment().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "file_path": './papers/1912.01703v1.pdf',
        "topic": "AI LLMs",
    }
    try:
        LatestAiDevelopment().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
