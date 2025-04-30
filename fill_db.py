from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
import os

DATA_PATH = "data"
CHROMA_PATH = "chroma_db"

# Verificar se o diretório existe
if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"O diretório {DATA_PATH} não existe.")

# Carregar PDFs
loader = PyPDFDirectoryLoader(DATA_PATH)
try:
    raw_documents = loader.load()
    print(f"Carregados {len(raw_documents)} documentos PDF.")
except Exception as e:
    raise ValueError(f"Erro ao carregar PDFs: {e}")

if not raw_documents:
    raise ValueError("Nenhum documento PDF foi carregado.")

text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=100)
chunks = text_splitter.split_documents(raw_documents)

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = chroma_client.get_or_create_collection(name="lei")

documents = [chunk.page_content for chunk in chunks]
metadata = [{"source": chunk.metadata.get("source", "desconhecido"), 
             "file_type": os.path.splitext(chunk.metadata.get("source", ""))[1] or "unknown"} 
            for chunk in chunks]
ids = [f"ID{i}" for i in range(len(chunks))]


try:
    collection.upsert(documents=documents, metadatas=metadata, ids=ids)
    print(f"Carregados {len(documents)} chunks no ChromaDB com sucesso!")
except Exception as e:
    print(f"Erro ao salvar no ChromaDB: {e}")


count = collection.count()
print(f"Total de itens na coleção 'lei': {count}")