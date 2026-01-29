import React, { useState, useContext } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import { AuthContext } from './Auth';
import './UploadExcel.css';

const API_URL = 'http://127.0.0.1:5000/api';

export function UploadExcel() {
  const { user } = useContext(AuthContext);
  const [isOpen, setIsOpen] = useState(false);
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  if (user?.role !== 'trainer') {
    return null;
  }

  const handleFileSelect = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.name.endsWith('.xlsx')) {
      setFile(selectedFile);
    } else {
      alert('Solo archivos .xlsx permitidos');
    }
  };

  const handleUpload = async () => {
    if (!file) {
      alert('Selecciona un archivo primero');
      return;
    }

    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('file', file);

      const token = Cookies.get('jarvis_token');
      const res = await axios.post(
        `${API_URL}/trainer/upload`,
        formData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'multipart/form-data'
          }
        }
      );

      if (res.data.success) {
        setResult({
          success: true,
          rows_inserted: res.data.rows_inserted,
          errors: res.data.errors
        });
        setFile(null);
      }
    } catch (e) {
      setResult({
        success: false,
        error: e.response?.data?.error || e.message
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      {/* Botón en sidebar */}
      <button
        className="upload-excel-btn"
        onClick={() => setIsOpen(true)}
        title="Subir datos Excel"
      >
        📤 Upload Excel
      </button>

      {/* Modal */}
      {isOpen && (
        <div className="upload-modal-overlay" onClick={() => setIsOpen(false)}>
          <div className="upload-modal" onClick={(e) => e.stopPropagation()}>
            <div className="upload-header">
              <h3>Subir datos Excel</h3>
              <button className="close-btn" onClick={() => setIsOpen(false)}>
                ✕
              </button>
            </div>

            <div className="upload-content">
              <div className="upload-info">
                <p>📌 Requisitos:</p>
                <ul>
                  <li>✅ Columna obligatoria: <code>id</code> (número único)</li>
                  <li>✅ Nombre de tabla: será el nombre del archivo</li>
                  <li>✅ Formato: <code>.xlsx</code> únicamente</li>
                  <li>ℹ️ Las demás columnas se crearán automáticamente</li>
                </ul>
                <div className="upload-divider"></div>
                <p className="upload-note">💡 Ejemplo: "proveedores.xlsx" → tabla "proveedores"</p>
              </div>

              <div className="file-input-wrapper">
                <input
                  type="file"
                  accept=".xlsx"
                  onChange={handleFileSelect}
                  id="excel-file"
                  disabled={loading}
                />
                <label htmlFor="excel-file" className="file-label">
                  {file ? `📄 ${file.name}` : '📁 Selecciona archivo .xlsx'}
                </label>
              </div>

              <button
                className="btn-upload"
                onClick={handleUpload}
                disabled={!file || loading}
              >
                {loading ? 'Subiendo...' : 'Subir datos'}
              </button>

              {result && (
                <div className={`upload-result ${result.success ? 'success' : 'error'}`}>
                  {result.success ? (
                    <>
                      <p>✅ {result.rows_inserted} filas insertadas exitosamente</p>
                      {result.errors?.length > 0 && (
                        <div className="errors">
                          <p>⚠️ Advertencias:</p>
                          {result.errors.map((err, i) => (
                            <small key={i}>{err}</small>
                          ))}
                        </div>
                      )}
                    </>
                  ) : (
                    <p>❌ Error: {result.error}</p>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </>
  );
}