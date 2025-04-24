from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import OllamaLLM

# Testing locally the deepseek-r1 (7B) model
llm = OllamaLLM(model="deepseek-r1")

response = llm.invoke("Write a linear regression using only numpy in python.")
print(response)

for chunk in llm.stream("Who are you?"):
    print(chunk, end="|")