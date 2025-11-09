/**
 * MainLayout Component
 * Layout principal con header y footer para todas las páginas autenticadas
 */

import React, { FC, ReactNode } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './styles/MainLayout.css';

interface MainLayoutProps {
  children: ReactNode;
}

const MainLayout: FC<MainLayoutProps> = ({ children }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const { user, logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const isActive = (path: string) => location.pathname === path;

  return (
    <div className="main-layout">
      {/* Header */}
      <header className="main-header">
        <div className="header-container">
          <div className="logo-section">
            <h1 className="logo">TaskFlow</h1>
            <p className="subtitle">Gestor de Tareas Colaborativo</p>
          </div>

          <nav className="main-nav">
            <button
              className={`nav-link ${isActive('/projects') ? 'active' : ''}`}
              onClick={() => navigate('/projects')}
            >
              📋 Proyectos
            </button>
            <button
              className={`nav-link ${isActive('/tasks') ? 'active' : ''}`}
              onClick={() => navigate('/tasks')}
            >
              ✓ Mis Tareas
            </button>
            <button
              className={`nav-link ${isActive('/') ? 'active' : ''}`}
              onClick={() => navigate('/')}
            >
              🏠 Inicio
            </button>
          </nav>

          <div className="user-section">
            <div className="user-info">
              <span className="user-name">{user?.username}</span>
              <span className="user-email">{user?.email}</span>
            </div>
            <button
              className="btn btn-logout"
              onClick={handleLogout}
              title="Cerrar sesión"
            >
              🚪 Salir
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="main-content">
        {children}
      </main>

      {/* Footer */}
      <footer className="main-footer">
        <div className="footer-container">
          <div className="footer-section">
            <h3>TaskFlow</h3>
            <p>Plataforma de gestión de tareas colaborativa</p>
          </div>

          <div className="footer-section">
            <h4>Enlaces Rápidos</h4>
            <ul>
              <li>
                <button onClick={() => navigate('/projects')}>Proyectos</button>
              </li>
              <li>
                <button onClick={() => navigate('/tasks')}>Mis Tareas</button>
              </li>
              <li>
                <button onClick={() => navigate('/')}>Inicio</button>
              </li>
            </ul>
          </div>

          <div className="footer-section">
            <h4>Usuario</h4>
            <ul>
              <li>
                <span>{user?.username}</span>
              </li>
              <li>
                <span>{user?.email}</span>
              </li>
              <li>
                <button onClick={handleLogout}>Cerrar Sesión</button>
              </li>
            </ul>
          </div>

          <div className="footer-section">
            <h4>Información</h4>
            <ul>
              <li>
                <a href="#privacy">Privacidad</a>
              </li>
              <li>
                <a href="#terms">Términos</a>
              </li>
              <li>
                <a href="#support">Soporte</a>
              </li>
            </ul>
          </div>
        </div>

        <div className="footer-bottom">
          <p>
            © {new Date().getFullYear()} TaskFlow. Todos los derechos reservados.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default MainLayout;
