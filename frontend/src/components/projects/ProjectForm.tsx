/**
 * ProjectForm Component
 * Formulario para crear/editar proyectos
 */

import React, { FC, useState } from 'react';
import '../styles/ProjectForm.css';

interface ProjectFormProps {
  onSubmit: (name: string, description: string) => Promise<void>;
  onCancel: () => void;
  initialName?: string;
  initialDescription?: string;
}

const ProjectForm: FC<ProjectFormProps> = ({
  onSubmit,
  onCancel,
  initialName = '',
  initialDescription = '',
}) => {
  const [name, setName] = useState(initialName);
  const [description, setDescription] = useState(initialDescription);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!name.trim()) {
      newErrors.name = 'El nombre es requerido';
    } else if (name.length < 3) {
      newErrors.name = 'El nombre debe tener al menos 3 caracteres';
    } else if (name.length > 100) {
      newErrors.name = 'El nombre no puede exceder 100 caracteres';
    }

    if (description.length > 500) {
      newErrors.description = 'La descripción no puede exceder 500 caracteres';
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
      await onSubmit(name, description);
      setName('');
      setDescription('');
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
          <label htmlFor="name">Nombre del Proyecto *</label>
          <input
            id="name"
            type="text"
            value={name}
            onChange={(e) => {
              setName(e.target.value);
              if (errors.name) setErrors({ ...errors, name: '' });
            }}
            placeholder="Mi Proyecto"
            className={`form-input ${errors.name ? 'input-error' : ''}`}
            disabled={isSubmitting}
          />
          {errors.name && <span className="form-error-text">{errors.name}</span>}
        </div>

        <div className="form-group">
          <label htmlFor="description">Descripción</label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => {
              setDescription(e.target.value);
              if (errors.description) setErrors({ ...errors, description: '' });
            }}
            placeholder="Descripción del proyecto..."
            className={`form-textarea ${errors.description ? 'input-error' : ''}`}
            rows={4}
            disabled={isSubmitting}
          />
          <div className="char-count">
            {description.length}/500 caracteres
          </div>
          {errors.description && (
            <span className="form-error-text">{errors.description}</span>
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
