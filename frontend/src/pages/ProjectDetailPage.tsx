/**
 * ProjectDetailPage Component
 * Página con detalles del proyecto
 */

import React, { FC, useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useProjects } from '@/hooks/useProject';
import { useTasks } from '@/hooks/useTask';
import CreateTaskModal from '../components/tasks/CreateTaskModal';
import './styles/ProjectDetail.css';

const ProjectDetailPage: FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const projectId = parseInt(id || '0');

  const { projects, isLoading: projectLoading, error: projectError, fetchProjects } = useProjects();
  const { 
    tasks, 
    isLoading: tasksLoading, 
    error: tasksError, 
    fetchProjectTasks, 
    createTask, 
    deleteTask, 
    updateStatus 
  } = useTasks();

  const [activeTab, setActiveTab] = useState<'tasks' | 'members'>('tasks');
  const [showCreateTaskModal, setShowCreateTaskModal] = useState(false);
  const project = projects.find((p: any) => p.id === projectId);

  useEffect(() => {
    const loadProjects = async () => {
      await fetchProjects(0, 50);
    };
    loadProjects();
  }, []);

  useEffect(() => {
    if (projectId) {
      fetchProjectTasks(projectId);
    }
  }, [projectId]);

  if (projectLoading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
        <p>Cargando...</p>
      </div>
    );
  }

  if (!project) {
    return (
      <div className="error-container">
        <p>Proyecto no encontrado</p>
        <button onClick={() => navigate('/projects')} className="btn btn-primary">
          Volver a Proyectos
        </button>
      </div>
    );
  }

  const tasksByStatus = {
    pending: tasks.filter(t => t.status === 'pending'),
    in_progress: tasks.filter(t => t.status === 'in_progress'),
    review: tasks.filter(t => t.status === 'review'),
    completed: tasks.filter(t => t.status === 'completed'),
  };

  return (
    <div className="project-detail-page">
      <div className="detail-header">
        <button onClick={() => navigate('/projects')} className="btn-back">
          ← Volver
        </button>
        <h1>{project.name}</h1>
        <p className="detail-description">{project.description}</p>
      </div>

      <div className="detail-tabs">
        <button
          className={`tab ${activeTab === 'tasks' ? 'active' : ''}`}
          onClick={() => setActiveTab('tasks')}
        >
          Tareas ({tasks.length})
        </button>
        <button
          className={`tab ${activeTab === 'members' ? 'active' : ''}`}
          onClick={() => setActiveTab('members')}
        >
          Miembros ({project.members?.length || 1})
        </button>
      </div>

      {activeTab === 'tasks' && (
        <div className="tasks-section">
          <div className="tasks-header">
            <h2>Tareas del Proyecto</h2>
            <button 
              onClick={() => setShowCreateTaskModal(true)} 
              className="btn btn-primary btn-create-task"
            >
              + Nueva Tarea
            </button>
          </div>
          {tasksLoading ? (
            <div className="loading">Cargando tareas...</div>
          ) : (
            <div className="tasks-board">
              {['pending', 'in_progress', 'review', 'completed'].map(status => (
                <div key={status} className={`task-column status-${status}`}>
                  <h3 className="column-title">{status.replace('_', ' ').toUpperCase()}</h3>
                  <div className="task-list">
                    {tasksByStatus[status as keyof typeof tasksByStatus]?.map(task => (
                      <div key={task.id} className="task-item">
                        <h4>{task.title}</h4>
                        <p>{task.description}</p>
                        <div className="task-footer">
                          <span className={`priority priority-${task.priority}`}>
                            {task.priority}
                          </span>
                          <button
                            className="btn-delete"
                            onClick={() => deleteTask(task.id)}
                          >
                            ✕
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {activeTab === 'members' && (
        <div className="members-section">
          <h3>Miembros del Proyecto</h3>
          <div className="members-list">
            {project.members && project.members.length > 0 ? (
              project.members.map(member => (
                <div key={member.id} className="member-item">
                  <div className="member-info">
                    <h4>{member.username}</h4>
                    <p>{member.email}</p>
                  </div>
                </div>
              ))
            ) : (
              <p>Sin miembros adicionales</p>
            )}
          </div>
        </div>
      )}

      <CreateTaskModal
        isOpen={showCreateTaskModal}
        onClose={() => setShowCreateTaskModal(false)}
        onSubmit={async (data) => {
          await createTask(projectId, {
            title: data.title,
            description: data.description,
            priority: data.priority,
          });
          await fetchProjectTasks(projectId);
        }}
        projects={projects}
        defaultProjectId={projectId}
      />
    </div>
  );
};

export default ProjectDetailPage;
