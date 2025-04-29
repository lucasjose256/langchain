import faiss
import numpy as np
import streamlit as st
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configuraitr a chave de API do Gemini
try:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY não encontrada no arquivo .env")
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Erro ao configurar a chave de API do Gemini: {e}")
    st.stop()

# Função para extrair texto de PDF
def extrair_texto_pdf(caminho_pdf):
    try:
        reader = PdfReader(caminho_pdf)
        texto = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                texto += page_text
        return texto
    except Exception as e:
        st.error(f"Erro ao extrair texto do PDF: {e}")
        return ""

# Função para dividir texto em pedaços
def dividir_texto(texto, tamanho_pedaco=500):
    pedacos = []
    for i in range(0, len(texto), tamanho_pedaco):
        pedacos.append(texto[i:i + tamanho_pedaco])
    return pedacos

# Função para gerar embeddings
def gerar_embeddings(pedacos, modelo_embedding):
    try:
        return np.array(modelo_embedding.encode(pedacos))
    except Exception as e:
        st.error(f"Erro ao gerar embeddings: {e}")
        return np.array([])

# Função para criar índice vetorial
def criar_indice_vetorial(embeddings):
    try:
        dimensao = embeddings.shape[1]
        indice = faiss.IndexFlatL2(dimensao)
        indice.add(embeddings)
        return indice
    except Exception as e:
        st.error(f"Erro ao criar índice vetorial: {e}")
        return None

# Função para consultar RAG com Gemini
def consultar_rag(pergunta, indice, pedacos, modelo_embedding):
    try:
        embedding_pergunta = modelo_embedding.encode([pergunta])[0]
        k = 3
        distancias, indices = indice.search(np.array([embedding_pergunta]), k)
        contexto = [pedacos[idx] for idx in indices[0]]
        prompt = f"Contexto: {''.join(contexto)}\n\nPergunta: {pergunta}\nResposta:"
        # Usar Gemini API para gerar resposta
        model = genai.GenerativeModel("gemini-1.5-flash")
        resposta = model.generate_content(prompt)
        return resposta.text
    except Exception as e:
        st.error(f"Erro ao consultar RAG: {e}")
        return "Erro ao gerar resposta."

# Inicializar modelo de embeddings
try:
    modelo_embedding = SentenceTransformer('all-MiniLM-L6-v2')
except Exception as e:
    st.error(f"Erro ao inicializar modelo de embeddings: {e}")
    st.stop()

# Interface Streamlit
st.title("Consulta em PDFs com RAG (Gemini API)")
pdf = st.file_uploader("Carregar PDF", type="pdf")
pergunta = st.text_input("Digite sua pergunta")

if pdf and pergunta:
    # Salvar PDF temporariamente
    try:
        with open("temp.pdf", "wb") as f:
            f.write(pdf.read())
    except Exception as e:
        st.error(f"Erro ao salvar PDF: {e}")
        st.stop()
    
    # Processar e consultar
    texto = extrair_texto_pdf("temp.pdf")
    if texto:
        pedacos = dividir_texto(texto)
        if pedacos:
            embeddings = gerar_embeddings(pedacos, modelo_embedding)
            if embeddings.size > 0:
                indice = criar_indice_vetorial(embeddings)
                if indice:
                    resposta = consultar_rag(pergunta, indice, pedacos, modelo_embedding)
                    st.write(resposta)
                else:
                    st.write("Falha ao criar índice vetorial.")
            else:
                st.write("Nenhum embedding gerado. Verifique o conteúdo do PDF.")
        else:
            st.write("Nenhum pedaço de texto gerado. O PDF pode estar vazio.")
    else:
        st.write("Nenhum texto foi extraído do PDF. Verifique o arquivo.")