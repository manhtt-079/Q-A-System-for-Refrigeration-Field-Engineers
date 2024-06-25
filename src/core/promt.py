from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.prompts.chat import MessagesPlaceholder

prompt_search_query = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    ("user", "Given the above conversation, generate a search query to look up to get information relevant to the conversation")
])


prompt_get_answer = ChatPromptTemplate.from_messages([
    ("system", """You are an expert Refrigeration Field Engineers. Answer the user's questions based on the below context:\\n\\n{context}. 
     If the answer is not in provided context just say, "answer is not available in the context", don't provide the wrong answer"""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
])


if __name__ == "__main__":
    pass