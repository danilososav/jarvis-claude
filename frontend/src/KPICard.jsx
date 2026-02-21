import React from 'react';
import './KPICard.css';

/**
 * KPICard - Componente para mostrar métricas clave (KPIs)
 * Dashboard con indicadores principales y trends
 */
export function KPICard({ config, data }) {
  if (!config || !config.kpis || config.kpis.length === 0) {
    return null;
  }

  const { title, description, kpis } = config;

  // Formatear valor según tipo
  const formatValue = (value, format) => {
    if (value === null || value === undefined) return '-';

    switch (format) {
      case 'currency':
        // Formatear a millones si es muy grande
        if (value >= 1000000000) {
          return `${(value / 1000000000).toFixed(1)}B Gs`;
        } else if (value >= 1000000) {
          return `${(value / 1000000).toFixed(1)}M Gs`;
        }
        return `${value.toLocaleString('es-PY')} Gs`;
      
      case 'percentage':
        return `${value.toFixed(2)}%`;
      
      case 'number':
        return value.toLocaleString('es-PY');
      
      case 'text':
      default:
        return String(value);
    }
  };

  // Obtener ícono de trend
  const getTrendIcon = (trend) => {
    switch (trend) {
      case 'up':
        return <span className="trend-icon trend-up">↑</span>;
      case 'down':
        return <span className="trend-icon trend-down">↓</span>;
      case 'neutral':
        return <span className="trend-icon trend-neutral">→</span>;
      default:
        return null;
    }
  };

  // Obtener clase de trend
  const getTrendClass = (trend) => {
    switch (trend) {
      case 'up':
        return 'kpi-positive';
      case 'down':
        return 'kpi-negative';
      case 'neutral':
        return 'kpi-neutral';
      default:
        return '';
    }
  };

  return (
    <div className="kpi-card-container">
      <div className="kpi-header">
        <h3 className="kpi-title">{title}</h3>
        <p className="kpi-description">{description}</p>
      </div>

      <div className="kpi-grid">
        {kpis.map((kpi, idx) => (
          <div key={idx} className={`kpi-item ${getTrendClass(kpi.trend)}`}>
            <div className="kpi-label">
              {kpi.label}
              {kpi.trend && getTrendIcon(kpi.trend)}
            </div>
            <div className="kpi-value">
              {formatValue(kpi.value, kpi.format)}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
