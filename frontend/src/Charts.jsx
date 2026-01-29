import React from 'react';
import {
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';

const COLORS = ['#58a6ff', '#79c0ff', '#1f6feb', '#0969da', '#388bfd'];

// Top 5 Clientes - Bar Chart
export function TopClientesChart({ data }) {
  if (!data || data.length === 0) return null;

  const chartData = data.map(item => ({
    name: item.cliente.substring(0, 20),
    facturacion: Math.round(item.facturacion / 1000000) // En millones
  }));

  return (
    <div className="chart-container">
      <h4>Top Clientes por Facturación (en millones Gs)</h4>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#30363d" />
          <XAxis dataKey="name" stroke="#8b949e" fontSize={12} />
          <YAxis stroke="#8b949e" fontSize={12} />
          <Tooltip 
            contentStyle={{ background: '#161b22', border: '1px solid #30363d', borderRadius: 6 }}
            cursor={{ fill: 'rgba(88, 166, 255, 0.1)' }}
          />
          <Bar dataKey="facturacion" fill="#58a6ff" radius={[8, 8, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

// Market Share - Pie Chart
export function MarketShareChart({ data }) {
  if (!data || data.length === 0) return null;

  const chartData = data
    .filter(item => item.market_share > 0)
    .slice(0, 5)
    .map(item => ({
      name: item.cliente.substring(0, 15),
      value: parseFloat(item.market_share.toFixed(2))
    }));

  return (
    <div className="chart-container">
      <h4>Market Share (%)</h4>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, value }) => `${name}: ${value}%`}
            outerRadius={100}
            fill="#8884d8"
            dataKey="value"
          >
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip 
            contentStyle={{ background: '#161b22', border: '1px solid #30363d', borderRadius: 6 }}
            formatter={(value) => `${value.toFixed(2)}%`}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

// Single Cliente Analysis
export function ClienteAnalysisChart({ data }) {
  if (!data || data.length === 0) return null;

  const item = data[0];
  const chartData = [
    { name: 'Facturación Total', value: Math.round(item.facturacion / 1000000) },
    { name: 'Promedio Mensual', value: Math.round(item.promedio_mensual / 1000000) }
  ];

  return (
    <div className="chart-container">
      <h4>{item.cliente}</h4>
      <div className="cliente-stats">
        <div className="stat-box">
          <span className="stat-label">Facturación Total</span>
          <span className="stat-value">{item.facturacion.toLocaleString('es-PY')} Gs</span>
        </div>
        <div className="stat-box">
          <span className="stat-label">Promedio Mensual</span>
          <span className="stat-value">{item.promedio_mensual.toLocaleString('es-PY')} Gs</span>
        </div>
        <div className="stat-box">
          <span className="stat-label">Market Share</span>
          <span className="stat-value">{item.market_share.toFixed(2)}%</span>
        </div>
      </div>

      <ResponsiveContainer width="100%" height={250}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#30363d" />
          <XAxis dataKey="name" stroke="#8b949e" fontSize={12} />
          <YAxis stroke="#8b949e" fontSize={12} label={{ value: 'Millones Gs', angle: -90, position: 'insideLeft' }} />
          <Tooltip 
            contentStyle={{ background: '#161b22', border: '1px solid #30363d', borderRadius: 6 }}
            formatter={(value) => `${value}M Gs`}
          />
          <Bar dataKey="value" fill="#58a6ff" radius={[8, 8, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
