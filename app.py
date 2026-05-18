"""
- Agente educativo con Ollama  
Backend Flask con generación de plan de clase, sílabo y malla curricular
"""

from flask import Flask, request, jsonify, send_file, render_template, send_from_directory
from flask_cors import CORS
import requests
import re
from datetime import datetime
import os

# Para exportar a DOCX y PDF
try:
    from docx import Document
    from docx.shared import Pt, RGBColor, Inches
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

import os
from flask import Flask, request, jsonify, send_file, render_template, send_from_directory
from flask_cors import CORS
import requests
import re
from datetime import datetime

# ─────────────────────────────────────────────
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "gemma4:latest" 
OUTPUT_DIR = "outputs"

# Crear carpetas necesarias si no existen 
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Configuración de Flask para encontrar tu index.html
app = Flask(__name__, template_folder='.') 
CORS(app)

# ─────────────────────────────────────────────
# UTILIDADES OLLAMA
# ─────────────────────────────────────────────

def query_ollama(prompt: str, system_prompt: str = "") -> str:
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "system": system_prompt,
        "stream": False,
        "context": [],  # <--- AÑADE ESTA LÍNEA para limpiar la memoria de la IA
        "options": {
            "temperature": 0.4,
            "num_thread": 4, # Usa hilos reales de tu PC
            "num_ctx": 4096  # Limita el tamaño de la memoria de trabajo
        }
    }
    try:
        resp = requests.post(OLLAMA_URL, json=payload, timeout=600)
        resp.raise_for_status()
        data = resp.json()
        return data.get("response", "").strip()
    except requests.exceptions.ConnectionError:
        return "ERROR_OLLAMA_OFFLINE"
    except Exception as e:
        return f"ERROR: {str(e)}"


# ─────────────────────────────────────────────
# PROMPTS DEL AGENTE
# ─────────────────────────────────────────────

SYSTEM_BASE = """Eres EduAgent. Genera contenido pedagógico experto.
REGLA CRÍTICA: Responde directamente con el formato Markdown. 
No saludes, no expliques qué vas a hacer, no des introducciones. 
Sé breve, técnico y directo en cada sección."""


def prompt_plan_clase(tema: str, propuesta: str, aprendizaje: str, nivel: str, duracion: str) -> str:
    return f"""Actúa como un Diseñador Instruccional experto. Tu tarea es crear un Plan de Clase de ALTO IMPACTO.

DATOS CLAVE:
- TEMA: {tema}
- ENFOQUE: {propuesta}
- OBJETIVO: {aprendizaje}
- NIVEL: {nivel}
- TIEMPO: {duracion}

INSTRUCCIONES DE FORMATO:
1. Usa Markdown con títulos (##) y subtítulos (###).
2. La secuencia didáctica DEBE sumar exactamente {duracion}.
3. Divide las actividades en: Inicio (Motivación), Desarrollo (Construcción) y Cierre (Metacognición).

CONTENIDO REQUERIDO:
## 1. Identificación
## 2. Objetivos (General y 3 específicos)
## 3. Contenidos (Saber, Saber hacer, Saber ser)
## 4. Secuencia Didáctica (Detalla minuto a minuto)
## 5. Evaluación (Define un producto tangible que el alumno entregará)
## 6. Recursos Necesarios

Sé creativo, innovador y asegúrate de que las actividades sean coherentes con el nivel {nivel}."""

# Acabe de hacer un nuevo prompt el comenterario de abajo no se quien lo puso pero ya esta un poco mejor 
# ESTE PROMPT QUE ACABAS DE VER ESTA MAL PORQUE 

def prompt_silabo(tema: str, propuesta: str, aprendizaje: str, nivel: str, semestres: int) -> str:
    return f"""Genera un Sílabo académico completo con los siguientes datos:

- **Asignatura**: {tema}
- **Enfoque**: {propuesta}
- **Competencia central**: {aprendizaje}
- **Nivel**: {nivel}
- **Duración**: {semestres} semanas

El sílabo debe incluir:
1. Datos de identificación (asignatura, código, créditos, horas)
2. Descripción general del curso
3. Competencias y resultados de aprendizaje
4. Unidades temáticas con contenidos por semana
5. Metodología de enseñanza-aprendizaje
6. Sistema de evaluación (parciales, trabajos, examen final con porcentajes)
7. Bibliografía (básica y complementaria)
8. Cronograma semanal detallado

Usa formato markdown estructurado. Sé preciso en porcentajes y fechas."""


