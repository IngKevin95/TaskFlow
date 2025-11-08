/**
 * TaskCard Component
 * Tarjeta individual de tarea con opciones de estado y eliminación
 */

import React, { FC } from 'react';
import { Task } from '../../types/task.types';
import '../styles/TaskCard.css';

interface TaskCardProps {
  task: Task;
  onStatusChange?: (status: string) => void;
  onDelete?: () => void;
}

const getPriorityColor = (priority: string): string => {
  const colors: Record<string, string> = {
    low: '#4CAF50',
    medium: '#FFC107',
    high: '#FF9800',
    critical: '#F44336',
  };
  return colors[priority] || '#999';
};

const getStatusLabel = (status: string): string => {
  const labels: Record<string, string> = {
    pending: 'Pendiente',
    in_progress: 'En Progreso',
    review: 'En Revisión',
    completed: 'Completado',
  };
  return labels[status] || status;
};

const TaskCard: FC<TaskCardProps> = ({ task, onStatusChange, onDelete }) => {
  const handleStatusChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    if (onStatusChange) {
      onStatusChange(e.target.value);
    }
  };

  return (
    <div className={`task-card priority-${task.priority}`}>
      <div className="task-header">
        <div className="task-meta">
          <span
            className="priority-dot"
            style={{ backgroundColor: getPriorityColor(task.priority) }}
            title={task.priority}
          ></span>
          <span className="task-priority">{task.priority.charAt(0).toUpperCase() + task.priority.slice(1)}</span>
        </div>
        <button
          className="task-delete-btn"
          onClick={onDelete}
          title="Eliminar tarea"
        >
          ✕
        </button>
      </div>

      <h4 className="task-title">{task.title}</h4>
      <p className="task-description">{task.description}</p>

      <div className="task-footer">
        <select
          value={task.status}
          onChange={handleStatusChange}
          className={`status-select status-${task.status}`}
        >
          <option value="pending">Pendiente</option>
          <option value="in_progress">En Progreso</option>
          <option value="review">En Revisión</option>
          <option value="completed">Completado</option>
        </select>

        {task.dueDate && (
          <span className="task-due-date">
            {new Date(task.dueDate).toLocaleDateString('es-ES', {
              month: 'short',
              day: 'numeric',
            })}
          </span>
        )}
      </div>

      {task.assignedToName && (
        <div className="task-assignee">
          Asignado a: <strong>{task.assignedToName}</strong>
        </div>
      )}
    </div>
  );
};

export default TaskCard;
