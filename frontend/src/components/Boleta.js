import React, { useEffect, useState } from "react";
import axios from "axios";
import "./Boleta.css";

function Boleta({ userId, courseId }) {
  const [data, setData] = useState(null);

  useEffect(() => {
    axios
      .get(`http://127.0.0.1:8000/boleta-json/${userId}/${courseId}`)
      .then((res) => setData(res.data));
  }, [userId, courseId]);

  if (!data) return <p>Cargando...</p>;

  return (
    <div className="boleta">

      {/* HEADER */}
      <div className="header">
        <div className="header-left">
          <strong>{data.nombre}</strong><br />
          Grado: ______
        </div>

        <div className="header-center">
          DEL MONTE SCHOOL
        </div>

        <div className="header-right">
          <strong>Profa. Español:</strong><br />
          __________<br /><br />
          <strong>Teacher English:</strong><br />
          __________
        </div>
      </div>

      {/* TABLA */}
      <div className="tabla-container">
        <table className="tabla">
          <thead>
            <tr>
              <th>ASIGNATURA</th>
              <th>P-I</th>
              <th>P-II</th>
              <th>P-III</th>
              <th>P-IV</th>
              <th>FINAL</th>
              <th>RECUP.</th>
            </tr>
          </thead>

          <tbody>
            {data.materias.map((m, i) => (
              <tr key={i}>
                <td className="materia">{m.materia}</td>
                <td>{m.P1}</td>
                <td>{m.P2}</td>
                <td>{m.P3}</td>
                <td>{m.P4}</td>
                <td>{m.final}</td>
                <td></td>
              </tr>
            ))}

            <tr className="promedio">
              <td>PROMEDIO</td>
              <td>{data.promedios.P1}</td>
              <td>{data.promedios.P2}</td>
              <td>{data.promedios.P3}</td>
              <td>{data.promedios.P4}</td>
              <td>{data.promedios.final}</td>
              <td></td>
            </tr>
          </tbody>
        </table>

        {/* PANEL DERECHO */}
        <div className="observaciones">
          <div className="obs-title">OBSERVACIONES Y ASISTENCIA</div>
          <label><input type="checkbox" /> Cumple normas</label>
          <label><input type="checkbox" /> Interés</label>
          <label><input type="checkbox" /> Presentación</label>
          <label><input type="checkbox" /> Finaliza trabajos</label>
          <label><input type="checkbox" /> Participa</label>

          <div className="asistencia">ASISTENCIA: ______</div>
        </div>
      </div>

      {/* COMENTARIOS */}
      <div className="comentarios">
        COMENTARIOS DE LOS MAESTROS
      </div>

      {/* FIRMAS */}
      <div className="firmas">
        <div>Padre de familia</div>
        <div>Prof(a). Español</div>
        <div>Teacher</div>
        <div>Director</div>
      </div>

    </div>
  );
  <div className="acciones">
  <button onClick={() => window.print()}>
    🖨️ Imprimir Boleta
  </button>
</div>
}

export default Boleta;