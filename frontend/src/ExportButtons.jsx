import React, { useState } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import './ExportButtons.css';

const API_URL = 'http://127.0.0.1:5000/api';

export function ExportButtons({ message, chartConfig, chartData }) {
  const [loading, setLoading] = useState(false);
  const [showMenu, setShowMenu] = useState(false);

  const downloadFile = (data, filename) => {
    const link = document.createElement('a');
    link.href = data;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleExportPDF = async () => {
  setLoading(true);
  try {
    const token = Cookies.get('jarvis_token');
    const res = await axios.post(
      `${API_URL}/export/pdf`,
      {
        response: message.content,
        chart_type: chartConfig?.type,
        chart_data: chartData
      },
      { headers: { Authorization: `Bearer ${token}` } }
    );

    if (res.data.success) {
      downloadFile(`data:application/pdf;base64,${res.data.pdf}`, res.data.filename);
    }
  } catch (e) {
    console.error('Error:', e);
    alert('Error descargando PDF');
  } finally {
    setLoading(false);
    setShowMenu(false);
  }
};

  const handleExportChart = async () => {
    if (!chartConfig || !chartData) return;
    
    setLoading(true);
    try {
      const token = Cookies.get('jarvis_token');
      const res = await axios.post(
        `${API_URL}/export/chart`,
        {
          chart_type: chartConfig.type,
          chart_data: chartData
        },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      if (res.data.success) {
        downloadFile(`data:image/png;base64,${res.data.image}`, res.data.filename);
      }
    } catch (e) {
      console.error('Error:', e);
      alert('Error descargando gráfico');
    } finally {
      setLoading(false);
      setShowMenu(false);
    }
  };

  const handleExportExcel = async () => {
    if (!chartData || chartData.length === 0) {
      alert('Sin datos para exportar');
      return;
    }
    
    setLoading(true);
    try {
      const token = Cookies.get('jarvis_token');
      const res = await axios.post(
        `${API_URL}/export/excel`,
        {
          data: chartData,
          filename: 'datos'
        },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      if (res.data.success) {
        downloadFile(
          `data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,${res.data.excel}`,
          res.data.filename
        );
      }
    } catch (e) {
      console.error('Error:', e);
      alert('Error descargando Excel');
    } finally {
      setLoading(false);
      setShowMenu(false);
    }
  };

  return (
    <div className="export-menu">
      <button
        className="export-toggle"
        onClick={() => setShowMenu(!showMenu)}
        disabled={loading}
        title="Descargar datos"
      >
        ⋮
      </button>

      {showMenu && (
        <div className="export-dropdown">
          <button onClick={handleExportPDF} disabled={loading}>
            📄 PDF - Respuesta
          </button>
          {chartConfig && (
            <button onClick={handleExportChart} disabled={loading}>
              🖼️ PNG - Gráfico
            </button>
          )}
          {chartData && chartData.length > 0 && (
            <button onClick={handleExportExcel} disabled={loading}>
              📊 Excel - Datos
            </button>
          )}
        </div>
      )}
    </div>
  );
}