def prompt_malla(tema: str, propuesta: str, aprendizaje: str, nivel: str, ciclos: int) -> str:
    return f"""Genera una Malla Curricular completa con los siguientes datos:

- **Carrera/Programa**: {tema}
- **Enfoque educativo**: {propuesta}
- **Perfil de egreso**: {aprendizaje}
- **Nivel**: {nivel}
- **Ciclos/Semestres**: {ciclos}

La malla debe incluir:
1. Presentación del programa
2. Perfil de ingreso y egreso
3. Objetivos del programa
4. Estructura curricular por ciclos (con materias, créditos y horas)
5. Áreas de formación (básica, profesional, especialización, electivas)
6. Mapa de prerrequisitos principales
7. Carga horaria total
8. Perfil profesional y campo laboral

Organiza las materias en una tabla por ciclo. Incluye créditos para cada asignatura."""


def prompt_adaptativo(tema: str, propuesta: str, aprendizaje: str, nivel: str, duracion: str, estilo: str) -> str:
    return f"""Genera un Plan de Clase ADAPTATIVO personalizado:

- **Tema**: {tema}
- **Propuesta**: {propuesta}  
- **Aprendizaje esperado**: {aprendizaje}
- **Nivel**: {nivel}
- **Duración**: {duracion}
- **Estilo de aprendizaje predominante**: {estilo}

Adapta el plan considerando el estilo de aprendizaje indicado:
- Si es Visual: incluye diagramas descritos, mapas conceptuales, organizadores gráficos
- Si es Auditivo: incluye debates, exposiciones, podcasts, discusión grupal
- Si es Kinestésico: incluye actividades prácticas, experimentos, role-play
- Si es Lector/Escritor: incluye análisis de textos, ensayos, investigación

Estructura igual que un plan de clase estándar pero con actividades específicas para ese estilo.
Incluye una sección de "Adaptaciones para otros estilos" al final."""


# ─────────────────────────────────────────────
# EXPORTADORES
# ─────────────────────────────────────────────

def markdown_to_plain(md_text: str) -> list[dict]:
    """Convierte markdown a lista de bloques {type, text}."""
    blocks = []
    for line in md_text.split('\n'):
        line = line.rstrip()
        if line.startswith('### '):
            blocks.append({'type': 'h3', 'text': line[4:]})
        elif line.startswith('## '):
            blocks.append({'type': 'h2', 'text': line[3:]})
        elif line.startswith('# '):
            blocks.append({'type': 'h1', 'text': line[2:]})
        elif line.startswith('- ') or line.startswith('* '):
            blocks.append({'type': 'bullet', 'text': line[2:]})
        elif re.match(r'^\d+\. ', line):
            blocks.append({'type': 'numbered', 'text': re.sub(r'^\d+\. ', '', line)})
        elif line.startswith('**') and line.endswith('**'):
            blocks.append({'type': 'bold', 'text': line[2:-2]})
        elif line == '' or line == '---':
            blocks.append({'type': 'space', 'text': ''})
        else:
            # Limpiar markdown inline
            clean = re.sub(r'\*\*(.*?)\*\*', r'\1', line)
            clean = re.sub(r'\*(.*?)\*', r'\1', clean)
            clean = re.sub(r'`(.*?)`', r'\1', clean)
            if clean.strip():
                blocks.append({'type': 'para', 'text': clean})
    return blocks


