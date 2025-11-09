/**
 * ProtectedRoute Component
 * Componente que protege rutas que requieren autenticación
 */

import React, { FC, ReactNode } from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

interface ProtectedRouteProps {
  children: ReactNode;
  redirectTo?: string;
}

/**
 * ProtectedRoute - Protege rutas que requieren autenticación
 * 
 * Si el usuario no está autenticado, redirige a la página de login
 * Si el usuario está autenticado, muestra el contenido
 * 
 * @param children - El contenido a mostrar si el usuario está autenticado
 * @param redirectTo - Página a redirigir si no está autenticado (default: /login)
 * 
 * @example
 * ```
 * <Route element={
 *   <ProtectedRoute>
 *     <ProjectsPage />
 *   </ProtectedRoute>
 * } path="/projects" />
 * ```
 */
const ProtectedRoute: FC<ProtectedRouteProps> = ({
  children,
  redirectTo = '/login'
}) => {
  const { isAuthenticated, isLoading } = useAuth();

  console.log('ProtectedRoute - Estado:', { isAuthenticated, isLoading });

  // Mientras se carga la información de autenticación
  if (isLoading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p>Cargando...</p>
      </div>
    );
  }

  // Si no está autenticado, redirigir
  if (!isAuthenticated) {
    console.log('No autenticado, redirigiendo a:', redirectTo);
    return <Navigate to={redirectTo} replace />;
  }

  // Si está autenticado, mostrar contenido
  console.log('Autenticado, mostrando contenido protegido');
  return <>{children}</>;
};

export default ProtectedRoute;
