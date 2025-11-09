/**
 * HomePage Component
 * Página de inicio/dashboard principal
 */

import React, { FC, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './styles/HomePage.css';

const HomePage: FC = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [greeting, setGreeting] = useState('');

  useEffect(() => {
    const hour = new Date().getHours();
    if (hour < 12) {
      setGreeting('Buenos días');
    } else if (hour < 18) {
      setGreeting('Buenas tardes');
    } else {
      setGreeting('Buenas noches');
    }
  }, []);

  if (!user) {
    return (
      <div className="home-loading">
        <p>Cargando...</p>
      </div>
    );
  }

  return (
    <div className="home-page">
      <div className="welcome-section">
        <h2>{greeting}, {user.username}! 👋</h2>
        <p>Bienvenido a TaskFlow</p>
      </div>

      <div className="dashboard-grid">
        <div className="dashboard-card">
          <div className="card-header">
            <h3>📊 Proyectos</h3>
          </div>
          <div className="card-content">
            <p>Gestiona tus proyectos y colabora con tu equipo</p>
            <button className="btn btn-primary" onClick={() => navigate('/projects')}>
              Ver Proyectos
            </button>
          </div>
        </div>

        <div className="dashboard-card">
          <div className="card-header">
            <h3>✅ Tareas</h3>
          </div>
          <div className="card-content">
            <p>Visualiza y gestiona tus tareas asignadas</p>
            <button className="btn btn-primary" onClick={() => navigate('/tasks')}>
              Ver Tareas
            </button>
          </div>
        </div>

        <div className="dashboard-card">
          <div className="card-header">
            <h3>👤 Perfil</h3>
          </div>
          <div className="card-content">
            <p>
              <strong>Usuario:</strong> {user.username}
              <br />
              <strong>Email:</strong> {user.email}
            </p>
          </div>
        </div>

        <div className="dashboard-card">
          <div className="card-header">
            <h3>ℹ️ Información</h3>
          </div>
          <div className="card-content">
            <p>
              TaskFlow es una plataforma colaborativa de gestión de proyectos y tareas.
              Organiza tu trabajo, colabora con tu equipo y alcanza tus objetivos.
            </p>
          </div>
        </div>
      </div>

      <div className="features-section">
        <h3>Características Principales</h3>
        <ul className="features-list">
          <li>✓ Gestión de proyectos colaborativos</li>
          <li>✓ Asignación y seguimiento de tareas</li>
          <li>✓ Definición de prioridades</li>
          <li>✓ Sistema de roles y permisos</li>
          <li>✓ Autenticación JWT segura</li>
          <li>✓ API REST completa</li>
        </ul>
      </div>
    </div>
  );
};

export default HomePage;
