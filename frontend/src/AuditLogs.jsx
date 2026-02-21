import React, { useState, useContext } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import { AuthContext } from './Auth';
import './AuditLogs.css';

const API_URL = 'http://127.0.0.1:5000/api';

export function AuditLogs() {
  const { user } = useContext(AuthContext);
  const [isOpen, setIsOpen] = useState(false);
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(false);

  if (user?.role !== 'trainer') {
    return null;
  }

  const loadLogs = async () => {
    setLoading(true);
    try {
      const token = Cookies.get('jarvis_token');
      const res = await axios.get(`${API_URL}/audit/logs`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setLogs(res.data.logs || []);
    } catch (e) {
      console.error('Error:', e);
    } finally {
      setLoading(false);
    }
  };

  const handleOpen = () => {
    setIsOpen(true);
    loadLogs();
  };

  const getActionColor = (action) => {
    switch (action) {
      case 'LOGIN':
        return '#3fb950';
      case 'LOGOUT':
        return '#f85149';
      case 'QUERY':
        return '#58a6ff';
      case 'FEEDBACK':
        return '#d29922';
      case 'UPLOAD':
        return '#6e40aa';
      default:
        return '#8b949e';
    }
  };

  return (
    <>
      {/* <button
        className="audit-btn"
        onClick={handleOpen}
        title="Ver auditoría"
      >
        📋 Auditoría
      </button> */}

      {isOpen && (
        <div className="audit-modal-overlay" onClick={() => setIsOpen(false)}>
          <div className="audit-modal" onClick={(e) => e.stopPropagation()}>
            <div className="audit-header">
              <h3>Auditoría - Registro de Acciones</h3>
              <button className="close-btn" onClick={() => setIsOpen(false)}>
                ✕
              </button>
            </div>

            <div className="audit-content">
              {loading ? (
                <p>Cargando...</p>
              ) : logs.length > 0 ? (
                <table className="audit-table">
                  <thead>
                    <tr>
                      <th>Usuario</th>
                      <th>Acción</th>
                      <th>Detalles</th>
                      <th>IP</th>
                      <th>Fecha/Hora</th>
                    </tr>
                  </thead>
                  <tbody>
                    {logs.map((log) => (
                      <tr key={log.id}>
                        <td>{log.username}</td>
                        <td>
                          <span
                            className="action-badge"
                            style={{ backgroundColor: getActionColor(log.action) }}
                          >
                            {log.action}
                          </span>
                        </td>
                        <td className="details">{log.details || '-'}</td>
                        <td className="ip">{log.ip_address}</td>
                        <td className="date">
                          {new Date(log.created_at).toLocaleString('es-PY')}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              ) : (
                <p>Sin registros de auditoría</p>
              )}
            </div>
          </div>
        </div>
      )}
    </>
  );
}