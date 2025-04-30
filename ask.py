from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA

# Carrega variáveis de ambiente
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")


if not api_key:
    raise ValueError("GEMINI_API_KEY não foi definida no .env")

def carregar_documentos_pasta(pasta: str):
    documentos = []
    for arquivo in os.listdir(pasta):
        if arquivo.endswith(".pdf"):
            caminho = os.path.join(pasta, arquivo)
            loader = PyPDFLoader(caminho)
            documentos.extend(loader.load())
    return documentos

print("Carregando documentos PDF...")
documentos = carregar_documentos_pasta("data")

# Divide o texto em pedaços
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(documentos)

# Cria embeddings e indexa com FAISS
print("Indexando documentos...")
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
vectorstore = FAISS.from_documents(chunks, embeddings)

# Cria o LLM e o RetrievalQA chain
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=api_key)
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore.as_retriever())


def fazer_pergunta():
    # Interface de perguntas via terminal
    print("\n✅ Pronto para perguntas sobre os PDFs. Digite 'sair' para encerrar.\n")
    while True:
        pergunta = input("Você: ")
        if pergunta.lower() in ["sair", "exit", "quit"]:
            break
        resposta = qa_chain.run(pergunta)
        print(f"🤖 Gemini: {resposta}\n")
        return resposta
