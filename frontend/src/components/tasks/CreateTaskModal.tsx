/**
 * CreateTaskModal Component
 * Modal reutilizable para crear tareas
 */

import React, { FC, useState, useEffect } from 'react';
import { Project } from '../../types';
import '../styles/CreateTaskModal.css';

interface CreateTaskModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (data: {
    title: string;
    description: string;
    priority: string;
    projectId: number;
  }) => Promise<void>;
  projects: Project[];
  defaultProjectId?: number;
  isLoading?: boolean;
}

type FilterPriority = 'low' | 'medium' | 'high' | 'critical';

const CreateTaskModal: FC<CreateTaskModalProps> = ({
  isOpen,
  onClose,
  onSubmit,
  projects,
  defaultProjectId,
  isLoading = false,
}) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    priority: 'medium' as FilterPriority,
    projectId: defaultProjectId || 0,
  });
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    // Actualizar el ID del proyecto cuando cambia defaultProjectId
    console.log("🎯 CreateTaskModal - projects recibidos:", projects);
    console.log("🎯 CreateTaskModal - defaultProjectId:", defaultProjectId);
    console.log("🎯 CreateTaskModal - projects.length:", projects.length);
    
    if (defaultProjectId) {
      setFormData(prev => ({ ...prev, projectId: defaultProjectId }));
    } else if (projects.length > 0 && formData.projectId === 0) {
      // Si no hay defaultProjectId pero hay proyectos, seleccionar el primero
      setFormData(prev => ({ ...prev, projectId: projects[0].id }));
    }
  }, [defaultProjectId, projects]);

  const handleSubmit = async () => {
    if (!formData.title.trim()) {
      alert('El título es requerido');
      return;
    }
    if (formData.projectId === 0) {
      alert('Debes seleccionar un proyecto');
      return;
    }

    setIsSubmitting(true);
    try {
      await onSubmit(formData);
      setFormData({
        title: '',
        description: '',
        priority: 'medium' as FilterPriority,
        projectId: defaultProjectId || (projects.length > 0 ? projects[0].id : 0),
      });
    } catch (err) {
      console.error('Error creating task:', err);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Crear Nueva Tarea</h2>
          <button className="modal-close" onClick={onClose} disabled={isSubmitting}>
            ✕
          </button>
        </div>
        <div className="modal-body">
          <div className="form-group">
            <label htmlFor="title">Título *</label>
            <input
              id="title"
              type="text"
              placeholder="Título de la tarea"
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              className="form-input"
              disabled={isSubmitting}
            />
          </div>
          <div className="form-group">
            <label htmlFor="description">Descripción</label>
            <textarea
              id="description"
              placeholder="Descripción de la tarea"
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              className="form-textarea"
              rows={4}
              disabled={isSubmitting}
            />
          </div>
          <div className="form-group">
            <label htmlFor="project">Proyecto *</label>
            <select
              id="project"
              value={formData.projectId}
              onChange={(e) => setFormData({ ...formData, projectId: Number(e.target.value) })}
              className="form-select"
              disabled={isSubmitting || projects.length === 0}
            >
              {projects.length === 0 ? (
                <option value={0}>No hay proyectos disponibles</option>
              ) : (
                <>
                  <option value={0}>Seleccionar proyecto...</option>
                  {projects.map((project: any) => (
                    <option key={project.id} value={project.id}>
                      {project.nombre}
                    </option>
                  ))}
                </>
              )}
            </select>
          </div>
          <div className="form-group">
            <label htmlFor="priority">Prioridad</label>
            <select
              id="priority"
              value={formData.priority}
              onChange={(e) => setFormData({ ...formData, priority: e.target.value as FilterPriority })}
              className="form-select"
              disabled={isSubmitting}
            >
              <option value="low">Baja</option>
              <option value="medium">Media</option>
              <option value="high">Alta</option>
              <option value="critical">Crítica</option>
            </select>
          </div>
        </div>
        <div className="modal-footer">
          <button 
            onClick={onClose} 
            className="btn btn-secondary" 
            disabled={isSubmitting}
          >
            Cancelar
          </button>
          <button 
            onClick={handleSubmit} 
            className="btn btn-primary" 
            disabled={isSubmitting || isLoading}
          >
            {isSubmitting ? 'Creando...' : 'Crear Tarea'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default CreateTaskModal;
