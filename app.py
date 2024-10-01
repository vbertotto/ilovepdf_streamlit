import streamlit as st
from streamlit_option_menu import option_menu
from pypdf import PdfReader, PdfWriter, PdfMerger
import io

# Configuração da página
st.set_page_config(page_title="Manipulador de PDFs", layout="wide")

# Barra lateral estilizada usando streamlit-option-menu
with st.sidebar:
    selected = option_menu(
        menu_title="Menu Principal",  # Título do menu
        options=["Extrair Texto", "Mesclar PDFs", "Dividir PDF", "Adicionar Marca d'Água", "Criptografar PDF", "Rotacionar Páginas"],
        icons=["file-earmark-text", "files", "split", "water", "lock", "arrow-90deg-left"],
        menu_icon="cast",  # Ícone do menu
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#f0f2f6"},
            "icon": {"color": "orange", "font-size": "20px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#d6d6d6"},
        }
    )

st.title("Manipulador de PDFs com Streamlit e PyPDF")

# Definição das funções (mesmas do código anterior)

def extrair_texto(pdf_bytes):
    reader = PdfReader(io.BytesIO(pdf_bytes))
    texto_completo = ""
    for pagina in reader.pages:
        texto_completo += pagina.extract_text() or ""
    return texto_completo

def mesclar_pdfs(pdfs):
    merger = PdfMerger()
    for pdf in pdfs:
        merger.append(io.BytesIO(pdf.read()))
    output = io.BytesIO()
    merger.write(output)
    merger.close()
    return output.getvalue()

def dividir_pdf(pdf_bytes):
    reader = PdfReader(io.BytesIO(pdf_bytes))
    paginas = []
    for i, pagina in enumerate(reader.pages):
        writer = PdfWriter()
        writer.add_page(pagina)
        output = io.BytesIO()
        writer.write(output)
        paginas.append(output.getvalue())
    return paginas

def adicionar_marca_dagua(pdf_bytes, watermark_bytes):
    reader = PdfReader(io.BytesIO(pdf_bytes))
    watermark = PdfReader(io.BytesIO(watermark_bytes)).pages[0]
    writer = PdfWriter()
    for pagina in reader.pages:
        pagina.merge_page(watermark)
        writer.add_page(pagina)
    output = io.BytesIO()
    writer.write(output)
    return output.getvalue()

def criptografar_pdf(pdf_bytes, senha):
    reader = PdfReader(io.BytesIO(pdf_bytes))
    writer = PdfWriter()
    for pagina in reader.pages:
        writer.add_page(pagina)
    writer.encrypt(user_password=senha, owner_password=None, use_128bit=True)
    output = io.BytesIO()
    writer.write(output)
    return output.getvalue()

def rotacionar_paginas(pdf_bytes, angulo):
    reader = PdfReader(io.BytesIO(pdf_bytes))
    writer = PdfWriter()
    for pagina in reader.pages:
        pagina.rotate(angulo)
        writer.add_page(pagina)
    output = io.BytesIO()
    writer.write(output)
    return output.getvalue()

# Interface principal com base na opção selecionada
if selected == "Extrair Texto":
    st.header("Extrair Texto de um PDF")
    uploaded_file = st.file_uploader("Faça upload do PDF", type=["pdf"])
    if uploaded_file:
        texto = extrair_texto(uploaded_file.read())
        st.text_area("Texto Extraído:", texto, height=400)

elif selected == "Mesclar PDFs":
    st.header("Mesclar Múltiplos PDFs")
    uploaded_files = st.file_uploader("Faça upload dos PDFs", type=["pdf"], accept_multiple_files=True)
    if uploaded_files and st.button("Mesclar PDFs"):
        pdf_merged = mesclar_pdfs(uploaded_files)
        st.download_button(
            label="Baixar PDF Mesclado",
            data=pdf_merged,
            file_name="mesclado.pdf",
            mime="application/pdf"
        )

elif selected == "Dividir PDF":
    st.header("Dividir PDF em Páginas Individuais")
    uploaded_file = st.file_uploader("Faça upload do PDF", type=["pdf"])
    if uploaded_file and st.button("Dividir PDF"):
        paginas = dividir_pdf(uploaded_file.read())
        for i, pagina in enumerate(paginas):
            st.download_button(
                label=f"Baixar Página {i + 1}",
                data=pagina,
                file_name=f"pagina_{i + 1}.pdf",
                mime="application/pdf"
            )

elif selected == "Adicionar Marca d'Água":
    st.header("Adicionar Marca d'Água em um PDF")
    pdf_file = st.file_uploader("Faça upload do PDF", type=["pdf"], key="pdf_marca")
    watermark_file = st.file_uploader("Faça upload da Marca d'Água (PDF)", type=["pdf"], key="watermark")
    if pdf_file and watermark_file and st.button("Adicionar Marca d'Água"):
        pdf_with_watermark = adicionar_marca_dagua(pdf_file.read(), watermark_file.read())
        st.download_button(
            label="Baixar PDF com Marca d'Água",
            data=pdf_with_watermark,
            file_name="com_marca_dagua.pdf",
            mime="application/pdf"
        )

elif selected == "Criptografar PDF":
    st.header("Criptografar um PDF com Senha")
    uploaded_file = st.file_uploader("Faça upload do PDF", type=["pdf"])
    senha = st.text_input("Defina a Senha para o PDF:", type="password")
    if uploaded_file and senha and st.button("Criptografar PDF"):
        pdf_criptografado = criptografar_pdf(uploaded_file.read(), senha)
        st.download_button(
            label="Baixar PDF Criptografado",
            data=pdf_criptografado,
            file_name="criptografado.pdf",
            mime="application/pdf"
        )

elif selected == "Rotacionar Páginas":
    st.header("Rotacionar Páginas de um PDF")
    uploaded_file = st.file_uploader("Faça upload do PDF", type=["pdf"])
    angulo = st.selectbox("Selecione o ângulo de rotação:", [90, 180, 270])
    if uploaded_file and st.button("Rotacionar PDF"):
        pdf_rotacionado = rotacionar_paginas(uploaded_file.read(), angulo)
        st.download_button(
            label=f"Baixar PDF Rotacionado {angulo}°",
            data=pdf_rotacionado,
            file_name=f"rotacionado_{angulo}.pdf",
            mime="application/pdf"
        )
