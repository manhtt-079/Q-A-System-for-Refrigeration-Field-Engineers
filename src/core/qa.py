from typing import Union
import streamlit as st

from langchain_openai import ChatOpenAI
from langchain_core.messages.ai import AIMessage
from langchain_core.messages.human import HumanMessage
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents.stuff import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever

from config.config import OpenAIConfig, ChatConfig, get_logger
from core.promt import prompt_search_query, prompt_get_answer
from core.template import user_template, bot_template, css
from core.embed import Embedding

logger = get_logger()
class QA:
    def __init__(self) -> None:
        self.chat_config = ChatConfig()
        self.openai_config = OpenAIConfig()
        self.embedding = Embedding()
        
        logger.info('Loading the embeddings')
        self.retriever = self.embedding.load_faiss().as_retriever(
            search_kwargs={"k": 5}
        )
        
        self.llm = ChatOpenAI(
            model=self.openai_config.chat_model,
            api_key=self.openai_config.api_key,
            max_retries=self.openai_config.max_retries,
            temperature=self.openai_config.temperature
        )
        
        retriever_chain = create_history_aware_retriever(
            llm=self.llm, 
            retriever=self.retriever, 
            prompt=prompt_search_query
        )
        document_chain = create_stuff_documents_chain(
            llm=self.llm,
            prompt=prompt_get_answer
        )
        
        self.retrievel_chain = create_retrieval_chain(
            retriever=retriever_chain,
            combine_docs_chain=document_chain
        )

    def oneturn_chat(self, question: str, chat_history: list[Union[HumanMessage, AIMessage]] = []):
        response = self.retrievel_chain.invoke({'chat_history': chat_history, 'input': question})
        
        if len(chat_history) > self.chat_config.max_history*2:
            chat_history = chat_history[-self.chat_config.max_history:]
            
        chat_history.append(HumanMessage(content=response['input']))
        chat_history.append(AIMessage(content=response['answer']))
        
        return response['answer'], chat_history

    def console_chat(self):
        logger.info("Chat with your own PDFs (type `exit` to quit the chat)")
        chat_history = []
        while True:
            print('\n')
            question = input(">> You: ")
            
            if question == "exit":
                break
            response = self.retrievel_chain.invoke({'chat_history': chat_history, 'input': question})
            print('>> Bot:', response['answer'])
            print('\n')

            if len(chat_history) > self.chat_config.max_history*2:
                chat_history = chat_history[-self.chat_config.max_history:]
            
            chat_history.append(HumanMessage(content=response['input']))
            chat_history.append(AIMessage(content=response['answer']))
    
    
    # todo
    def ui_chat(self):
        st.set_page_config(page_title='Chat with your own PDFs', page_icon=':books:')
        st.write(css, unsafe_allow_html=True)
        

        chat_history = []
        
        st.header('Chat with Your own PDFs :books:')
        question = st.text_input("Ask anything to your PDF: ", key="question")

        if question:
            st.session_state['question'] = ''
            response = self.retrievel_chain.invoke({'chat_history': chat_history, 'input': question})
            chat_history.append(HumanMessage(content=response['input']))
            chat_history.append(AIMessage(content=response['answer']))

            for i, message in enumerate(chat_history):
                if i % 2 == 0:
                    st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
                else:
                    st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

qa = QA()

def get_qa():
    return qa

if __name__ == "__main__":
    pass