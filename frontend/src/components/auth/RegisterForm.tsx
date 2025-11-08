/**
 * RegisterForm Component
 * Formulario para registrar nuevo usuario
 */

import React, { FC, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import '../styles/Form.css';

interface RegisterFormProps {
  onSuccess?: () => void;
}

const RegisterForm: FC<RegisterFormProps> = ({ onSuccess }) => {
  const navigate = useNavigate();
  const { register, isLoading, error } = useAuth();
  
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    firstName: '',
    lastName: '',
  });
  
  const [validationErrors, setValidationErrors] = useState<Record<string, string>>({});

  // Validar email
  const validateEmail = (email: string): boolean => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  // Validación del formulario
  const validateForm = (): boolean => {
    const errors: Record<string, string> = {};
    
    // Validar username
    if (!formData.username.trim()) {
      errors.username = 'El nombre de usuario es requerido';
    } else if (formData.username.length < 3) {
      errors.username = 'El nombre de usuario debe tener al menos 3 caracteres';
    }
    
    // Validar email
    if (!formData.email.trim()) {
      errors.email = 'El email es requerido';
    } else if (!validateEmail(formData.email)) {
      errors.email = 'El email no es válido';
    }
    
    // Validar contraseña
    if (!formData.password) {
      errors.password = 'La contraseña es requerida';
    } else if (formData.password.length < 6) {
      errors.password = 'La contraseña debe tener al menos 6 caracteres';
    }
    
    // Validar confirmación de contraseña
    if (!formData.confirmPassword) {
      errors.confirmPassword = 'Debes confirmar la contraseña';
    } else if (formData.password !== formData.confirmPassword) {
      errors.confirmPassword = 'Las contraseñas no coinciden';
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
    
    // Limpiar error del campo
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
      await register({
        username: formData.username,
        email: formData.email,
        password: formData.password,
        first_name: formData.firstName,
        last_name: formData.lastName,
      });
      
      // Limpiar formulario
      setFormData({
        username: '',
        email: '',
        password: '',
        confirmPassword: '',
        firstName: '',
        lastName: '',
      });
      
      // Callback de éxito
      if (onSuccess) {
        onSuccess();
      } else {
        // Redirigir a dashboard
        navigate('/projects');
      }
    } catch (err) {
      console.error('Error al registrar:', err);
    }
  };

  return (
    <div className="form-container">
      <h2>Crear Cuenta</h2>
      
      {/* Mostrar errores del servidor */}
      {error && (
        <div className="form-error alert alert-danger">
          <span className="alert-icon">⚠️</span>
          {error}
        </div>
      )}
      
      <form onSubmit={handleSubmit} className="auth-form" noValidate>
        {/* Fila: Usuario y Email */}
        <div className="form-row">
          <div className="form-group form-group-half">
            <label htmlFor="username">Nombre de usuario *</label>
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

          <div className="form-group form-group-half">
            <label htmlFor="email">Email *</label>
            <input
              id="email"
              type="email"
              name="email"
              value={formData.email}
              onChange={handleInputChange}
              placeholder="tu@email.com"
              className={`form-input ${validationErrors.email ? 'input-error' : ''}`}
              disabled={isLoading}
              autoComplete="email"
              required
            />
            {validationErrors.email && (
              <span className="form-error-text">{validationErrors.email}</span>
            )}
          </div>
        </div>

        {/* Fila: Nombre y Apellido */}
        <div className="form-row">
          <div className="form-group form-group-half">
            <label htmlFor="firstName">Nombre</label>
            <input
              id="firstName"
              type="text"
              name="firstName"
              value={formData.firstName}
              onChange={handleInputChange}
              placeholder="Tu nombre"
              className="form-input"
              disabled={isLoading}
              autoComplete="given-name"
            />
          </div>

          <div className="form-group form-group-half">
            <label htmlFor="lastName">Apellido</label>
            <input
              id="lastName"
              type="text"
              name="lastName"
              value={formData.lastName}
              onChange={handleInputChange}
              placeholder="Tu apellido"
              className="form-input"
              disabled={isLoading}
              autoComplete="family-name"
            />
          </div>
        </div>

        {/* Fila: Contraseña */}
        <div className="form-row">
          <div className="form-group form-group-half">
            <label htmlFor="password">Contraseña *</label>
            <input
              id="password"
              type="password"
              name="password"
              value={formData.password}
              onChange={handleInputChange}
              placeholder="Al menos 6 caracteres"
              className={`form-input ${validationErrors.password ? 'input-error' : ''}`}
              disabled={isLoading}
              autoComplete="new-password"
              required
            />
            {validationErrors.password && (
              <span className="form-error-text">{validationErrors.password}</span>
            )}
          </div>

          <div className="form-group form-group-half">
            <label htmlFor="confirmPassword">Confirmar Contraseña *</label>
            <input
              id="confirmPassword"
              type="password"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleInputChange}
              placeholder="Repite tu contraseña"
              className={`form-input ${validationErrors.confirmPassword ? 'input-error' : ''}`}
              disabled={isLoading}
              autoComplete="new-password"
              required
            />
            {validationErrors.confirmPassword && (
              <span className="form-error-text">{validationErrors.confirmPassword}</span>
            )}
          </div>
        </div>

        {/* Nota de campos requeridos */}
        <div className="form-note">
          <small>* Campos requeridos</small>
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
              Creando cuenta...
            </>
          ) : (
            'Crear Cuenta'
          )}
        </button>
      </form>

      {/* Link a login */}
      <div className="form-footer">
        <p>
          ¿Ya tienes cuenta?{' '}
          <a href="/login" className="link">
            Inicia sesión
          </a>
        </p>
      </div>
    </div>
  );
};

export default RegisterForm;
