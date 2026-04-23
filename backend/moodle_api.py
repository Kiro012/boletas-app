import requests

MOODLE_URL = "https://alumnosacademia.delmonteschool.edu.gt/webservice/rest/server.php"
TOKEN = "052cc2469aa549471757471e25edf33a"

# FUNCIÓN PARA ALUMNOS
def obtener_alumnos(course_id):
    params = {
        "wstoken": TOKEN,
        "wsfunction": "core_enrol_get_enrolled_users",
        "moodlewsrestformat": "json",
        "courseid": course_id
    }

    response = requests.get(MOODLE_URL, params=params)
    return response.json()


# FUNCIÓN PARA NOTAS
def obtener_notas(user_id, course_id):
    params = {
        "wstoken": TOKEN,
        "wsfunction": "gradereport_user_get_grades_table",
        "moodlewsrestformat": "json",
        "userid": user_id,
        "courseid": course_id
    }

    response = requests.get(MOODLE_URL, params=params)
    return response.json()
def obtener_cursos():
    params = {
        "wstoken": TOKEN,
        "wsfunction": "core_course_get_courses",
        "moodlewsrestformat": "json"
    }

    response = requests.get(MOODLE_URL, params=params)
    return response.json()