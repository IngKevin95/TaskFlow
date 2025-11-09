/**
 * TasksPage Component
 * Página de gestión de tareas - Vista personal de tareas asignadas
 */

import React, { FC, useEffect, useState } from 'react';
import { useTasks } from '@/hooks/useTask';
import { useProjects } from '@/hooks/useProject';
import { useAuth } from '@/context/AuthContext';
import TaskCard from '../components/tasks/TaskCard';
import CreateTaskModal from '../components/tasks/CreateTaskModal';
import './styles/TasksPage.css';

type FilterStatus = 'all' | 'pending' | 'in_progress' | 'review' | 'completed';
type FilterPriority = 'all' | 'low' | 'medium' | 'high' | 'critical';

const TasksPage: FC = () => {
  const { user } = useAuth();
  const { myTasks, isLoading, error, fetchMyTasks, updateStatus, deleteTask, createTask } = useTasks();
  const { projects, fetchProjects } = useProjects();
  const [statusFilter, setStatusFilter] = useState<FilterStatus>('all');
  const [priorityFilter, setPriorityFilter] = useState<FilterPriority>('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    const loadData = async () => {
      await fetchMyTasks();
      await fetchProjects(0, 50);
    };
    loadData();
  }, []);

  const filteredTasks = myTasks.filter(task => {
    const matchStatus = statusFilter === 'all' || task.status === statusFilter;
    const matchPriority = priorityFilter === 'all' || task.priority === priorityFilter;
    const matchSearch =
      task.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      task.description.toLowerCase().includes(searchTerm.toLowerCase());

    return matchStatus && matchPriority && matchSearch;
  });

  const tasksByStatus = {
    pending: filteredTasks.filter(t => t.status === 'pending'),
    in_progress: filteredTasks.filter(t => t.status === 'in_progress'),
    review: filteredTasks.filter(t => t.status === 'review'),
    completed: filteredTasks.filter(t => t.status === 'completed'),
  };

  const handleStatusChange = async (taskId: number, newStatus: string) => {
    await updateStatus(taskId, newStatus as any);
  };

  const handleDeleteTask = async (taskId: number) => {
    if (confirm('¿Eliminar esta tarea?')) {
      await deleteTask(taskId);
      await fetchMyTasks();
    }
  };

  return (
    <div className="tasks-page">
      <div className="tasks-header">
        <h1>Mis Tareas</h1>
        <button onClick={() => setShowModal(true)} className="btn btn-primary btn-create-task">
          + Nueva Tarea
        </button>
      </div>

      <div className="tasks-controls">
        <div className="search-box">
          <input
            type="text"
            placeholder="Buscar tareas..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
        </div>

        <div className="filters">
          <div className="filter-group">
            <label>Estado:</label>
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value as FilterStatus)}
              className="filter-select"
            >
              <option value="all">Todos</option>
              <option value="pending">Pendiente</option>
              <option value="in_progress">En Progreso</option>
              <option value="review">En Revisión</option>
              <option value="completed">Completado</option>
            </select>
          </div>

          <div className="filter-group">
            <label>Prioridad:</label>
            <select
              value={priorityFilter}
              onChange={(e) => setPriorityFilter(e.target.value as FilterPriority)}
              className="filter-select"
            >
              <option value="all">Todas</option>
              <option value="low">Baja</option>
              <option value="medium">Media</option>
              <option value="high">Alta</option>
              <option value="critical">Crítica</option>
            </select>
          </div>
        </div>
      </div>

      {error && <div className="alert alert-danger">{error}</div>}

      {isLoading ? (
        <div className="loading">
          <div className="spinner"></div>
          <p>Cargando tareas...</p>
        </div>
      ) : (
        <div className="tasks-board">
          {['pending', 'in_progress', 'review', 'completed'].map(status => (
            <div key={status} className={`task-column status-${status}`}>
              <div className="column-header">
                <h3>{status.replace('_', ' ').toUpperCase()}</h3>
                <span className="count-badge">{tasksByStatus[status as keyof typeof tasksByStatus].length}</span>
              </div>
              <div className="task-list">
                {tasksByStatus[status as keyof typeof tasksByStatus].length === 0 ? (
                  <div className="empty-column">Sin tareas</div>
                ) : (
                  tasksByStatus[status as keyof typeof tasksByStatus].map(task => (
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
          ))}
        </div>
      )}

      <div className="tasks-stats">
        <div className="stat">
          <span className="stat-label">Total:</span>
          <span className="stat-value">{filteredTasks.length}</span>
        </div>
        <div className="stat">
          <span className="stat-label">Completado:</span>
          <span className="stat-value">{tasksByStatus.completed.length}</span>
        </div>
        <div className="stat">
          <span className="stat-label">En Progreso:</span>
          <span className="stat-value">{tasksByStatus.in_progress.length}</span>
        </div>
      </div>

      <CreateTaskModal
        isOpen={showModal}
        onClose={() => setShowModal(false)}
        onSubmit={async (data) => {
          await createTask(data.projectId, {
            title: data.title,
            description: data.description,
            priority: data.priority,
            assigned_to_id: user?.id,
          });
          await fetchMyTasks();
          setShowModal(false);
        }}
        projects={projects}
      />
    </div>
  );
};

export default TasksPage;
