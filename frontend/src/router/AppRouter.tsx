/**
 * Router Configuration
 * Define todas las rutas de la aplicación con rutas protegidas y públicas
 */

import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import ProtectedRoute from '../components/auth/ProtectedRoute';

// Páginas
import AuthPage from '../pages/AuthPage';
import ProjectsPage from '../pages/ProjectsPage';
import ProjectDetailPage from '../pages/ProjectDetailPage';
import TasksPage from '../pages/TasksPage';
// Páginas futuras
// import SettingsPage from '../pages/SettingsPage';

/**
 * App Router Component
 * 
 * Rutas públicas (sin autenticación requerida):
 * - /login - Página de inicio de sesión
 * - /register - Página de registro
 * - / - Redirige a /login o /dashboard según autenticación
 * 
 * Rutas protegidas (requieren autenticación):
 * - /dashboard - Dashboard principal
 * - /projects - Lista de proyectos
 * - /projects/:id - Detalle de proyecto
 * - /tasks - Mis tareas
 * - /settings - Configuración
 */
const AppRouter: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        {/* Rutas públicas */}
        <Route path="/login" element={<AuthPage />} />
        <Route path="/register" element={<AuthPage />} />

        {/* Rutas protegidas */}
        <Route
          path="/projects"
          element={
            <ProtectedRoute>
              <ProjectsPage />
            </ProtectedRoute>
          }
        />

        <Route
          path="/projects/:id"
          element={
            <ProtectedRoute>
              <ProjectDetailPage />
            </ProtectedRoute>
          }
        />

        <Route
          path="/tasks"
          element={
            <ProtectedRoute>
              <TasksPage />
            </ProtectedRoute>
          }
        />

        {/* Ruta raíz - Redirige a login */}
        <Route path="/" element={<Navigate to="/login" replace />} />

        {/* Ruta 404 - No encontrada */}
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </BrowserRouter>
  );
};

export default AppRouter;
