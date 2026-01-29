import React, { useState, useContext } from 'react';
import { AuthContext } from './Auth';
import './LoginPage.css';

export default function LoginPage() {
  const { login, register, error } = useContext(AuthContext);
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      if (isLogin) {
        await login(username, password);
      } else {
        await register(username, password);
      }
    } catch (e) {
      // Error ya se maneja en el contexto
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <div className="login-box">
          <h1>JARVIS</h1>
          <p className="subtitle">Intelligence Platform</p>

          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <input
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                disabled={loading}
              />
            </div>

            <div className="form-group">
              <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                disabled={loading}
              />
            </div>

            {error && <div className="error-message">{error}</div>}

            <button type="submit" disabled={loading} className="btn-submit">
              {loading ? 'Loading...' : isLogin ? 'Login' : 'Register'}
            </button>
          </form>

          <div className="toggle-auth">
            <p>
              {isLogin ? "¿No tienes cuenta?" : "¿Ya tienes cuenta?"}
              <button
                type="button"
                onClick={() => {
                  setIsLogin(!isLogin);
                  setUsername('');
                  setPassword('');
                }}
              >
                {isLogin ? 'Registrate' : 'Login'}
              </button>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}