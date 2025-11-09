// Hook para gestión de proyectos

import { useState, useEffect } from "react";
import { Project, ProjectWithDetails, ProjectCreateRequest, ProjectUpdateRequest } from "../types";
import projectsAPI from "../api/projects.api";

export const useProject = (projectId?: number) => {
  const [project, setProject] = useState<ProjectWithDetails | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (projectId) {
      fetchProject(projectId);
    }
  }, [projectId]);

  const fetchProject = async (id: number) => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await projectsAPI.getById(id);
      setProject(data);
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || "Error al obtener proyecto";
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return {
    project,
    isLoading,
    error,
    fetchProject,
  };
};

export const useProjects = () => {
  const [projects, setProjects] = useState<Project[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [total, setTotal] = useState(0);

  const fetchProjects = async (skip = 0, limit = 10) => {
    setIsLoading(true);
    setError(null);
    try {
      const data: any = await projectsAPI.getAll(skip, limit);
      console.log("📊 Datos de proyectos recibidos:", data);
      console.log("📊 Tipo de datos:", typeof data);
      console.log("📊 Es array?:", Array.isArray(data));
      
      // Si es un objeto con propiedad 'data', extraer eso
      const projectsArray = Array.isArray(data) ? data : (data?.data || []);
      console.log("📊 Array final a guardar:", projectsArray);
      
      setProjects(projectsArray);
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || "Error al obtener proyectos";
      setError(errorMessage);
      console.error("❌ Error al obtener proyectos:", err);
    } finally {
      setIsLoading(false);
    }
  };

  const createProject = async (data: ProjectCreateRequest) => {
    setIsLoading(true);
    setError(null);
    try {
      const newProject = await projectsAPI.create(data);
      setProjects([...projects, newProject]);
      return newProject;
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || "Error al crear proyecto";
      setError(errorMessage);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const updateProject = async (id: number, data: ProjectUpdateRequest) => {
    setIsLoading(true);
    setError(null);
    try {
      const updated = await projectsAPI.update(id, data);
      setProjects(projects.map(p => p.id === id ? updated : p));
      return updated;
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || "Error al actualizar proyecto";
      setError(errorMessage);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const deleteProject = async (id: number) => {
    setIsLoading(true);
    setError(null);
    try {
      await projectsAPI.delete(id);
      setProjects(projects.filter(p => p.id !== id));
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || "Error al eliminar proyecto";
      setError(errorMessage);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  return {
    projects,
    isLoading,
    error,
    total,
    fetchProjects,
    createProject,
    updateProject,
    deleteProject,
  };
};
