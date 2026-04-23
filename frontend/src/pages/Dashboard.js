import React, { useEffect, useState } from "react";
import axios from "axios";
import Boleta from "./Boleta";

function Dashboard() {
  const [cursos, setCursos] = useState([]);
  const [alumnos, setAlumnos] = useState([]);

  const [cursoSeleccionado, setCursoSeleccionado] = useState("");
  const [alumnoSeleccionado, setAlumnoSeleccionado] = useState("");

  // 🔹 Cargar cursos
  useEffect(() => {
    axios.get("http://127.0.0.1:8000/cursos")
      .then(res => setCursos(res.data));
  }, []);

  // 🔹 Cargar alumnos cuando cambia curso
  useEffect(() => {
    if (cursoSeleccionado) {
      axios.get(`http://127.0.0.1:8000/alumnos/${cursoSeleccionado}`)
        .then(res => setAlumnos(res.data));
    }
  }, [cursoSeleccionado]);

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>

      <h2>📊 Sistema de Boletas</h2>

      {/* SELECT CURSO */}
      <div style={{ marginBottom: "10px" }}>
        <label>Curso:</label><br />
        <select
          value={cursoSeleccionado}
          onChange={(e) => {
            setCursoSeleccionado(e.target.value);
            setAlumnoSeleccionado("");
          }}
        >
          <option value="">-- Seleccionar curso --</option>
          {cursos.map(c => (
            <option key={c.id} value={c.id}>
              {c.nombre}
            </option>
          ))}
        </select>
      </div>

      {/* SELECT ALUMNO */}
      <div style={{ marginBottom: "20px" }}>
        <label>Alumno:</label><br />
        <select
          value={alumnoSeleccionado}
          onChange={(e) => setAlumnoSeleccionado(e.target.value)}
          disabled={!cursoSeleccionado}
        >
          <option value="">-- Seleccionar alumno --</option>
          {alumnos.map(a => (
            <option key={a.id} value={a.id}>
              {a.nombre}
            </option>
          ))}
        </select>
      </div>

      {/* MOSTRAR BOLETA */}
      {alumnoSeleccionado && cursoSeleccionado && (
        <Boleta
          userId={alumnoSeleccionado}
          courseId={cursoSeleccionado}
        />
      )}

    </div>
  );
}

export default Dashboard;