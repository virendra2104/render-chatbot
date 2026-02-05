from backend.agent.tools import search_academy_knowledge, web_search

print("---- FAISS TEST ----")
print(search_academy_knowledge("What does Blismos Academy teach?"))

print("\n---- WEB TEST ----")
print(web_search("What is weather today?"))
