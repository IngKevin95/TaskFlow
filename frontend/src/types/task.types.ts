// Tipos de tarea

import { User } from "./auth.types";
import { TaskPriority, TaskStatus } from "./auth.types";

export interface Task {
  id: number;
  title: string;
  description?: string;
  project_id: number;
  creator_id?: number;
  assigned_to_id?: number;
  priority: TaskPriority;
  status: TaskStatus;
  due_date?: string;
  created_at: string;
  updated_at: string;
}

export interface TaskWithAssignee extends Task {
  creator?: User;
  assigned_to?: User;
}

export interface TaskCreateRequest {
  title: string;
  description?: string;
  priority?: TaskPriority;
  due_date?: string;
  assigned_to_id?: number;
}

export interface TaskUpdateRequest {
  title?: string;
  description?: string;
  priority?: TaskPriority;
  status?: TaskStatus;
  due_date?: string;
  assigned_to_id?: number;
}

export interface TasksState {
  tasks: Task[];
  myTasks: Task[];
  isLoading: boolean;
  error: string | null;
  filters: {
    status?: TaskStatus;
    priority?: TaskPriority;
    assignedTo?: number;
  };
}
