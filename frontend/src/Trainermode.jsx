import React, { useState, useContext } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import { AuthContext } from './Auth';
import './TrainerMode.css';

const API_URL = 'http://127.0.0.1:5000/api';

export function TrainerMode({ message, index, userQuery, data }) {
  const { user } = useContext(AuthContext);
  const [isOpen, setIsOpen] = useState(false);
  const [correctedText, setCorrectedText] = useState(message.content);
  const [feedbackType, setFeedbackType] = useState('correction');
  const [notes, setNotes] = useState('');
  const [loading, setLoading] = useState(false);
  const [validationResult, setValidationResult] = useState(null);

  if (user?.role !== 'trainer' || message.type !== 'bot') {
    return null;
  }

  const handleSubmit = async () => {
    setLoading(true);
    setValidationResult(null);

    // DEBUG
    console.log('🔍 DEBUG - Data recibida:', data);
    console.log('🔍 DEBUG - Message completo:', message);
    
    try {
      const token = Cookies.get('jarvis_token');
      const res = await axios.post(
        `${API_URL}/trainer/feedback`,
        {
          conversation_id: index,
          original_query: userQuery,
          original_response: message.content,
          corrected_response: correctedText,
          feedback_type: feedbackType,
          notes: notes,
          data_snapshot: data || []  // NUEVO - Datos para validación
        },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      if (res.data.success) {
        // Mostrar resultado de validación de Claude
        setValidationResult(res.data.validation);
      }
    } catch (e) {
      console.error('Error submitting feedback:', e);
      setValidationResult({
        status: 'error',
        title: '❌ Error',
        message: 'Hubo un error al enviar la corrección. Intenta nuevamente.'
      });
    } finally {
      setLoading(false);
    }
  };

  const handleEscalate = async () => {
    const reason = prompt('¿Por qué crees que la validación de Claude es incorrecta?');
    
    if (!reason || !reason.trim()) {
      return;
    }

    try {
      const token = Cookies.get('jarvis_token');
      const res = await axios.post(
        `${API_URL}/trainer/feedback/${validationResult.feedback_id}/escalate`,
        { reason: reason },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      if (res.data.success) {
        alert('✅ ' + res.data.message);
        setIsOpen(false);
        setValidationResult(null);
      }
    } catch (e) {
      console.error('Error escalating:', e);
      alert('Error al reportar. Intenta nuevamente.');
    }
  };

  const handleClose = () => {
    setIsOpen(false);
    setValidationResult(null);
    setCorrectedText(message.content);
    setNotes('');
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
            <button className="close-trainer" onClick={handleClose}>
              ✕
            </button>
          </div>

          <div className="trainer-form">
            {!validationResult ? (
              <>
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
                  {loading ? 'Validando con Claude...' : 'Enviar corrección'}
                </button>
              </>
            ) : (
              <div className="validation-result">
                <h3 className={`validation-title ${validationResult.status}`}>
                  {validationResult.title}
                </h3>
                
                <div className="validation-message">
                  {validationResult.message}
                </div>

                {validationResult.details && (
                  <details className="validation-details">
                    <summary>Ver detalles técnicos</summary>
                    <p>{validationResult.details}</p>
                  </details>
                )}

                <div className="validation-actions">
                  {validationResult.show_escalate_button && (
                    <button 
                      className="btn-escalate"
                      onClick={handleEscalate}
                    >
                      🚨 Reportar al Administrador
                    </button>
                  )}
                  
                  <button 
                    className="btn-close"
                    onClick={handleClose}
                  >
                    Cerrar
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}