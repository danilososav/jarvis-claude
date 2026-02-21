import React, { useState } from 'react';
import './DataTable.css';

/**
 * DataTable - Componente tabla profesional
 * Features: sorting, totales, formato de moneda/porcentaje/números
 */
export function DataTable({ config, data }) {
  if (!config || !data || data.length === 0) {
    return null;
  }

  const { title, description, columns, show_totals, sortable } = config;
  
  const [sortConfig, setSortConfig] = useState({
    key: null,
    direction: 'asc'
  });

  // Manejar sorting
  const handleSort = (columnKey) => {
    if (!sortable) return;

    let direction = 'asc';
    if (sortConfig.key === columnKey && sortConfig.direction === 'asc') {
      direction = 'desc';
    }

    setSortConfig({ key: columnKey, direction });
  };

  // Datos ordenados
  const sortedData = React.useMemo(() => {
    if (!sortConfig.key) return data;

    const sorted = [...data].sort((a, b) => {
      const aValue = a[sortConfig.key];
      const bValue = b[sortConfig.key];

      if (typeof aValue === 'number' && typeof bValue === 'number') {
        return sortConfig.direction === 'asc' ? aValue - bValue : bValue - aValue;
      }

      const aStr = String(aValue || '').toLowerCase();
      const bStr = String(bValue || '').toLowerCase();
      
      if (aStr < bStr) return sortConfig.direction === 'asc' ? -1 : 1;
      if (aStr > bStr) return sortConfig.direction === 'asc' ? 1 : -1;
      return 0;
    });

    return sorted;
  }, [data, sortConfig]);

  // Calcular totales
  const totals = React.useMemo(() => {
    if (!show_totals) return null;

    const result = {};
    columns.forEach(col => {
      if (col.type === 'currency' || col.type === 'number') {
        result[col.key] = data.reduce((sum, row) => sum + (row[col.key] || 0), 0);
      } else if (col.type === 'percentage') {
        const sum = data.reduce((sum, row) => sum + (row[col.key] || 0), 0);
        result[col.key] = sum / data.length;
      } else {
        result[col.key] = null;
      }
    });

    return result;
  }, [data, columns, show_totals]);

  // Formatear valores
  const formatValue = (value, type) => {
    if (value === null || value === undefined) return '-';

    switch (type) {
      case 'currency':
        return `${value.toLocaleString('es-PY')} Gs`;
      case 'percentage':
        return `${value.toFixed(2)}%`;
      case 'number':
        return value.toLocaleString('es-PY');
      default:
        return value;
    }
  };

  // Ícono de sorting
  const getSortIcon = (columnKey) => {
    if (!sortable) return null;
    if (sortConfig.key !== columnKey) return '⇅';
    return sortConfig.direction === 'asc' ? '↑' : '↓';
  };

  return (
    <div className="data-table-card">
      <div className="table-header">
        <h3 className="table-title">{title}</h3>
        <p className="table-description">{description}</p>
      </div>

      <div className="table-wrapper">
        <table className="data-table">
          <thead>
            <tr>
              {columns.map((col, idx) => (
                <th
                  key={idx}
                  onClick={() => handleSort(col.key)}
                  className={sortable ? 'sortable' : ''}
                  style={{ textAlign: col.type === 'text' ? 'left' : 'right' }}
                >
                  <div className="th-content">
                    <span>{col.label}</span>
                    {sortable && <span className="sort-icon">{getSortIcon(col.key)}</span>}
                  </div>
                </th>
              ))}
            </tr>
          </thead>

          <tbody>
            {sortedData.map((row, rowIdx) => (
              <tr key={rowIdx}>
                {columns.map((col, colIdx) => (
                  <td
                    key={colIdx}
                    style={{ textAlign: col.type === 'text' ? 'left' : 'right' }}
                    className={col.type}
                  >
                    {formatValue(row[col.key], col.type)}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>

          {show_totals && totals && (
            <tfoot>
              <tr className="totals-row">
                {columns.map((col, idx) => (
                  <td
                    key={idx}
                    style={{ textAlign: col.type === 'text' ? 'left' : 'right' }}
                    className="total-cell"
                  >
                    {idx === 0 ? (
                      <strong>TOTAL</strong>
                    ) : totals[col.key] !== null ? (
                      <strong>{formatValue(totals[col.key], col.type)}</strong>
                    ) : (
                      '-'
                    )}
                  </td>
                ))}
              </tr>
            </tfoot>
          )}
        </table>
      </div>

      <div className="table-footer">
        <span className="table-count">
          📊 {data.length} registro{data.length !== 1 ? 's' : ''}
        </span>
      </div>
    </div>
  );
}
