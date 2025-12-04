import os
import requests
from PyPDF2 import PdfReader
from docx import Document as DocxDocument

OPENROUTER_KEY = os.environ.get("OPENROUTER_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"


def leer_pdf(ruta):
    texto = ""
    with open(ruta, "rb") as f:
        pdf = PdfReader(f)
        for page in pdf.pages:
            t = page.extract_text() or ""
            texto += t + "\n"
    return texto.strip()


def leer_docx(ruta):
    doc = DocxDocument(ruta)
    return "\n".join(p.text for p in doc.paragraphs)


def leer_txt(ruta):
    with open(ruta, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def leer_contenido_generico(ruta, mime_type, nombre_archivo=""):
    ext = os.path.splitext(nombre_archivo)[1].lower()

    if ext == ".pdf":
        return leer_pdf(ruta)
    if ext == ".docx":
        return leer_docx(ruta)
    if ext in [".txt", ".log", ".csv"]:
        return leer_txt(ruta)

    return f"[Formato no soportado] {nombre_archivo}"


def llamar_openrouter(messages):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json",
    }
    payload = {"model": "qwen/qwen-2.5-7b-instruct", "messages": messages}
    r = requests.post(API_URL, json=payload, headers=headers)
    data = r.json()
    return data["choices"][0]["message"]["content"]


def tarea_resumen(contenido, contexto_extra=""):
    mensajes = [
        {"role": "system", "content": "Sos un asistente experto en documentos técnicos."},
        {"role": "user", "content": f"{contexto_extra}\n\nResumí este documento:\n{contenido}"},
    ]
    return llamar_openrouter(mensajes)


def tarea_cumplimiento_ens(contenido):
    mensajes = [
        {"role": "system", "content": "Experto en ENS / ISO 27001."},
        {"role": "user", "content": f"Analizá cumplimiento ENS / ISO:\n{contenido}"},
    ]
    return llamar_openrouter(mensajes)


def tarea_clasificacion(contenido):
    mensajes = [
        {"role": "system", "content": "Especialista en gestión documental."},
        {"role": "user", "content": f"Clasifica este documento:\n{contenido}"},
    ]
    return llamar_openrouter(mensajes)


def tarea_recomendaciones(contenido):
    mensajes = [
        {"role": "system", "content": "Consultor técnico senior."},
        {"role": "user", "content": f"Recomendaciones para mejorar:\n{contenido}"},
    ]
    return llamar_openrouter(mensajes)
