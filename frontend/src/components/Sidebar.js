import { FaHome, FaUserGraduate } from "react-icons/fa";
import "../styles/dashboard.css";

function Sidebar() {
  return (
    <div className="sidebar">
      <h2>Boletas</h2>
      <ul>
        <li className="active"><FaHome /> Dashboard</li>
        <li><FaUserGraduate /> Alumnos</li>
      </ul>
    </div>
  );
}

export default Sidebar;