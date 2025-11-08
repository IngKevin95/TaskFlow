/**
 * TaskBoard Component
 * Tablero Kanban con vista de tareas por estado (para mostrar en detalles de proyecto)
 */

import React, { FC, useEffect, useState } from 'react';
import { Task } from '../../types/task.types';
import TaskCard from './TaskCard';
import '../styles/TaskBoard.css';

interface TaskBoardProps {
  projectId: number;
  tasks: Task[];
  isLoading?: boolean;
  onTaskStatusChange?: (taskId: number, newStatus: string) => Promise<void>;
  onTaskDelete?: (taskId: number) => Promise<void>;
  onTaskSelect?: (task: Task) => void;
}

const TaskBoard: FC<TaskBoardProps> = ({
  projectId,
  tasks,
  isLoading = false,
  onTaskStatusChange,
  onTaskDelete,
  onTaskSelect,
}) => {
  const statuses = ['pending', 'in_progress', 'review', 'completed'];
  const statusLabels: Record<string, string> = {
    pending: 'Pendiente',
    in_progress: 'En Progreso',
    review: 'En Revisión',
    completed: 'Completado',
  };

  const getTasksByStatus = (status: string) => {
    return tasks.filter(task => task.status === status);
  };

  const handleStatusChange = async (taskId: number, newStatus: string) => {
    if (onTaskStatusChange) {
      try {
        await onTaskStatusChange(taskId, newStatus);
      } catch (error) {
        console.error('Error al cambiar estado:', error);
      }
    }
  };

  const handleDeleteTask = async (taskId: number) => {
    if (onTaskDelete) {
      if (confirm('¿Estás seguro de que deseas eliminar esta tarea?')) {
        try {
          await onTaskDelete(taskId);
        } catch (error) {
          console.error('Error al eliminar tarea:', error);
        }
      }
    }
  };

  return (
    <div className="task-board">
      {isLoading ? (
        <div className="board-loading">
          <div className="spinner"></div>
          <p>Cargando tareas...</p>
        </div>
      ) : (
        <div className="board-container">
          {statuses.map(status => {
            const statusTasks = getTasksByStatus(status);
            return (
              <div key={status} className={`board-column status-${status}`}>
                <div className="column-header">
                  <h3>{statusLabels[status]}</h3>
                  <span className="task-count">{statusTasks.length}</span>
                </div>

                <div className="tasks-container">
                  {statusTasks.length === 0 ? (
                    <div className="empty-column-message">
                      <p>Sin tareas</p>
                    </div>
                  ) : (
                    statusTasks.map(task => (
                      <TaskCard
                        key={task.id}
                        task={task}
                        onStatusChange={(newStatus) => handleStatusChange(task.id, newStatus)}
                        onDelete={() => handleDeleteTask(task.id)}
                      />
                    ))
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}

      {tasks.length > 0 && (
        <div className="board-stats">
          <div className="stat-item">
            <span className="stat-label">Total:</span>
            <span className="stat-value">{tasks.length}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Completadas:</span>
            <span className="stat-value">{getTasksByStatus('completed').length}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">En Progreso:</span>
            <span className="stat-value">{getTasksByStatus('in_progress').length}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">En Revisión:</span>
            <span className="stat-value">{getTasksByStatus('review').length}</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default TaskBoard;
