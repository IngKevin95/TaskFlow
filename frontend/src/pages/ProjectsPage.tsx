/**
 * ProjectsPage Component
 * Página principal de gestión de proyectos
 */

import React, { FC, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useProjects } from '@/hooks/useProject';
import ProjectCard from '../components/projects/ProjectCard';
import ProjectForm from '../components/projects/ProjectForm';
import './styles/ProjectsPage.css';

const ProjectsPage: FC = () => {
  const navigate = useNavigate();
  const { projects, isLoading, error, fetchProjects, createProject, deleteProject } = useProjects();
  const [showForm, setShowForm] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchProjects();
  }, []);

  const filteredProjects = projects.filter(project =>
    project.nombre.toLowerCase().includes(searchTerm.toLowerCase()) ||
    (project.descripcion && project.descripcion.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  const handleCreateProject = async (nombre: string, descripcion: string) => {
    await createProject({ nombre, descripcion });
    setShowForm(false);
  };

  const handleDeleteProject = async (projectId: number) => {
    if (confirm('¿Estás seguro de que deseas eliminar este proyecto?')) {
      await deleteProject(projectId);
    }
  };

  const handleProjectClick = (projectId: number) => {
    navigate(`/projects/${projectId}`);
  };

  return (
    <div className="projects-page">
      <div className="projects-header">
        <h1>Mis Proyectos</h1>
        <button
          className="btn btn-primary"
          onClick={() => setShowForm(!showForm)}
        >
          {showForm ? '✕ Cancelar' : '+ Nuevo Proyecto'}
        </button>
      </div>

      {showForm && (
        <ProjectForm onSubmit={handleCreateProject} onCancel={() => setShowForm(false)} />
      )}

      <div className="projects-search">
        <input
          type="text"
          placeholder="Buscar proyectos..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="search-input"
        />
      </div>

      {error && (
        <div className="alert alert-danger">
          {error}
        </div>
      )}

      {isLoading ? (
        <div className="loading">
          <div className="spinner"></div>
          <p>Cargando proyectos...</p>
        </div>
      ) : filteredProjects.length === 0 ? (
        <div className="empty-state">
          <p>No hay proyectos creados</p>
          <button
            className="btn btn-primary"
            onClick={() => setShowForm(true)}
          >
            Crear primer proyecto
          </button>
        </div>
      ) : (
        <div className="projects-grid">
          {filteredProjects.map(project => (
            <ProjectCard
              key={project.id}
              project={project}
              onView={() => handleProjectClick(project.id)}
              onDelete={() => handleDeleteProject(project.id)}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default ProjectsPage;
