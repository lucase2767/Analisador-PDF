import os
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_classic.chains import RetrievalQA
from dotenv import load_dotenv

load_dotenv()

class Brain:
    def __init__(self, persist_directory="chroma_db"):
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
        
        self.vector_store = Chroma(
            persist_directory=persist_directory,
            embedding_function=self.embeddings
        )
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", #eu não consigo usar o 1.5 flash com a minha api, mas, se possivel, use um modelo mais barato.
            temperature=0.2,
            convert_system_message_to_human=True
        )
        
        self.retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 4}
        )
        
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            return_source_documents=True
        )

    def ask(self, query: str):
        if not query: return "Por favor, faça uma pergunta."
        
        try:
            response = self.qa_chain.invoke({"query": query})
            answer = response.get("result", "Desculpe, não consegui encontrar uma resposta.")
            sources = [doc.metadata.get("source", "Desconhecido") for doc in response.get("source_documents", [])]
            
            return {
                "answer": answer,
                "sources": list(set(sources))
            }
        except Exception as e: return {"answer": f"Erro ao processar a pergunta: {str(e)}", "sources": []}
