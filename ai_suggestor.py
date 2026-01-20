from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.messages import HumanMessage
import os
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

endpoint = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-Coder-7B-Instruct",
    huggingfacehub_api_token=HF_TOKEN,
    temperature=0.7,
    max_new_tokens=500
)

llm = ChatHuggingFace(llm=endpoint)

def generate_ai_suggestion(code: str) -> str:
    if not code.strip():
        return "No code provided."

    prompt  = f"""
I am new to Python. Please check my code and give a short, clear, and stand-alone suggestion:


- List only mistakes or issues in the code
- Suggest simple improvements
- Explain each mistake in 1 line
- Use bullet points
- Keep it very short and easy to read
- give me the ai suggested code for imporved version of my code
Explain Why Suggestions Were Made: for examples-
Not just: “Remove unused import”
But: “Unused imports increase memory usage and reduce code readability.”
Follow the PEP8 standard coding guidelines for Coding Style Analysis: ●	Highlight issues like improper indentation, naming conventions, or long functions.
●	Score submissions based on style compliance


Code:
{code}

"""

    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content.strip() if response.content else "AI returned no response."



def chat_with_ai(previous_suggestion: str, user_question: str) -> str:
    if not user_question.strip():
        return "Please enter a question."


    prompt = f"""
    Previous AI suggestion:
{previous_suggestion}

I have a question:
{user_question}


Explain in 1-2 short sentences, very simple and easy to read.
"""



    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content.strip() if response.content else "AI returned no response."



