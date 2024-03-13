import streamlit as st
import os
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

from langchain.prompts import PromptTemplate
openai_api_key=os.getenv("OPENAI_API_KEY")


embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
#Load the embedings
vector_db = Chroma(persist_directory='vector_db',collection_name="wissam_collection",embedding_function=embeddings)

template = """
You are a helpful assistant that can answer questions about Wissam.answer the questions of user in a helpful way.only give answer from context if question is out of context just say i dont know.Finally, if you don't know the answer about wissam, simply state that you don't know the answer and that Wissam can be contacted through e-mail present on his CV.
 Question: {question}
 Context: {context}
 Assistant Response:
 """
propmpt=PromptTemplate.from_template(template=template)
llm=ChatOpenAI(api_key=openai_api_key)

# #memory
retriever=vector_db.as_retriever(
search_kwargs={"fetch_k":4,"k":3},search_type="mmr")
memory=ConversationBufferMemory(return_messages=True,memory_key="chat_history")
chain=ConversationalRetrievalChain.from_llm(
     llm=llm,
     memory=memory,
     retriever=retriever,
     combine_docs_chain_kwargs={"prompt": propmpt},
     chain_type="stuff"
 )

def my_main(user_input:str) -> str:
     """
     This function takes the user question or query and returns the response
     :param: user_input: The input text from the user
     :return: String value of answer  to the user question or query
     """
     # question="Tell me about education of Wissam"
     response=chain.invoke({"question":user_input,"chat_history": st.session_state.messages})
     return response.get("answer")
     # return response


