import streamlit as st
import requests
from pypdf import PdfReader
import os
from dotenv import load_dotenv

# --- 1. TÍTULO PRIMERO  ---
st.title("📄 Analizador de PDFs con IA Local")

# --- 2. CARGAR VARIABLES ---
load_dotenv() 

API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")
MODELO = "llama3.2:3b"

# --- 3. DIAGNÓSTICO EN PANTALLA ---
if not API_KEY:
    st.error("❌ ERROR: No encuentro la API_KEY. Verifica que el archivo .env exista.")
    st.info("El archivo .env debe estar en la misma carpeta que app.py")
    st.stop() 
elif not API_URL:
    st.error("❌ ERROR: No encuentro la API_URL en el archivo .env")
    st.stop()
    

# --- 4. FUNCIONES DEL PROGRAMA ---
def extraer_texto_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def consultar_ia(texto_pdf):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""
    Analiza el siguiente texto extraído de un PDF. 
    Identifica los 5 temas más relevantes y dame una breve descripción de cada uno.
    Devuelve la respuesta en formato de lista Markdown.
    
    TEXTO:
    {texto_pdf[:5000]} 
    """

    payload = {
        "model": MODELO,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"Error al conectar con la IA: {e}"

# --- 5. INTERFAZ DE CARGA ---
uploaded_file = st.file_uploader("Elige un archivo PDF", type="pdf")

if uploaded_file is not None:
    if st.button("Analizar Documento"):
        with st.spinner("Leyendo PDF y consultando a la IA..."):
            texto = extraer_texto_pdf(uploaded_file)
            resultado = consultar_ia(texto)
            st.markdown("### Resultados del Análisis:")
            st.markdown(resultado)