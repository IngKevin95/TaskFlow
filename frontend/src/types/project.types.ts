// Tipos de proyecto

import { User } from "./auth.types";
import { Task } from "./task.types";

export interface Project {
  id: number;
  name: string;
  description?: string;
  owner_id: number;
  created_at: string;
  updated_at: string;
}

export interface ProjectWithDetails extends Project {
  owner?: User;
  members: User[];
  tasks: Task[];
}

export interface ProjectCreateRequest {
  name: string;
  description?: string;
}

export interface ProjectUpdateRequest {
  name?: string;
  description?: string;
}

export interface AddMemberRequest {
  user_id: number;
}

export interface ProjectsState {
  projects: Project[];
  currentProject: ProjectWithDetails | null;
  isLoading: boolean;
  error: string | null;
  total: number;
}
