/**
 * AuthPage Component
 * Página que contiene los formularios de login y registro
 */

import React, { FC, useState } from 'react';
import { useLocation } from 'react-router-dom';
import LoginForm from '../components/auth/LoginForm';
import RegisterForm from '../components/auth/RegisterForm';
import '../styles/AuthPage.css';

type AuthMode = 'login' | 'register';

const AuthPage: FC = () => {
  const location = useLocation();
  
  // Determinar el modo inicial basado en la ruta
  const isRegisterPage = location.pathname === '/register';
  const [mode, setMode] = useState<AuthMode>(isRegisterPage ? 'register' : 'login');

  return (
    <div className="auth-page">
      <div className="auth-container">
        {/* Header */}
        <div className="auth-header">
          <h1>TaskFlow</h1>
          <p className="auth-subtitle">Gestor de Tareas Colaborativo</p>
        </div>

        {/* Tabs/Switches */}
        <div className="auth-tabs">
          <button
            className={`auth-tab ${mode === 'login' ? 'active' : ''}`}
            onClick={() => setMode('login')}
          >
            Iniciar Sesión
          </button>
          <button
            className={`auth-tab ${mode === 'register' ? 'active' : ''}`}
            onClick={() => setMode('register')}
          >
            Registrarse
          </button>
        </div>

        {/* Formularios */}
        <div className="auth-forms">
          {mode === 'login' ? (
            <div className="form-wrapper active">
              <LoginForm onSuccess={() => {
                // El LoginForm se encarga de la redirección
              }} />
            </div>
          ) : (
            <div className="form-wrapper active">
              <RegisterForm onSuccess={() => {
                // El RegisterForm se encarga de la redirección
              }} />
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="auth-footer">
          <p className="footer-text">
            © {new Date().getFullYear()} TaskFlow. Todos los derechos reservados.
          </p>
          <div className="footer-links">
            <a href="#" className="footer-link">Privacidad</a>
            <span className="separator">•</span>
            <a href="#" className="footer-link">Términos</a>
            <span className="separator">•</span>
            <a href="#" className="footer-link">Soporte</a>
          </div>
        </div>
      </div>

      {/* Ilustración o decoración lateral (opcional) */}
      <div className="auth-decoration">
        <div className="decoration-content">
          <h2>Bienvenido a TaskFlow</h2>
          <ul className="decoration-features">
            <li>✓ Gestión colaborativa de tareas</li>
            <li>✓ Asignación de prioridades</li>
            <li>✓ Seguimiento de proyectos</li>
            <li>✓ Integraciones avanzadas</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default AuthPage;
