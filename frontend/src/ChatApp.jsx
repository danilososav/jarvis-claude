import React, { useState, useEffect, useRef, useContext } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import { AuthContext } from './Auth';
import './ChatApp.css';
import { TopClientesChart, MarketShareChart, ClienteAnalysisChart } from './Charts';
import './Charts.css';
import { TrainerMode } from './TrainerMode';
import { DynamicChart } from './DynamicChart';
import { UploadExcel } from './UploadExcel';

const API_URL = 'http://127.0.0.1:5000/api';

export default function ChatApp() {
  const { user, logout } = useContext(AuthContext);
  const [messages, setMessages] = useState([]);
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);
  const messagesEndRef = useRef(null);

    const loadHistory = async () => {
    try {
      const token = Cookies.get('jarvis_token');
      const res = await axios.get(`${API_URL}/chat/history`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setHistory(res.data.conversations || []);
    } catch (e) {
      console.error('Error loading history:', e);
    }
  };

useEffect(() => {
  messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
}, [messages]);

useEffect(() => {
  loadHistory();
}, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

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
      { query: msg },
      { headers: { Authorization: `Bearer ${token}` } }
    );

    if (res.data.success) {
      setMessages(p => [...p, { 
        type: 'bot', 
        content: res.data.response,
        query_type: res.data.query_type,
        chart_config: res.data.chart_config,
        rows: res.data.rows
      }]);
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

  const selectConv = (conv) => {
    setMessages([
      { type: 'user', content: conv.query },
      { type: 'bot', content: conv.response }
    ]);
  };

  const deleteConv = async (id) => {
  try {
    const token = Cookies.get('jarvis_token');
    const res = await axios.delete(`${API_URL}/chat/history/${id}`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    
    if (res.data.success) {
      setHistory(h => h.filter(x => x.id !== id));
      console.log('✅ Chat eliminado:', id);
    }
  } catch (e) {
    console.error('❌ Error deleting:', e.response?.data || e.message);
  }
};

  const handleNewChat = () => {
    setMessages([]);
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
        <UploadExcel />

        <div className="history-container">
          <div className="history-label">Conversations</div>
          <div className="history-list">
            {history.length ? (
              history.map(c => (
                <div key={c.id} className="history-item">
                  <span onClick={() => selectConv(c)} className="history-text">
                    {c.query.substring(0, 40)}
                  </span>
                  <button
                    className="delete-btn"
                    onClick={() => deleteConv(c.id)}
                    title="Delete"
                  >
                    ×
                  </button>
                </div>
              ))
            ) : (
              <div className="history-empty">No conversations yet</div>
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
                    <div className={`message ${m.type}`}>
                      <div className="message-bubble">
                        {m.content}
                        {m.type === 'bot' && <TrainerMode message={m} index={i} userQuery={messages[i-1]?.content || ''} />}
                      </div>
                    </div>
                    {m.chart_config && m.rows && <DynamicChart data={m.rows} config={m.chart_config} />}
                    {m.query_type === 'ranking' && m.rows && !m.chart_config && <TopClientesChart data={m.rows} />}
                    {m.query_type === 'ranking' && m.rows && !m.chart_config && <MarketShareChart data={m.rows} />}
                    {m.query_type === 'facturacion' && m.rows && !m.chart_config && <ClienteAnalysisChart data={m.rows} />}
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