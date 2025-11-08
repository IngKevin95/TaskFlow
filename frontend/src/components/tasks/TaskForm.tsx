/**
 * TaskForm Component
 * Formulario para crear/editar tareas
 */

import React, { FC, useState, useEffect } from 'react';
import { Task } from '../../types/task.types';
import '../styles/TaskForm.css';

interface TaskFormProps {
  projectId: number;
  task?: Task;
  onSubmit: (data: {
    title: string;
    description: string;
    priority: string;
    status: string;
    dueDate?: string;
  }) => Promise<void>;
  onCancel: () => void;
  isLoading?: boolean;
}

const TaskForm: FC<TaskFormProps> = ({ projectId, task, onSubmit, onCancel, isLoading = false }) => {
  const [formData, setFormData] = useState({
    title: task?.title || '',
    description: task?.description || '',
    priority: task?.priority || 'medium',
    status: task?.status || 'pending',
    dueDate: task?.dueDate || '',
  });
  const [error, setError] = useState('');

  useEffect(() => {
    if (task) {
      setFormData({
        title: task.title,
        description: task.description,
        priority: task.priority,
        status: task.status,
        dueDate: task.dueDate || '',
      });
    }
  }, [task]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
    setError('');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!formData.title.trim()) {
      setError('El título es requerido');
      return;
    }

    if (!formData.description.trim()) {
      setError('La descripción es requerida');
      return;
    }

    try {
      await onSubmit(formData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error al guardar la tarea');
    }
  };

  return (
    <form className="task-form" onSubmit={handleSubmit}>
      <div className="form-group">
        <label htmlFor="title">Título *</label>
        <input
          id="title"
          type="text"
          name="title"
          value={formData.title}
          onChange={handleChange}
          placeholder="Nombre de la tarea"
          maxLength={100}
          disabled={isLoading}
          className="form-input"
        />
        <span className="char-count">{formData.title.length}/100</span>
      </div>

      <div className="form-group">
        <label htmlFor="description">Descripción *</label>
        <textarea
          id="description"
          name="description"
          value={formData.description}
          onChange={handleChange}
          placeholder="Descripción detallada de la tarea"
          maxLength={500}
          rows={4}
          disabled={isLoading}
          className="form-textarea"
        />
        <span className="char-count">{formData.description.length}/500</span>
      </div>

      <div className="form-row">
        <div className="form-group">
          <label htmlFor="priority">Prioridad</label>
          <select
            id="priority"
            name="priority"
            value={formData.priority}
            onChange={handleChange}
            disabled={isLoading}
            className="form-select"
          >
            <option value="low">Baja</option>
            <option value="medium">Media</option>
            <option value="high">Alta</option>
            <option value="critical">Crítica</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="status">Estado</label>
          <select
            id="status"
            name="status"
            value={formData.status}
            onChange={handleChange}
            disabled={isLoading}
            className="form-select"
          >
            <option value="pending">Pendiente</option>
            <option value="in_progress">En Progreso</option>
            <option value="review">En Revisión</option>
            <option value="completed">Completado</option>
          </select>
        </div>
      </div>

      <div className="form-group">
        <label htmlFor="dueDate">Fecha de Vencimiento</label>
        <input
          id="dueDate"
          type="date"
          name="dueDate"
          value={formData.dueDate}
          onChange={handleChange}
          disabled={isLoading}
          className="form-input"
        />
      </div>

      {error && <div className="form-error">{error}</div>}

      <div className="form-actions">
        <button type="button" onClick={onCancel} disabled={isLoading} className="btn btn-secondary">
          Cancelar
        </button>
        <button type="submit" disabled={isLoading} className="btn btn-primary">
          {isLoading ? 'Guardando...' : task ? 'Actualizar Tarea' : 'Crear Tarea'}
        </button>
      </div>
    </form>
  );
};

export default TaskForm;
