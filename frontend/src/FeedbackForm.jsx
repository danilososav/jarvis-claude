import React, { useState } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import './FeedbackForm.css';

const API_URL = 'http://127.0.0.1:5000/api';

const CATEGORIES = [
  'Facturación',
  'Rankings',
  'Clientes',
  'Comparativas',
  'Análisis',
  'Otros'
];

export function FeedbackForm({ message, userQuery, onClose, onSave }) {
  const [category, setCategory] = useState('');
  const [tags, setTags] = useState([]);
  const [tagInput, setTagInput] = useState('');
  const [notes, setNotes] = useState('');
  const [correctedResponse, setCorrectedResponse] = useState(message?.content || '');
  const [loading, setLoading] = useState(false);
  const [message_feedback, setMessage] = useState(null);

  const addTag = () => {
    if (tagInput.trim() && !tags.includes(tagInput.trim())) {
      setTags([...tags, tagInput.trim()]);
      setTagInput('');
    }
  };

  const removeTag = (tag) => {
    setTags(tags.filter(t => t !== tag));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!category) {
      setMessage({ type: 'error', text: 'Selecciona una categoría' });
      return;
    }

    if (!correctedResponse.trim()) {
      setMessage({ type: 'error', text: 'Escribe la respuesta corregida' });
      return;
    }

    setLoading(true);
    try {
      const token = Cookies.get('jarvis_token');
      const res = await axios.post(
        `${API_URL}/trainer/feedback`,
        {
          original_query: userQuery,
          original_response: message?.content || '',
          corrected_response: correctedResponse,
          feedback_type: 'correction',
          notes: notes,
          category: category,
          tags: tags,
          chart_config: message?.chart_config || null,
          query_type: message?.query_type || 'generico'
        },
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );

      if (res.data.success) {
        setMessage({ type: 'success', text: '✅ Feedback guardado correctamente' });
        setTimeout(() => {
          onClose();
          if (onSave) onSave();
        }, 1500);
      }
    } catch (e) {
      console.error('Error:', e);
      setMessage({ type: 'error', text: 'Error guardando feedback' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="feedback-form-overlay" onClick={onClose}>
      <div className="feedback-form-modal" onClick={(e) => e.stopPropagation()}>
        <div className="feedback-form-header">
          <h3>✏️ Corregir Respuesta</h3>
          <button className="close-btn" onClick={onClose}>✕</button>
        </div>

        <form className="feedback-form" onSubmit={handleSubmit}>
          {message_feedback && (
            <div className={`notification ${message_feedback.type}`}>
              {message_feedback.text}
            </div>
          )}

          {/* Original Query */}
          <div className="form-group">
            <label>📝 Pregunta Original</label>
            <div className="readonly-field">{userQuery}</div>
          </div>

          {/* Original Response */}
          <div className="form-group">
            <label>💬 Respuesta Original</label>
            <div className="readonly-field">{message?.content}</div>
          </div>

          {/* Categoría */}
          <div className="form-group">
            <label>📂 Categoría *</label>
            <select 
              value={category} 
              onChange={(e) => setCategory(e.target.value)}
              className="form-select"
              required
            >
              <option value="">-- Selecciona categoría --</option>
              {CATEGORIES.map(cat => (
                <option key={cat} value={cat}>{cat}</option>
              ))}
            </select>
          </div>

          {/* Tags */}
          <div className="form-group">
            <label>🏷️ Etiquetas (tags)</label>
            <div className="tags-input">
              <input
                type="text"
                value={tagInput}
                onChange={(e) => setTagInput(e.target.value)}
                onKeyPress={(e) => {
                  if (e.key === 'Enter') {
                    e.preventDefault();
                    addTag();
                  }
                }}
                placeholder="Escribe y presiona Enter"
                className="tag-input-field"
              />
              <button type="button" onClick={addTag} className="tag-add-btn">
                ➕
              </button>
            </div>
            {tags.length > 0 && (
              <div className="tags-list">
                {tags.map(tag => (
                  <span key={tag} className="tag-item">
                    {tag}
                    <button 
                      type="button" 
                      onClick={() => removeTag(tag)}
                      className="tag-remove"
                    >
                      ✕
                    </button>
                  </span>
                ))}
              </div>
            )}
          </div>

          {/* Respuesta Corregida */}
          <div className="form-group">
            <label>✅ Respuesta Corregida *</label>
            <textarea
              value={correctedResponse}
              onChange={(e) => setCorrectedResponse(e.target.value)}
              className="form-textarea"
              rows="6"
              required
            />
          </div>

          {/* Notas */}
          <div className="form-group">
            <label>📌 Notas (opcional)</label>
            <textarea
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              className="form-textarea"
              rows="3"
              placeholder="Motivo de la corrección, contexto, etc."
            />
          </div>

          {/* Botones */}
          <div className="form-buttons">
            <button 
              type="button" 
              onClick={onClose}
              className="btn-cancel"
            >
              Cancelar
            </button>
            <button 
              type="submit"
              className="btn-submit"
              disabled={loading}
            >
              {loading ? '⏳ Guardando...' : '💾 Guardar Feedback'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
