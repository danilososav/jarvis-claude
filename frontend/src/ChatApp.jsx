import React, { useState, useEffect, useRef, useContext } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import { AuthContext } from './Auth';
import './ChatApp.css';
import { ApexChartCard } from './ApexChartCard';
import { DataTable } from './DataTable';
import { KPICard } from './KPICard';
import './Charts.css';
import { TrainerMode } from './TrainerMode';
import { UploadExcel } from './UploadExcel';
import { ImportExport } from './ImportExport';
import { ExportButtons } from './ExportButtons';
import { AuditLogs } from './AuditLogs';
import { SavedResponses } from './SavedResponses';

const API_URL = 'http://127.0.0.1:5000/api';

export default function ChatApp() {
  const { user, logout } = useContext(AuthContext);
  const [messages, setMessages] = useState([]);
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);
  const messagesEndRef = useRef(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [sessionId, setSessionId] = useState(null);

  const loadHistory = async () => {
    try {
      const token = Cookies.get('jarvis_token');
      const res = await axios.get(`${API_URL}/chat/history`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      const sessions = res.data.sessions || [];
      
      setHistory(sessions.map(s => ({
        session_id: s.session_id,
        messages: s.messages,
        created_at: s.created_at
      })));
    } catch (e) {
      console.error('Error loading history:', e);
    }
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  useEffect(() => {
    if (!sessionId) {
      setSessionId(`session_${user.user_id}_${Date.now()}`);
    }
  }, [user, sessionId]);

  useEffect(() => {
    loadHistory();
  }, []);

  const sendQuery = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    const msg = query;
    setQuery('');
    setMessages(p => [...p, { type: 'user', content: msg }]);
    setLoading(true);

    try {
      const token = Cookies.get('jarvis_token');
      
      const res = await axios.post(
        `${API_URL}/query`,
        { query: msg, session_id: sessionId },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      if (res.data.success) {
        // Nuevo sistema: backend envía array de respuestas
        const responses = res.data.responses || [];
        
        // Agregar cada respuesta como mensaje separado
        responses.forEach(response => {
          if (response.type === 'info') {
            // Mensaje informativo
            setMessages(p => [...p, { 
              type: 'bot',
              content: response.content,
              isInfo: true
            }]);
          } else if (response.type === 'chart') {
            // Gráfico
            setMessages(p => [...p, { 
              type: 'bot',
              isChart: true,
              chart_config: response.chart_config,
              chart_data: response.data,
              query_type: response.query_type
            }]);
          } else if (response.type === 'table') {
            // Tabla
            setMessages(p => [...p, { 
              type: 'bot',
              isTable: true,
              table_config: response.table_config,
              table_data: response.data,
              query_type: response.query_type
            }]);
          } else if (response.type === 'kpi') {
            // KPI Card
            setMessages(p => [...p, { 
              type: 'bot',
              isKPI: true,
              kpi_config: response.kpi_config,
              kpi_data: response.data,
              query_type: response.query_type
            }]);
          } else if (response.type === 'text') {
            // Texto de análisis
            setMessages(p => [...p, { 
              type: 'bot',
              content: response.content,
              query_type: response.query_type,
              data: response.data
            }]);
          }
        });
        
        loadHistory();
      } else {
        setMessages(p => [...p, { type: 'error', content: `Error: ${res.data.error}` }]);
      }
    } catch (e) {
      setMessages(p => [...p, { type: 'error', content: `Error: ${e.message}` }]);
    } finally {
      setLoading(false);
    }
  };

const selectSession = (session) => {
  setMessages(session.messages.flatMap((m) => {
    const messages = [{ type: 'user', content: m.query }];
    
    // Si tiene chart_config, crear mensaje de gráfico
    if (m.chart_config) {
      messages.push({
        type: 'bot',
        isChart: true,
        chart_config: m.chart_config,
        chart_data: m.rows,
        query_type: m.query_type
      });
    }
    
    // Si tiene texto de respuesta, agregar mensaje de texto
    if (m.response) {
      messages.push({
        type: 'bot',
        content: m.response,
        query_type: m.query_type,
        data: m.rows
      });
    }
    
    return messages;
  }));
};

  const deleteConv = async (id) => {
    try {
      const token = Cookies.get('jarvis_token');
      const res = await axios.delete(`${API_URL}/chat/history/${id}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      if (res.data.success) {
        loadHistory();
        console.log('✅ Chat eliminado:', id);
      }
    } catch (e) {
      console.error('❌ Error deleting:', e.response?.data || e.message);
    }
  };

  const handleNewChat = () => {
    setMessages([]);
    setSessionId(`session_${user.user_id}_${Date.now()}`);
  };

  const handleLogout = () => {
    logout();
  };

  return (
    <div className="app-layout">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <h1>JARVIS</h1>
          <button className="logout-btn" onClick={handleLogout} title="Logout">
            ⎋
          </button>
        </div>

        <button className="new-chat-btn" onClick={handleNewChat}>
          + New Chat
        </button>
        <ImportExport />
        <SavedResponses />
        <AuditLogs />
        
        <div className="history-container">
          <div className="history-label">Conversations</div>
          
          <input
            type="text"
            placeholder="🔍 Buscar..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="search-input"
          />
          
          <div className="history-list">
            {history.length ? (
              history
                .filter(session => 
                  session.messages.some(m =>
                    m.query.toLowerCase().includes(searchQuery.toLowerCase()) ||
                    m.response.toLowerCase().includes(searchQuery.toLowerCase())
                  )
                )
                .map(session => (
                  <div key={session.session_id} className="history-session">
                    <button
                      className="history-item"
                      onClick={() => selectSession(session)}
                      title={session.messages[0]?.query}
                    >
                      {session.messages[0]?.query.substring(0, 35)}...
                    </button>
                    <button 
                      className="delete-btn"
                      onClick={() => deleteConv(session.messages[0].id)}
                      title="Eliminar chat"
                    >
                      🗑️
                    </button>
                  </div>
                ))
            ) : (
              <div className="history-empty">Sin conversaciones</div>
            )}
          </div>
        </div>

        <div className="sidebar-footer">
          <div className="user-info">
            <div className="user-avatar">{user?.username?.[0]?.toUpperCase()}</div>
            <div>
              <div className="user-name">{user?.username}</div>
              <div className="user-role">{user?.role}</div>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Chat */}
      <main className="chat-area">
        <div className="chat-header">
          <div>
            <h2>JARVIS - Analytics</h2>
            <p>Facturación, rankings, comparaciones y análisis de clientes.</p>
          </div>
        </div>

        <div className="chat-container">
          {!messages.length ? (
            <div className="welcome-state">
              <h3>Welcome to JARVIS</h3>
              <p>Ask about billing, clients, rankings, comparisons and investment analysis</p>
              <div className="example-queries">
                <button onClick={() => { setQuery('Muestra un gráfico de barras de los top 5 clientes'); }}>Top 5 clientes</button>
                <button onClick={() => { setQuery('Gráfico: clientes que más facturaron'); }}>Clientes facturación</button>
                <button onClick={() => { setQuery('Cuánto facturó CERVEPAR?'); }}>Facturación cliente</button>
              </div>
            </div>
          ) : (
            <div className="messages">
              {messages.map((m, i) => (
                <div key={i}>
                  {/* Mensaje de usuario */}
                  {m.type === 'user' && (
                    <div className="message user">
                      <div className="message-bubble">{m.content}</div>
                    </div>
                  )}
                  
                  {/* Mensaje de error */}
                  {m.type === 'error' && (
                    <div className="message error">
                      <div className="message-bubble">{m.content}</div>
                    </div>
                  )}
                  
                  {/* Mensaje informativo */}
                  {m.type === 'bot' && m.isInfo && (
                    <div className="message bot">
                      <div className="message-bubble info-message">{m.content}</div>
                    </div>
                  )}
                  
                  {/* Gráfico (solo gráfico, sin texto) */}
                  {m.type === 'bot' && m.isChart && (
                    <div className="message bot">
                      <ApexChartCard 
                        config={m.chart_config} 
                        data={m.chart_data} 
                      />
                    </div>
                  )}
                  
                  {/* Tabla (solo tabla, sin texto) */}
                  {m.type === 'bot' && m.isTable && (
                    <div className="message bot">
                      <DataTable 
                        config={m.table_config} 
                        data={m.table_data} 
                      />
                    </div>
                  )}
                  
                  {/* KPI Card (solo métricas, sin texto) */}
                  {m.type === 'bot' && m.isKPI && (
                    <div className="message bot">
                      <KPICard 
                        config={m.kpi_config} 
                        data={m.kpi_data} 
                      />
                    </div>
                  )}
                  
                  {/* Texto de análisis (sin gráfico ni tabla ni KPI) */}
                  {m.type === 'bot' && !m.isChart && !m.isTable && !m.isKPI && !m.isInfo && m.content && (
                    <div className="message bot">
                      <div className="message-bubble">
                        {m.content}
                        <TrainerMode 
                          message={m} 
                          index={i} 
                          userQuery={messages[i-1]?.content || ''} 
                          data={m.data || m.rows || []}
                        />
                      </div>
                      <ExportButtons message={m} chartConfig={null} chartData={m.data} />
                    </div>
                  )}
                </div>
              ))}
              {loading && (
                <div className="message bot">
                  <div className="message-bubble loading">Processing...</div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>

        <form className="input-form" onSubmit={sendQuery}>
          <textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyPress={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendQuery(e);
              }
            }}
            placeholder="Ask me anything..."
            disabled={loading}
          />
          <button type="submit" disabled={loading}>
            Send
          </button>
        </form>
      </main>
    </div>
  );
}