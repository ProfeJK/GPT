# -*- coding: utf-8 -*-
"""CodigoOpenAI.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1WeVOgQnAxtFrEzkjhHSUjzm4Pb3uBl5N
"""

import pdfplumber

def extraer_texto(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        paginas_texto = [pagina.extract_text() for pagina in pdf.pages]
    return " ".join(paginas_texto) if paginas_texto else ""

"""**Importar pdfplumber:** Esto carga la biblioteca pdfplumber en tu script, la cual es necesaria para interactuar con archivos PDF.

**Definir la función extraer_texto:** Esta función acepta un argumento **pdf_path**, que es la ruta al archivo PDF que deseas procesar.

**Abrir el PDF:** **pdfplumber.open(pdf_path)** abre el archivo PDF ubicado en la ruta especificada. La instrucción with se utiliza aquí para asegurar que el archivo se maneje correctamente y se cierre después de terminar el proceso, evitando así el uso innecesario de recursos.



**Extraer texto de cada página:**

**pdf.pages** es una lista de todas las páginas en el documento PDF.
**[pagina.extract_text() for pagina in pdf.pages]** es una comprensión de lista que itera sobre cada página del PDF, extrayendo el texto de cada una mediante el método **extract_text()**.
Esto produce una lista de strings, donde cada string contiene el texto
extraído de una página.



**Concatenar y retornar el texto:**

**" ".join(paginas_texto)** toma la lista de textos de cada página y los une en un solo string, separando cada página de texto con un espacio.
**if paginas_texto else ""** verifica si la lista paginas_texto no está vacía. Si está vacía (lo que significa que no se pudo extraer texto), retorna un string vacío.
"""

import openai

def obtener_respuestas(texto):
    openai.api_key = 'sk-proj-yuE9WmQMI4guvUeNOt2LT3BlbkFJLpvEMfJAmvni9E6OUWaI'
    preguntas = [
        "¿Cuál es la fecha mencionada en el documento?",
        "¿Quién es el cliente?",
        "¿Cuál es la fecha de vencimiento de términos?",
        "¿Cuál es el tema principal del documento?"
    ]
    respuestas = {}
    for pregunta in preguntas:
        respuesta = openai.Completion.create(
            model="text-davinci-002",
            prompt=f"Texto: {texto}\nPregunta: {pregunta}",
            max_tokens=50
        )
        respuestas[pregunta] = respuesta.choices[0].text.strip()
    return respuestas

from flask import Flask, request, jsonify
import pdfplumber

app = Flask(__name__)

def extraer_texto(file_stream):
    with pdfplumber.open(file_stream) as pdf:
        paginas_texto = [pagina.extract_text() for pagina in pdf.pages]
    return " ".join(paginas_texto) if paginas_texto else ""

def obtener_respuestas(texto):
    import openai
    openai.api_key = 'sk-proj-yuE9WmQMI4guvUeNOt2LT3BlbkFJLpvEMfJAmvni9E6OUWaI'
    preguntas = [
        "¿Cuál es la fecha mencionada en el documento?",
        "¿Quién es el imputado?",
        "¿Cuál es la fecha de vencimiento de términos?",
        "¿Cuál es el tema principal del documento?"
    ]
    respuestas = {}
    for pregunta in preguntas:
        respuesta = openai.Completion.create(
            model="text-davinci-002",
            prompt=f"Texto: {texto}\nPregunta: {pregunta}",
            max_tokens=50
        )
        respuestas[pregunta] = respuesta.choices[0].text.strip()
    return respuestas

@app.route('/cargar', methods=['POST'])
def cargar_pdfs():
    archivos = request.files.getlist('archivo')
    resultados = []
    for archivo in archivos:
        if archivo and archivo.filename.endswith('.pdf'):
            texto = extraer_texto_del_pdf(archivo)
            respuestas = obtener_respuestas(texto)
            resultados.append({
                'nombre_archivo': archivo.filename,
                'respuestas': respuestas
            })
        else:
            resultados.append({
                'nombre_archivo': archivo.filename,
                'error': 'Formato de archivo no soportado o no se seleccionó archivo'
            })
    return jsonify(resultados)


if __name__ == '__main__':
    app.run(debug=True)
