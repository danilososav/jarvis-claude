import React from 'react';
import {
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';
import './DynamicChart.css';

const COLORS = ['#58a6ff', '#79c0ff', '#1f6feb', '#0969da', '#388bfd', '#6e40aa', '#f85149'];

export function DynamicChart({ data, config }) {
  if (!config || !data || data.length === 0) return null;

  const chartData = data.map(item => ({
    name: item.cliente?.substring(0, 20) || item.name,
    facturacion: Math.round(item.facturacion / 1000000),
    market_share: item.market_share,
    full_name: item.cliente
  }));

  const renderChart = () => {
    switch (config.type) {
      case 'bar':
        return (
          <ResponsiveContainer width="100%" height={350}>
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#30363d" />
              <XAxis dataKey="name" stroke="#8b949e" fontSize={12} />
              <YAxis stroke="#8b949e" fontSize={12} />
              <Tooltip 
                contentStyle={{ 
                  background: '#161b22', 
                  border: '1px solid #30363d', 
                  borderRadius: 6,
                  color: '#e6edf3'
                }}
                cursor={{ fill: 'rgba(88, 166, 255, 0.1)' }}
                formatter={(value) => `${value}M Gs`}
              />
              <Legend />
              <Bar 
                dataKey="facturacion" 
                fill="#58a6ff" 
                radius={[8, 8, 0, 0]}
                name="Facturación (Millones Gs)"
              />
            </BarChart>
          </ResponsiveContainer>
        );

      case 'pie':
        return (
          <ResponsiveContainer width="100%" height={350}>
            <PieChart>
              <Pie
                data={chartData.slice(0, 5)}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, market_share }) => `${name}: ${market_share?.toFixed(1)}%`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="market_share"
              >
                {chartData.slice(0, 5).map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip 
                contentStyle={{ 
                  background: '#161b22', 
                  border: '1px solid #30363d', 
                  borderRadius: 6,
                  color: '#e6edf3'
                }}
                formatter={(value) => `${value?.toFixed(2)}%`}
              />
            </PieChart>
          </ResponsiveContainer>
        );

      case 'line':
        return (
          <ResponsiveContainer width="100%" height={350}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#30363d" />
              <XAxis dataKey="name" stroke="#8b949e" fontSize={12} />
              <YAxis stroke="#8b949e" fontSize={12} />
              <Tooltip 
                contentStyle={{ 
                  background: '#161b22', 
                  border: '1px solid #30363d', 
                  borderRadius: 6,
                  color: '#e6edf3'
                }}
                cursor={{ stroke: '#58a6ff', strokeWidth: 2 }}
                formatter={(value) => `${value}M Gs`}
              />
              <Legend />
              <Line 
                type="monotone" 
                dataKey="facturacion" 
                stroke="#58a6ff" 
                dot={{ fill: '#58a6ff', r: 4 }}
                activeDot={{ r: 6 }}
                name="Facturación (Millones Gs)"
              />
            </LineChart>
          </ResponsiveContainer>
        );

      default:
        return null;
    }
  };

  return (
    <div className="dynamic-chart-container">
      <div className="chart-title">
        {config.type === 'bar' && '📊 Gráfico de Barras'}
        {config.type === 'pie' && '🥧 Gráfico Circular'}
        {config.type === 'line' && '📈 Gráfico de Línea'}
      </div>
      {renderChart()}
    </div>
  );
}