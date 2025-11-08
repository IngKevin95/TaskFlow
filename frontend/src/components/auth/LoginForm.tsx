/**
 * LoginForm Component
 * Formulario para iniciar sesión con email y contraseña
 */

import React, { FC, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import '../styles/Form.css';

interface LoginFormProps {
  onSuccess?: () => void;
}

const LoginForm: FC<LoginFormProps> = ({ onSuccess }) => {
  const navigate = useNavigate();
  const { login, isLoading, error } = useAuth();
  
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });
  
  const [validationErrors, setValidationErrors] = useState<Record<string, string>>({});

  // Validación básica del formulario
  const validateForm = (): boolean => {
    const errors: Record<string, string> = {};
    
    if (!formData.username.trim()) {
      errors.username = 'El nombre de usuario es requerido';
    }
    
    if (!formData.password) {
      errors.password = 'La contraseña es requerida';
    } else if (formData.password.length < 6) {
      errors.password = 'La contraseña debe tener al menos 6 caracteres';
    }
    
    setValidationErrors(errors);
    return Object.keys(errors).length === 0;
  };

  // Manejar cambios en los inputs
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Limpiar error del campo cuando el usuario comienza a escribir
    if (validationErrors[name]) {
      setValidationErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  // Manejar envío del formulario
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    
    // Validar formulario
    if (!validateForm()) {
      return;
    }
    
    try {
      await login(formData.username, formData.password);
      
      // Limpiar formulario
      setFormData({ username: '', password: '' });
      
      // Callback de éxito
      if (onSuccess) {
        onSuccess();
      } else {
        // Redirigir a dashboard si no hay callback
        navigate('/projects');
      }
    } catch (err) {
      // El error se maneja en el hook useAuth y se mostrará en la UI
      console.error('Error al iniciar sesión:', err);
    }
  };

  return (
    <div className="form-container">
      <h2>Iniciar Sesión</h2>
      
      {/* Mostrar errores del servidor */}
      {error && (
        <div className="form-error alert alert-danger">
          <span className="alert-icon">⚠️</span>
          {error}
        </div>
      )}
      
      <form onSubmit={handleSubmit} className="auth-form" noValidate>
        {/* Campo Usuario */}
        <div className="form-group">
          <label htmlFor="username">Nombre de usuario</label>
          <input
            id="username"
            type="text"
            name="username"
            value={formData.username}
            onChange={handleInputChange}
            placeholder="Tu nombre de usuario"
            className={`form-input ${validationErrors.username ? 'input-error' : ''}`}
            disabled={isLoading}
            autoComplete="username"
            required
          />
          {validationErrors.username && (
            <span className="form-error-text">{validationErrors.username}</span>
          )}
        </div>

        {/* Campo Contraseña */}
        <div className="form-group">
          <label htmlFor="password">Contraseña</label>
          <input
            id="password"
            type="password"
            name="password"
            value={formData.password}
            onChange={handleInputChange}
            placeholder="Tu contraseña"
            className={`form-input ${validationErrors.password ? 'input-error' : ''}`}
            disabled={isLoading}
            autoComplete="current-password"
            required
          />
          {validationErrors.password && (
            <span className="form-error-text">{validationErrors.password}</span>
          )}
        </div>

        {/* Botón Enviar */}
        <button
          type="submit"
          className="btn btn-primary btn-submit"
          disabled={isLoading}
        >
          {isLoading ? (
            <>
              <span className="spinner"></span>
              Iniciando sesión...
            </>
          ) : (
            'Iniciar Sesión'
          )}
        </button>
      </form>

      {/* Link a registro */}
      <div className="form-footer">
        <p>
          ¿No tienes cuenta?{' '}
          <a href="/register" className="link">
            Regístrate aquí
          </a>
        </p>
      </div>
    </div>
  );
};

export default LoginForm;