def export_to_docx(content: str, title: str, filename: str) -> str:
    """Exporta contenido markdown a DOCX."""
    if not DOCX_AVAILABLE:
        raise ImportError("python-docx no instalado")

    doc = Document()

    # Estilos básicos
    style = doc.styles['Normal']
    style.font.name = 'Calibri'
    style.font.size = Pt(11)

    # Título del documento
    title_para = doc.add_heading(title, level=0)
    title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Fecha
    date_para = doc.add_paragraph(f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    date_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    date_para.runs[0].font.size = Pt(9)
    date_para.runs[0].font.color.rgb = RGBColor(128, 128, 128)

    doc.add_paragraph()

    blocks = markdown_to_plain(content)
    for block in blocks:
        t = block['text'].strip()
        if not t and block['type'] == 'space':
            doc.add_paragraph()
            continue
        if not t:
            continue

        if block['type'] == 'h1':
            doc.add_heading(t, level=1)
        elif block['type'] == 'h2':
            doc.add_heading(t, level=2)
        elif block['type'] == 'h3':
            doc.add_heading(t, level=3)
        elif block['type'] == 'bullet':
            p = doc.add_paragraph(t, style='List Bullet')
        elif block['type'] == 'numbered':
            p = doc.add_paragraph(t, style='List Number')
        elif block['type'] == 'bold':
            p = doc.add_paragraph()
            run = p.add_run(t)
            run.bold = True
        else:
            doc.add_paragraph(t)

    path = os.path.join(OUTPUT_DIR, filename)
    doc.save(path)
    return path


def export_to_pdf(content: str, title: str, filename: str) -> str:
    """Exporta contenido markdown a PDF con ReportLab."""
    if not PDF_AVAILABLE:
        raise ImportError("reportlab no instalado")

    path = os.path.join(OUTPUT_DIR, filename)
    doc = SimpleDocTemplate(path, pagesize=A4,
                            rightMargin=60, leftMargin=60,
                            topMargin=60, bottomMargin=60)

    styles = getSampleStyleSheet()
    story = []

    # Estilos personalizados
    title_style = ParagraphStyle('CustomTitle',
        parent=styles['Title'],
        fontSize=20, spaceAfter=6,
        textColor=colors.HexColor('#1a1a2e'),
        alignment=TA_CENTER)

    date_style = ParagraphStyle('DateStyle',
        parent=styles['Normal'],
        fontSize=9, spaceAfter=20,
        textColor=colors.HexColor('#888888'),
        alignment=TA_CENTER)

    h1_style = ParagraphStyle('H1',
        parent=styles['Heading1'],
        fontSize=16, spaceBefore=16, spaceAfter=6,
        textColor=colors.HexColor('#1a1a2e'))

    h2_style = ParagraphStyle('H2',
        parent=styles['Heading2'],
        fontSize=13, spaceBefore=12, spaceAfter=4,
        textColor=colors.HexColor('#16213e'))

    h3_style = ParagraphStyle('H3',
        parent=styles['Heading3'],
        fontSize=11, spaceBefore=8, spaceAfter=4,
        textColor=colors.HexColor('#0f3460'))

    body_style = ParagraphStyle('Body',
        parent=styles['Normal'],
        fontSize=10, spaceAfter=4,
        leading=14, alignment=TA_JUSTIFY)

    bullet_style = ParagraphStyle('Bullet',
        parent=styles['Normal'],
        fontSize=10, spaceAfter=3,
        leftIndent=20, leading=13)

    # Título
    story.append(Paragraph(title, title_style))
    story.append(Paragraph(f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}", date_style))

    blocks = markdown_to_plain(content)
    for block in blocks:
        t = block['text'].strip()
        if not t and block['type'] == 'space':
            story.append(Spacer(1, 6))
            continue
        if not t:
            continue

        # Escapar caracteres especiales para ReportLab
        t_safe = t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

        if block['type'] == 'h1':
            story.append(Paragraph(t_safe, h1_style))
        elif block['type'] == 'h2':
            story.append(Paragraph(t_safe, h2_style))
        elif block['type'] == 'h3':
            story.append(Paragraph(t_safe, h3_style))
        elif block['type'] in ('bullet', 'numbered'):
            prefix = '• ' if block['type'] == 'bullet' else '→ '
            story.append(Paragraph(f"{prefix}{t_safe}", bullet_style))
        elif block['type'] == 'bold':
            story.append(Paragraph(f"<b>{t_safe}</b>", body_style))
        else:
            story.append(Paragraph(t_safe, body_style))

    doc.build(story)
    return path


# ─────────────────────────────────────────────
# RUTAS API
# ─────────────────────────────────────────────
# ====================== RUTA PRINCIPAL ======================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Sirve archivos estáticos como index.html si es necesario"""
    return send_from_directory('.', path)
@app.route('/api/saludo', methods=['GET'])
def saludo():
    nombre = request.args.get('nombre', 'Docente')
    hora = datetime.now().hour
    if hora < 12:
        saludo_txt = "Buenos días"
    elif hora < 18:
        saludo_txt = "Buenas tardes"
    else:
        saludo_txt = "Buenas noches"

    prompt = f"""Da un saludo cálido y profesional a {nombre}.
El saludo es: {saludo_txt}.
Preséntate como EduAgent, asistente pedagógico.
Menciona brevemente qué puedes hacer (plan de clase, sílabo, malla curricular).
Máximo 3 oraciones. Sé amigable pero directo."""

    respuesta = query_ollama(prompt, SYSTEM_BASE)
    if respuesta.startswith("ERROR"):
        respuesta = f"{saludo_txt}, {nombre}! Soy EduAgent, tu asistente pedagógico. Puedo ayudarte a crear planes de clase, sílabos y mallas curriculares."

    return jsonify({"saludo": respuesta, "hora": saludo_txt})


@app.route('/api/plan-clase', methods=['POST'])
def plan_clase():
    data = request.json
    tema = data.get('tema', '')
    propuesta = data.get('propuesta', '')
    aprendizaje = data.get('aprendizaje', '')
    nivel = data.get('nivel', 'Bachillerato')
    duracion = data.get('duracion', '60 minutos')
    adaptativo = data.get('adaptativo', False)
    estilo = data.get('estilo', 'Visual')

    if not tema or not propuesta or not aprendizaje:
        return jsonify({"error": "Faltan datos requeridos"}), 400

    if adaptativo:
        prompt = prompt_adaptativo(tema, propuesta, aprendizaje, nivel, duracion, estilo)
    else:
        prompt = prompt_plan_clase(tema, propuesta, aprendizaje, nivel, duracion)

    contenido = query_ollama(prompt, SYSTEM_BASE)

    if contenido.startswith("ERROR_OLLAMA_OFFLINE"):
        return jsonify({"error": "Ollama no está corriendo. Inicia con: ollama serve"}), 503

    return jsonify({
        "tipo": "plan_clase",
        "titulo": f"Plan de Clase: {tema}",
        "contenido": contenido,
        "adaptativo": adaptativo
    })


@app.route('/api/silabo', methods=['POST'])
def silabo():
    data = request.json
    tema = data.get('tema', '')
    propuesta = data.get('propuesta', '')
    aprendizaje = data.get('aprendizaje', '')
    nivel = data.get('nivel', 'Universidad')
    semanas = data.get('semanas', 16)

    if not tema or not propuesta or not aprendizaje:
        return jsonify({"error": "Faltan datos requeridos"}), 400

    prompt = prompt_silabo(tema, propuesta, aprendizaje, nivel, semanas)
    contenido = query_ollama(prompt, SYSTEM_BASE)

    if contenido.startswith("ERROR_OLLAMA_OFFLINE"):
        return jsonify({"error": "Ollama no está corriendo. Inicia con: ollama serve"}), 503

    return jsonify({
        "tipo": "silabo",
        "titulo": f"Sílabo: {tema}",
        "contenido": contenido
    })


@app.route('/api/malla', methods=['POST'])
def malla():
    data = request.json
    tema = data.get('tema', '')
    propuesta = data.get('propuesta', '')
    aprendizaje = data.get('aprendizaje', '')
    nivel = data.get('nivel', 'Universidad')
    ciclos = data.get('ciclos', 8)

    if not tema or not propuesta or not aprendizaje:
        return jsonify({"error": "Faltan datos requeridos"}), 400

    prompt = prompt_malla(tema, propuesta, aprendizaje, nivel, ciclos)
    contenido = query_ollama(prompt, SYSTEM_BASE)

    if contenido.startswith("ERROR_OLLAMA_OFFLINE"):
        return jsonify({"error": "Ollama no está corriendo. Inicia con: ollama serve"}), 503

    return jsonify({
        "tipo": "malla",
        "titulo": f"Malla Curricular: {tema}",
        "contenido": contenido
    })


@app.route('/api/exportar', methods=['POST'])
def exportar():
    data = request.json
    formato = data.get('formato', 'pdf')  # 'pdf' o 'docx'
    titulo = data.get('titulo', 'Documento Educativo')
    contenido = data.get('contenido', '')
    tipo = data.get('tipo', 'documento')

    if not contenido:
        return jsonify({"error": "Sin contenido para exportar"}), 400

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe_title = re.sub(r'[^\w\s-]', '', titulo).strip().replace(' ', '_')[:40]
    filename = f"{safe_title}_{timestamp}"

    try:
        if formato == 'docx':
            filename += '.docx'
            path = export_to_docx(contenido, titulo, filename)
            mimetype = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        else:
            filename += '.pdf'
            path = export_to_pdf(contenido, titulo, filename)
            mimetype = 'application/pdf'

        return send_file(path, mimetype=mimetype,
                        as_attachment=True,
                        download_name=filename)
    except ImportError as e:
        return jsonify({"error": f"Librería no disponible: {str(e)}. Instala con pip install python-docx reportlab"}), 500
    except Exception as e:
        return jsonify({"error": f"Error al exportar: {str(e)}"}), 500


@app.route('/api/estado', methods=['GET'])
def estado():
    """Verifica si Ollama está disponible."""
    try:
        resp = requests.get("http://localhost:11434/api/tags", timeout=5)
        modelos = [m['name'] for m in resp.json().get('models', [])]
        return jsonify({
            "ollama": True,
            "modelos": modelos,
            "modelo_activo": OLLAMA_MODEL
        })
    except:
        return jsonify({
            "ollama": False,
            "modelos": [],
            "modelo_activo": OLLAMA_MODEL
        })


if __name__ == '__main__':
    print("=" * 50)
    print("  EduAgent Backend")
    print("  http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)