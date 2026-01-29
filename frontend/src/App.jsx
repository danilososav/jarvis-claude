import React, { useContext } from 'react';
import { AuthContext } from './Auth';
import LoginPage from './LoginPage';
import ChatApp from './ChatApp';

export default function App() {
  const { user, loading } = useContext(AuthContext);

  if (loading) {
    return <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100vh', color: 'white' }}>Loading...</div>;
  }

  return user ? <ChatApp /> : <LoginPage />;
}