// Tipos comunes

export interface ApiResponse<T> {
  data: T;
  status: number;
  message?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  skip: number;
  limit: number;
}

export interface ApiError {
  detail: string;
  status: number;
}

export interface NotificationMessage {
  id: string;
  type: "success" | "error" | "warning" | "info";
  message: string;
  duration?: number;
}

export interface UiState {
  loading: boolean;
  notifications: NotificationMessage[];
  theme: "light" | "dark";
  sidebarOpen: boolean;
}

export type AsyncThunkStatus = "idle" | "pending" | "fulfilled" | "rejected";
