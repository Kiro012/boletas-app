from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import zipfile

from moodle_api import obtener_alumnos, obtener_notas, obtener_cursos
from pdf_generator import generar_boleta

app = FastAPI()

# 🔓 CORS (React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# 📚 CURSOS
# =========================
@app.get("/cursos")
def cursos():
    data = obtener_cursos()

    return [
        {
            "id": c.get("id"),
            "nombre": c.get("fullname")
        }
        for c in data
    ]


# =========================
# 👨‍🎓 ALUMNOS (solo estudiantes)
# =========================
@app.get("/alumnos/{course_id}")
def alumnos(course_id: int):
    data = obtener_alumnos(course_id)

    resultado = []

    for alumno in data:
        roles = alumno.get("roles", [])
        es_estudiante = any(r.get("shortname") == "student" for r in roles)

        if es_estudiante:
            resultado.append({
                "id": alumno.get("id"),
                "nombre": alumno.get("fullname"),
                "email": alumno.get("email")
            })

    return resultado


# =========================
# 📊 NOTAS CRUDAS
# =========================
@app.get("/notas/{user_id}/{course_id}")
def notas(user_id: int, course_id: int):
    data = obtener_notas(user_id, course_id)

    try:
        rows = data["tables"][0]["tabledata"]

        return [
            {
                "actividad": r["cells"][0]["content"],
                "nota": r["cells"][1]["content"]
            }
            for r in rows
        ]
    except:
        return {"error": "No se pudieron obtener notas"}


# =========================
# 🧠 EXTRAER MATERIAS
# =========================
def obtener_materias(rows):
    materias = []

    for row in rows:
        columnas = row["cells"]

        nombre = columnas[0]["content"].strip()
        nota = columnas[1]["content"]

        try:
            valor = float(nota)
        except:
            continue

        # ❌ ignorar totales
        if "total" in nombre.lower():
            continue

        materias.append({
            "materia": nombre,
            "P1": valor,
            "P2": "",
            "P3": "",
            "P4": "",
            "final": valor
        })

    return materias


# =========================
# 🧠 PROMEDIOS POR PERIODO
# =========================
def obtener_promedios_periodos(rows):
    periodos = {
        "P1": 0,
        "P2": 0,
        "P3": 0,
        "P4": 0,
        "final": 0
    }

    for row in rows:
        columnas = row["cells"]

        nombre = columnas[0]["content"].strip().lower()
        nota = columnas[1]["content"]

        try:
            valor = float(nota)
        except:
            continue

        if "total periodo i" in nombre:
            periodos["P1"] = valor
        elif "total periodo ii" in nombre:
            periodos["P2"] = valor
        elif "total periodo iii" in nombre:
            periodos["P3"] = valor
        elif "total periodo iv" in nombre:
            periodos["P4"] = valor
        elif "total del curso" in nombre:
            periodos["final"] = valor

    return periodos


# =========================
# 📄 BOLETA INDIVIDUAL
# =========================
@app.get("/boleta/{user_id}/{course_id}")
def boleta(user_id: int, course_id: int):
    alumnos = obtener_alumnos(course_id)
    notas = obtener_notas(user_id, course_id)

    nombre = "Alumno"

    # 🔍 buscar nombre
    for a in alumnos:
        if a.get("id") == user_id:
            nombre = a.get("fullname")

    try:
        rows = notas.get("tables", [])[0].get("tabledata", [])

        materias = procesar_materias_por_periodo(rows)
        promedios = obtener_promedios_periodos(rows)

    except:
        materias = []
        promedios = {
            "P1": 0,
            "P2": 0,
            "P3": 0,
            "P4": 0,
            "final": 0
        }

    archivo = f"boleta_{user_id}.pdf"

    generar_boleta(nombre, materias, promedios, archivo)

    return FileResponse(archivo, media_type="application/pdf", filename=archivo)


# =========================
# 📦 BOLETAS MASIVAS (ZIP)
# =========================
@app.get("/boletas-curso/{course_id}")
def boletas_curso(course_id: int):
    alumnos = obtener_alumnos(course_id)

    archivos = []

    for alumno in alumnos:
        user_id = alumno.get("id")
        nombre = alumno.get("fullname")

        notas = obtener_notas(user_id, course_id)

        try:
            rows = notas.get("tables", [])[0].get("tabledata", [])

            materias = obtener_materias(rows)
            promedios = obtener_promedios_periodos(rows)

        except:
            continue

        archivo_pdf = f"boleta_{user_id}.pdf"

        generar_boleta(nombre, materias, promedios, archivo_pdf)

        archivos.append(archivo_pdf)

    zip_name = f"boletas_curso_{course_id}.zip"

    with zipfile.ZipFile(zip_name, "w") as zipf:
        for archivo in archivos:
            zipf.write(archivo)

    return FileResponse(zip_name, media_type="application/zip", filename=zip_name)
def procesar_materias_por_periodo(rows):
    materias = {}

    periodo_actual = None

    for row in rows:
        columnas = row["cells"]

        nombre = columnas[0]["content"].strip().lower()
        nota = columnas[1]["content"]

        # 🔎 Detectar periodo
        if "periodo i" in nombre:
            periodo_actual = "P1"
            continue
        elif "periodo ii" in nombre:
            periodo_actual = "P2"
            continue
        elif "periodo iii" in nombre:
            periodo_actual = "P3"
            continue
        elif "periodo iv" in nombre:
            periodo_actual = "P4"
            continue

        # Ignorar totales
        if "total" in nombre:
            continue

        try:
            valor = float(nota)
        except:
            continue

        materia_nombre = nombre.title()

        if materia_nombre not in materias:
            materias[materia_nombre] = {
                "materia": materia_nombre,
                "P1": "",
                "P2": "",
                "P3": "",
                "P4": "",
                "final": 0
            }

        if periodo_actual:
            materias[materia_nombre][periodo_actual] = valor

    # 🔥 calcular promedio final por materia
    for m in materias.values():
        notas = [
            m["P1"], m["P2"], m["P3"], m["P4"]
        ]

        notas_validas = [n for n in notas if isinstance(n, (int, float))]

        if notas_validas:
            m["final"] = round(sum(notas_validas) / len(notas_validas), 2)

    return list(materias.values())
@app.get("/boleta-json/{user_id}/{course_id}")
def boleta_json(user_id: int, course_id: int):
    alumnos = obtener_alumnos(course_id)
    notas = obtener_notas(user_id, course_id)

    nombre = "Alumno"

    for a in alumnos:
        if a.get("id") == user_id:
            nombre = a.get("fullname")

    try:
        rows = notas.get("tables", [])[0].get("tabledata", [])

        materias = procesar_materias_por_periodo(rows)
        promedios = obtener_promedios_periodos(rows)

    except:
        materias = []
        promedios = {
            "P1": 0, "P2": 0, "P3": 0, "P4": 0, "final": 0
        }

    return {
        "nombre": nombre,
        "materias": materias,
        "promedios": promedios
    }