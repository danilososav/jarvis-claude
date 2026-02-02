import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import './SavedResponses.css';

const API_URL = 'http://127.0.0.1:5000/api';

export function SavedResponses() {
  const [isOpen, setIsOpen] = useState(false);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [feedbacks, setFeedbacks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  const loadCategories = async () => {
    try {
      const token = Cookies.get('jarvis_token');
      const res = await axios.get(`${API_URL}/trainer/feedback/categories`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setCategories(res.data.categories || []);
    } catch (e) {
      console.error('Error loading categories:', e);
    }
  };

  const loadFeedbacks = async (category) => {
    setLoading(true);
    try {
      const token = Cookies.get('jarvis_token');
      const res = await axios.get(
        `${API_URL}/trainer/feedback?category=${category}`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setFeedbacks(res.data.feedbacks || []);
    } catch (e) {
      console.error('Error loading feedbacks:', e);
    } finally {
      setLoading(false);
    }
  };

  const handleOpen = () => {
    setIsOpen(true);
    loadCategories();
  };

  const handleSelectCategory = (category) => {
    setSelectedCategory(category);
    loadFeedbacks(category);
    setSearchQuery('');
  };

  const filteredFeedbacks = feedbacks.filter(fb =>
    fb.original_query.toLowerCase().includes(searchQuery.toLowerCase()) ||
    fb.corrected_response.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <>
      <button className="saved-responses-btn" onClick={handleOpen} title="Respuestas Guardadas">
        💾 Respuestas Guardadas
      </button>

      {isOpen && (
        <div className="saved-responses-overlay" onClick={() => setIsOpen(false)}>
          <div className="saved-responses-modal" onClick={(e) => e.stopPropagation()}>
            <div className="saved-responses-header">
              <h3>💾 Respuestas Guardadas por Categoría</h3>
              <button className="close-btn" onClick={() => setIsOpen(false)}>✕</button>
            </div>

            <div className="saved-responses-content">
              {!selectedCategory ? (
                <div className="categories-view">
                  <h4>Selecciona una categoría</h4>
                  <div className="categories-grid">
                    {categories.length > 0 ? (
                      categories.map(cat => (
                        <button
                          key={cat}
                          className="category-card"
                          onClick={() => handleSelectCategory(cat)}
                        >
                          <span className="category-icon">📂</span>
                          <span className="category-name">{cat}</span>
                        </button>
                      ))
                    ) : (
                      <p className="empty-message">Sin categorías creadas</p>
                    )}
                  </div>
                </div>
              ) : (
                <div className="feedbacks-view">
                  <div className="feedbacks-header">
                    <button 
                      className="back-btn"
                      onClick={() => setSelectedCategory(null)}
                    >
                      ← Volver
                    </button>
                    <h4>{selectedCategory}</h4>
                    <div className="search-box">
                      <input
                        type="text"
                        placeholder="🔍 Buscar..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        className="search-input"
                      />
                    </div>
                  </div>

                  {loading ? (
                    <p className="loading">Cargando...</p>
                  ) : filteredFeedbacks.length > 0 ? (
                    <div className="feedbacks-list">
                      {filteredFeedbacks.map(fb => (
                        <div key={fb.id} className="feedback-item">
                          <div className="feedback-query">
                            <strong>❓ Pregunta:</strong>
                            <p>{fb.original_query}</p>
                          </div>

                          <div className="feedback-response">
                            <strong>✅ Respuesta Corregida:</strong>
                            <p>{fb.corrected_response}</p>
                          </div>

                          {fb.tags && fb.tags.length > 0 && (
                            <div className="feedback-tags">
                              {fb.tags.map(tag => (
                                <span key={tag} className="feedback-tag">
                                  {tag}
                                </span>
                              ))}
                            </div>
                          )}

                          <div className="feedback-meta">
                            <span className="meta-item">
                              🎯 Tipo: {fb.query_type}
                            </span>
                            <span className="meta-item">
                              📊 Score: {fb.similarity_score || 'N/A'}
                            </span>
                            <span className="meta-item">
                              📅 {new Date(fb.created_at).toLocaleDateString('es-PY')}
                            </span>
                          </div>

                          {fb.notes && (
                            <div className="feedback-notes">
                              <strong>📌 Notas:</strong>
                              <p>{fb.notes}</p>
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="empty-message">Sin respuestas en esta categoría</p>
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
