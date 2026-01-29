import React, { useState, useContext } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import { AuthContext } from './Auth';
import './TrainerMode.css';

const API_URL = 'http://127.0.0.1:5000/api';

export function TrainerMode({ message, index, userQuery }) {
  const { user } = useContext(AuthContext);
  const [isOpen, setIsOpen] = useState(false);
  const [correctedText, setCorrectedText] = useState(message.content);
  const [feedbackType, setFeedbackType] = useState('correction');
  const [notes, setNotes] = useState('');
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  if (user?.role !== 'trainer' || message.type !== 'bot') {
    return null;
  }

  const handleSubmit = async () => {
  setLoading(true);
  try {
    const token = Cookies.get('jarvis_token');
    const res = await axios.post(
    `${API_URL}/trainer/feedback`,
    {
      conversation_id: index,
      original_query: userQuery,  // Usar la prop
      original_response: message.content,
      corrected_response: correctedText,
      feedback_type: feedbackType,
      notes: notes
    },
      { headers: { Authorization: `Bearer ${token}` } }
    );

    if (res.data.success) {
      setSubmitted(true);
      setTimeout(() => {
        setIsOpen(false);
        setSubmitted(false);
        setCorrectedText(message.content);
        setNotes('');
      }, 2000);
    }
  } catch (e) {
    console.error('Error submitting feedback:', e);
  } finally {
    setLoading(false);
  }
};

  return (
    <div className="trainer-mode">
      <button
        className="trainer-btn"
        onClick={() => setIsOpen(!isOpen)}
        title="Corregir respuesta"
      >
        ✏️
      </button>

      {isOpen && (
        <div className="trainer-panel">
          <div className="trainer-header">
            <h4>Trainer Mode - Corregir respuesta</h4>
            <button
              className="close-trainer"
              onClick={() => setIsOpen(false)}
            >
              ✕
            </button>
          </div>

          <div className="trainer-form">
            <div className="form-group">
              <label>Tipo de feedback</label>
              <select
                value={feedbackType}
                onChange={(e) => setFeedbackType(e.target.value)}
              >
                <option value="correction">Corrección</option>
                <option value="improvement">Mejora</option>
                <option value="error">Error</option>
              </select>
            </div>

            <div className="form-group">
              <label>Respuesta original</label>
              <textarea
                value={message.content}
                disabled
                className="disabled-textarea"
              />
            </div>

            <div className="form-group">
              <label>Respuesta corregida</label>
              <textarea
                value={correctedText}
                onChange={(e) => setCorrectedText(e.target.value)}
                placeholder="Ingresa la respuesta corregida..."
              />
            </div>

            <div className="form-group">
              <label>Notas</label>
              <textarea
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                placeholder="¿Por qué esta corrección?"
                rows="2"
              />
            </div>

            <button
              className="btn-submit-feedback"
              onClick={handleSubmit}
              disabled={loading}
            >
              {loading ? 'Enviando...' : 'Guardar corrección'}
            </button>

            {submitted && (
              <div className="success-message">
                ✅ Corrección guardada exitosamente
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}