import React, { useState, useContext } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import { AuthContext } from './Auth';
import './ImportExport.css';

const API_URL = 'http://127.0.0.1:5000/api';

export function ImportExport() {
  const { user } = useContext(AuthContext);
  const [isOpen, setIsOpen] = useState(false);
  const [activeTab, setActiveTab] = useState('import');
  const [tables, setTables] = useState([]);
  const [loading, setLoading] = useState(false);
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState(null);
  const [verifyingTable, setVerifyingTable] = useState(null);
  const [tableExists, setTableExists] = useState(false);

  if (user?.role !== 'trainer') {
    return null;
  }

  const loadTables = async () => {
    setLoading(true);
    try {
      const token = Cookies.get('jarvis_token');
      const res = await axios.get(`${API_URL}/trainer/tables`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setTables(res.data.tables || []);
    } catch (e) {
      console.error('Error:', e);
    } finally {
      setLoading(false);
    }
  };

  const handleOpen = () => {
    setIsOpen(true);
    setMessage(null);
    loadTables();
  };

  const handleDownloadTemplate = async (tableName) => {
    try {
      const token = Cookies.get('jarvis_token');
      const res = await axios.post(
        `${API_URL}/trainer/export-template`,
        { table_name: tableName },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      if (res.data.success) {
        const link = document.createElement('a');
        link.href = `data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,${res.data.excel}`;
        link.download = res.data.filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      }
    } catch (e) {
      console.error('Error:', e);
      setMessage({
        type: 'error',
        text: 'Error descargando template'
      });
    }
  };

  const handleFileSelect = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.name.endsWith('.xlsx')) {
      setFile(selectedFile);
      setMessage(null);
      setTableExists(false);
    } else {
      setMessage({
        type: 'error',
        text: 'Solo archivos .xlsx permitidos'
      });
    }
  };

  const verifyTableExists = async (fileName) => {
    const tableName = fileName.replace('.xlsx', '').toLowerCase().replace(/\s+/g, '_').replace(/[^\w-]/g, '');
    setVerifyingTable(tableName);

    try {
      const token = Cookies.get('jarvis_token');
      const res = await axios.get(`${API_URL}/trainer/tables`, {
        headers: { Authorization: `Bearer ${token}` }
      });

      const exists = res.data.tables.some(t => t.table_name === tableName);

      if (exists) {
        setTableExists(true);
        setMessage({
          type: 'info',
          text: `ℹ️ La tabla "${tableName}" ya existe.\n\nSe agregarán datos a la tabla existente (sin columna id, será automática).`
        });
      } else {
        setTableExists(false);
        setMessage({
          type: 'success',
          text: `✅ La tabla "${tableName}" es nueva y se puede subir.`
        });
      }
    } catch (e) {
      console.error('Error:', e);
      setMessage({
        type: 'error',
        text: 'Error verificando tabla'
      });
    } finally {
      setVerifyingTable(null);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage({
        type: 'error',
        text: 'Selecciona un archivo primero'
      });
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
        if (res.data.table_exists) {
          // Tabla existente
          setMessage({
            type: 'success',
            text: `✅ Se agregaron ${res.data.rows_inserted} filas a la tabla "${res.data.table_name}"\n\nNotificado a soporte para que integren los datos a JARVIS.`
          });
        } else {
          // Tabla nueva
          setMessage({
            type: 'success',
            text: `✅ Tabla "${res.data.table_name}" creada!\n\nNotificado a soporte para que integren los datos a JARVIS.`
          });
        }
        
        setFile(null);
        setTableExists(false);
        setTimeout(() => setMessage(null), 5000);
        loadTables();
      }
    } catch (e) {
      console.error('Error:', e);
      setMessage({
        type: 'error',
        text: 'Error subiendo archivo'
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      {/* <button
        className="import-export-btn"
        onClick={handleOpen}
        title="Import/Export"
      >
        📊 Import/Export
      </button> */}

      {isOpen && (
        <div className="import-export-modal-overlay" onClick={() => setIsOpen(false)}>
          <div className="import-export-modal" onClick={(e) => e.stopPropagation()}>
            <div className="import-export-header">
              <h3>Gestionar Datos</h3>
              <button className="close-btn" onClick={() => setIsOpen(false)}>
                ✕
              </button>
            </div>

            <div className="import-export-tabs">
              <button
                className={`tab-btn ${activeTab === 'import' ? 'active' : ''}`}
                onClick={() => {
                  setActiveTab('import');
                  setMessage(null);
                  setFile(null);
                  setTableExists(false);
                }}
              >
                📥 IMPORT
              </button>
              <button
                className={`tab-btn ${activeTab === 'export' ? 'active' : ''}`}
                onClick={() => {
                  setActiveTab('export');
                  setMessage(null);
                }}
              >
                📤 EXPORT
              </button>
            </div>

            <div className="import-export-content">
              {message && (
                <div className={`notification ${message.type}`}>
                  {message.text}
                </div>
              )}

              {activeTab === 'import' ? (
                <>
                  <h4>Subir Nueva Tabla o Agregar Datos</h4>
                  <p className="info-text">📌 El nombre del archivo será el nombre de la tabla</p>
                  <p className="info-text">📌 Debe tener columna "id" como identificador único</p>

                  <div className="file-upload-area">
                    <input
                      type="file"
                      accept=".xlsx"
                      onChange={handleFileSelect}
                      id="excel-file-import"
                      disabled={loading || verifyingTable}
                    />
                    <label htmlFor="excel-file-import" className="file-label">
                      {file ? `📄 ${file.name}` : '📁 Selecciona archivo .xlsx'}
                    </label>
                  </div>

                  {file && (
                    <>
                      <button
                        className="btn-verify"
                        onClick={() => verifyTableExists(file.name)}
                        disabled={loading || verifyingTable}
                      >
                        {verifyingTable ? '⏳ Verificando...' : '✓ Verificar Tabla'}
                      </button>

                      {message && (
                        <div className="button-group">
                          <button
                            className="btn-cancel"
                            onClick={() => {
                              setFile(null);
                              setMessage(null);
                              setTableExists(false);
                            }}
                          >
                            Cancelar
                          </button>
                          <button
                            className="btn-upload"
                            onClick={handleUpload}
                            disabled={!file || loading || verifyingTable}
                          >
                            {loading ? 'Subiendo...' : 'Subir'}
                          </button>
                        </div>
                      )}
                    </>
                  )}
                </>
              ) : (
                <>
                  <h4>Descargar Templates</h4>
                  {loading ? (
                    <p>Cargando tablas...</p>
                  ) : tables.length > 0 ? (
                    <div className="tables-list">
                      {tables.map(table => (
                        <div key={table.table_name} className="table-item">
                          <div className="table-info">
                            <strong>{table.table_name}</strong>
                            <small>{table.columns.filter(col => col !== 'id').join(', ')}</small>
                          </div>
                          <button
                            className="btn-download"
                            onClick={() => handleDownloadTemplate(table.table_name)}
                          >
                            ⬇️ Descargar
                          </button>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p>Sin tablas creadas</p>
                  )}
                </>
              )}
            </div>
          </div>
        </div>
      )}
    </>
  );
}