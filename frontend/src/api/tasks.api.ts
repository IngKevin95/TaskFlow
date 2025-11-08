// Servicio de API para tareas

import axiosInstance from "./axiosInstance";
import { ENDPOINTS } from "../config/api.config";
import { Task, TaskWithAssignee, TaskCreateRequest, TaskUpdateRequest } from "../types";

class TasksAPI {
  async getProjectTasks(projectId: number, skip = 0, limit = 50): Promise<Task[]> {
    const response = await axiosInstance.get(ENDPOINTS.PROJECTS.TASKS(projectId), {
      params: { skip, limit },
    });
    return response.data;
  }

  async getById(id: number): Promise<TaskWithAssignee> {
    const response = await axiosInstance.get(ENDPOINTS.TASKS.DETAIL(id));
    return response.data;
  }

  async create(projectId: number, data: TaskCreateRequest): Promise<Task> {
    const response = await axiosInstance.post(ENDPOINTS.TASKS.CREATE(projectId), data);
    return response.data;
  }

  async update(id: number, data: TaskUpdateRequest): Promise<Task> {
    const response = await axiosInstance.patch(ENDPOINTS.TASKS.UPDATE(id), data);
    return response.data;
  }

  async delete(id: number): Promise<void> {
    await axiosInstance.delete(ENDPOINTS.TASKS.DELETE(id));
  }

  async getMyTasks(skip = 0, limit = 50): Promise<Task[]> {
    const response = await axiosInstance.get(ENDPOINTS.TASKS.MY_TASKS, {
      params: { skip, limit },
    });
    return response.data;
  }
}

export default new TasksAPI();
