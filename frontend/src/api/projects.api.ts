// Servicio de API para proyectos

import axiosInstance from "./axiosInstance";
import { ENDPOINTS } from "../config/api.config";
import { Project, ProjectWithDetails, ProjectCreateRequest, ProjectUpdateRequest, AddMemberRequest } from "../types";

class ProjectsAPI {
  async getAll(skip = 0, limit = 10): Promise<Project[]> {
    const response = await axiosInstance.get(ENDPOINTS.PROJECTS.LIST, {
      params: { skip, limit },
    });
    return response.data;
  }

  async getById(id: number): Promise<ProjectWithDetails> {
    const response = await axiosInstance.get(ENDPOINTS.PROJECTS.DETAIL(id));
    return response.data;
  }

  async create(data: ProjectCreateRequest): Promise<Project> {
    const response = await axiosInstance.post(ENDPOINTS.PROJECTS.CREATE, data);
    return response.data;
  }

  async update(id: number, data: ProjectUpdateRequest): Promise<Project> {
    const response = await axiosInstance.patch(ENDPOINTS.PROJECTS.UPDATE(id), data);
    return response.data;
  }

  async delete(id: number): Promise<void> {
    await axiosInstance.delete(ENDPOINTS.PROJECTS.DELETE(id));
  }

  async addMember(projectId: number, userId: number): Promise<void> {
    const data: AddMemberRequest = { user_id: userId };
    await axiosInstance.post(ENDPOINTS.PROJECTS.ADD_MEMBER(projectId), data);
  }

  async removeMember(projectId: number, userId: number): Promise<void> {
    await axiosInstance.delete(ENDPOINTS.PROJECTS.REMOVE_MEMBER(projectId, userId));
  }
}

export default new ProjectsAPI();
