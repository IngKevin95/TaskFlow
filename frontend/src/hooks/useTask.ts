// Hook para gestión de tareas

import { useState } from "react";
import { Task, TaskCreateRequest, TaskUpdateRequest } from "../types";
import type { TaskStatus } from "../types/auth.types";
import tasksAPI from "../api/tasks.api";

export const useTasks = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [myTasks, setMyTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchProjectTasks = async (projectId: number, skip = 0, limit = 50) => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await tasksAPI.getProjectTasks(projectId, skip, limit);
      setTasks(data);
      return data;
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || "Error al obtener tareas";
      setError(errorMessage);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const fetchMyTasks = async (skip = 0, limit = 50) => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await tasksAPI.getMyTasks(skip, limit);
      console.log("📋 Mis tareas obtenidas:", data);
      setMyTasks(data);
      return data;
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || "Error al obtener tus tareas";
      console.error("❌ Error al obtener tareas:", err);
      setError(errorMessage);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const createTask = async (projectId: number, data: TaskCreateRequest) => {
    setIsLoading(true);
    setError(null);
    try {
      const newTask = await tasksAPI.create(projectId, data);
      console.log("✅ Tarea creada:", newTask);
      setTasks([...tasks, newTask]);
      // También agregar a myTasks si es del usuario actual
      setMyTasks([...myTasks, newTask]);
      return newTask;
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || "Error al crear tarea";
      console.error("❌ Error al crear tarea:", err);
      setError(errorMessage);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const updateTask = async (id: number, data: TaskUpdateRequest) => {
    setIsLoading(true);
    setError(null);
    try {
      const updated = await tasksAPI.update(id, data);
      setTasks(tasks.map((t: Task) => t.id === id ? updated : t));
      return updated;
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || "Error al actualizar tarea";
      setError(errorMessage);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const deleteTask = async (id: number) => {
    setIsLoading(true);
    setError(null);
    try {
      await tasksAPI.delete(id);
      setTasks(tasks.filter((t: Task) => t.id !== id));
      setMyTasks(myTasks.filter((t: Task) => t.id !== id));
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || "Error al eliminar tarea";
      setError(errorMessage);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const updateStatus = async (id: number, status: TaskStatus) => {
    setIsLoading(true);
    setError(null);
    try {
      const updated = await tasksAPI.update(id, { status });
      setTasks(tasks.map((t: Task) => t.id === id ? updated : t));
      setMyTasks(myTasks.map((t: Task) => t.id === id ? updated : t));
      return updated;
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || "Error al actualizar estado";
      setError(errorMessage);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  return {
    tasks,
    myTasks,
    isLoading,
    error,
    fetchProjectTasks,
    fetchMyTasks,
    createTask,
    updateTask,
    deleteTask,
    updateStatus,
  };
};
