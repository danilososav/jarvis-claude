import React, { createContext, useState, useEffect } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';

export const AuthContext = createContext();

const API_URL = 'http://127.0.0.1:5000/api';

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const token = Cookies.get('jarvis_token');
    if (token) {
      verifyToken(token);
    } else {
      setLoading(false);
    }
  }, []);

  const verifyToken = async (token) => {
    try {
      const res = await axios.get(`${API_URL}/auth/verify`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setUser(res.data);
      setError(null);
    } catch (e) {
      Cookies.remove('jarvis_token');
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  const register = async (username, password) => {
    setLoading(true);
    try {
      const res = await axios.post(`${API_URL}/auth/register`, { username, password });
      Cookies.set('jarvis_token', res.data.token, { expires: 7 });
      setUser(res.data);
      setError(null);
      return res.data;
    } catch (e) {
      const msg = e.response?.data?.error || 'Error registrando';
      setError(msg);
      throw new Error(msg);
    } finally {
      setLoading(false);
    }
  };

  const login = async (username, password) => {
    setLoading(true);
    try {
      const res = await axios.post(`${API_URL}/auth/login`, { username, password });
      Cookies.set('jarvis_token', res.data.token, { expires: 7 });
      setUser(res.data);
      setError(null);
      return res.data;
    } catch (e) {
      const msg = e.response?.data?.error || 'Error en login';
      setError(msg);
      throw new Error(msg);
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    Cookies.remove('jarvis_token');
    setUser(null);
    setError(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, error, register, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}