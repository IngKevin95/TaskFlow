/**
 * ProjectCard Component
 * Card individual para mostrar proyecto en lista
 */

import React, { FC } from 'react';
import { Project } from '../../types/project.types';
import '../styles/ProjectCard.css';

interface ProjectCardProps {
  project: Project;
  onView: () => void;
  onDelete: () => void;
}

const ProjectCard: FC<ProjectCardProps> = ({ project, onView, onDelete }) => {
  return (
    <div className="project-card">
      <div className="project-card-header">
        <h3 className="project-name">{project.name}</h3>
        <button className="btn-menu" onClick={(e) => e.stopPropagation()}>
          ⋯
        </button>
      </div>

      <p className="project-description">{project.description || 'Sin descripción'}</p>

      <div className="project-card-footer">
        <div className="project-meta">
          <span className="meta-item">
            📅 {new Date(project.created_at).toLocaleDateString()}
          </span>
        </div>
        <div className="project-actions">
          <button className="btn btn-small btn-primary" onClick={onView}>
            Ver
          </button>
          <button className="btn btn-small btn-danger" onClick={onDelete}>
            Eliminar
          </button>
        </div>
      </div>
    </div>
  );
};

export default ProjectCard;
