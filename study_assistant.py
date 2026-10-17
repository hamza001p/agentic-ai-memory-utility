from dotenv import load_dotenv
load_dotenv()
import os
from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver


@tool
def calculate_average(marks: list[float]) -> float:
    """Calculates the average of a list of marks."""
    if not marks:
        return 0.0
    return sum(marks) / len(marks)

@tool
def get_study_tips(subject: str) -> str:
    """Provides study tips for a given subject."""
    tips = {
        "math": "Practice problems daily and review your mistakes.",
        "science": "Conduct experiments and relate concepts to real life.",
        "history": "Create timelines and connect events to understand context.",
        "language": "Read extensively and practice writing regularly."
    }
    return tips.get(subject.lower(), "consistent practice is the key to success.")

@tool
def count_study_hours(hours: list[float]) -> float:
    """Counts the total study hours from a list of hours."""
    return sum(hours)
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

checkpoint = InMemorySaver()

agent = create_agent(
    model=llm,
    tools=[calculate_average, get_study_tips, count_study_hours],
    system_prompt="Tum aik madadgar study assistant ho",
    checkpointer=checkpoint,
)
    


config = {"configurable": {"thread_id": "ali101"}}

agent.invoke({
    "messages": [{"role": "user", "content": "Hi, mera name ali hai."}],
    
},
config=config,

)


result = agent.invoke({
    "messages": [{"role": "user", "content": "mera name kia hai."}]},
config=config,  

)

print(result["messages"][-1].content)

result = agent.invoke({
    "messages": [{"role": "user", "content": "mere marks hai 80,89,90,70- average nikalo,"

                  "or math k liye study tips do."}]},

config=config,)

print(result["messages"][-1].content)

result = agent.invoke({
    "messages": [{"role": "user", "content": "mere study hours hai 2,3,4,1- total hours nikalo."}]},
config=config,)

print(result["messages"][-1].content)
