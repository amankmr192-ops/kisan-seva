
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama as OllamaLLM 
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

import os
BASE_DIR         = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VECTORSTORE_PATH = os.path.join(BASE_DIR, "vectorstore", "faiss_index")

KISAN_PROMPT = PromptTemplate(
    input_variables=["context", "question", "chat_history"],
    template="""
You are Kisan Seva AI, a helpful assistant for Indian farmers.
You MUST always reply in Hinglish — a mix of Hindi and English.
Write Hindi words in English script (Roman Hindi), not Devanagari.

Example of good response style:
"PM-KISAN scheme mein aapko har saal 6000 rupaye milte hain.
Yeh paisa 3 installments mein seedha aapke bank account mein
aata hai. Is scheme ke liye aapko Aadhaar Card aur land record
chahiye hoga."

Always structure your answer like this:
1. Scheme kya hai (1-2 lines)
2. Kise milega (eligibility)
3. Kya documents chahiye
4. Kaise apply karein

If you don't know something, say:
"Is baare mein mujhe puri jaankari nahi hai. Apne nazdiki
CSC centre ya agriculture office mein sampark karein."

Context from official documents:
{context}

Chat History:
{chat_history}

Farmer's Question: {question}

Answer in Hinglish (Roman Hindi + English mix):"""
)


def load_rag_chain():
    print("Loading embeddings...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "mps"}
    )

    print("Loading FAISS index...")
    vectorstore = FAISS.load_local(
        VECTORSTORE_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )

    print("Loading Mistral via Ollama...")
    llm = OllamaLLM(
        model="mistral",
        temperature=0.3,
        num_predict=512
    )

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"
    )

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True,
        combine_docs_chain_kwargs={"prompt": KISAN_PROMPT}
    )

    print("✅ RAG chain ready!")
    return chain