// Configuración de API
// Define URLs base y constantes de API

// URL base de la API
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
export const API_PREFIX = "/api";

// Endpoints
export const ENDPOINTS = {
  AUTH: {
    REGISTER: `${API_PREFIX}/auth/register`,
    LOGIN: `${API_PREFIX}/auth/login`,
    ME: `${API_PREFIX}/auth/me`,
  },
  PROJECTS: {
    LIST: `${API_PREFIX}/projects`,
    CREATE: `${API_PREFIX}/projects`,
    DETAIL: (id: number) => `${API_PREFIX}/projects/${id}`,
    UPDATE: (id: number) => `${API_PREFIX}/projects/${id}`,
    DELETE: (id: number) => `${API_PREFIX}/projects/${id}`,
    ADD_MEMBER: (id: number) => `${API_PREFIX}/projects/${id}/members`,
    REMOVE_MEMBER: (id: number, userId: number) => `${API_PREFIX}/projects/${id}/members/${userId}`,
    TASKS: (id: number) => `${API_PREFIX}/projects/${id}/tasks`,
  },
  TASKS: {
    CREATE: `${API_PREFIX}/tasks`,
    DETAIL: (id: number) => `${API_PREFIX}/tasks/${id}`,
    UPDATE: (id: number) => `${API_PREFIX}/tasks/${id}`,
    DELETE: (id: number) => `${API_PREFIX}/tasks/${id}`,
    MY_TASKS: `${API_PREFIX}/tasks/my-tasks`,
  },
} as const;

// Timeout para requests (ms)
export const API_TIMEOUT = 30000;

// Número de reintentos para requests fallidos
export const API_RETRIES = 3;

// Delay entre reintentos (ms)
export const API_RETRY_DELAY = 1000;
