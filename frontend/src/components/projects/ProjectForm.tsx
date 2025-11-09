/**
 * ProjectForm Component
 * Formulario para crear/editar proyectos
 */

import React, { FC, useState } from 'react';
import '../styles/ProjectForm.css';

interface ProjectFormProps {
  onSubmit: (nombre: string, descripcion: string) => Promise<void>;
  onCancel: () => void;
  initialNombre?: string;
  initialDescripcion?: string;
}

const ProjectForm: FC<ProjectFormProps> = ({
  onSubmit,
  onCancel,
  initialNombre = '',
  initialDescripcion = '',
}) => {
  const [nombre, setNombre] = useState(initialNombre);
  const [descripcion, setDescripcion] = useState(initialDescripcion);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!nombre.trim()) {
      newErrors.nombre = 'El nombre es requerido';
    } else if (nombre.length < 3) {
      newErrors.nombre = 'El nombre debe tener al menos 3 caracteres';
    } else if (nombre.length > 100) {
      newErrors.nombre = 'El nombre no puede exceder 100 caracteres';
    }

    if (descripcion.length > 500) {
      newErrors.descripcion = 'La descripción no puede exceder 500 caracteres';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    try {
      setIsSubmitting(true);
      await onSubmit(nombre, descripcion);
      setNombre('');
      setDescripcion('');
    } catch (err) {
      console.error('Error:', err);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="project-form-container">
      <form onSubmit={handleSubmit} className="project-form">
        <div className="form-group">
          <label htmlFor="nombre">Nombre del Proyecto *</label>
          <input
            id="nombre"
            type="text"
            value={nombre}
            onChange={(e) => {
              setNombre(e.target.value);
              if (errors.nombre) setErrors({ ...errors, nombre: '' });
            }}
            placeholder="Mi Proyecto"
            className={`form-input ${errors.nombre ? 'input-error' : ''}`}
            disabled={isSubmitting}
          />
          {errors.nombre && <span className="form-error-text">{errors.nombre}</span>}
        </div>

        <div className="form-group">
          <label htmlFor="descripcion">Descripción</label>
          <textarea
            id="descripcion"
            value={descripcion}
            onChange={(e) => {
              setDescripcion(e.target.value);
              if (errors.descripcion) setErrors({ ...errors, descripcion: '' });
            }}
            placeholder="Descripción del proyecto..."
            className={`form-textarea ${errors.descripcion ? 'input-error' : ''}`}
            rows={4}
            disabled={isSubmitting}
          />
          <div className="char-count">
            {descripcion.length}/500 caracteres
          </div>
          {errors.descripcion && (
            <span className="form-error-text">{errors.descripcion}</span>
          )}
        </div>

        <div className="form-actions">
          <button
            type="button"
            className="btn btn-secondary"
            onClick={onCancel}
            disabled={isSubmitting}
          >
            Cancelar
          </button>
          <button
            type="submit"
            className="btn btn-primary"
            disabled={isSubmitting}
          >
            {isSubmitting ? 'Guardando...' : 'Crear Proyecto'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default ProjectForm;
