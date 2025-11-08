// Constantes de la aplicación

// Prioridades de tareas
export const TASK_PRIORITIES = {
  LOW: "low",
  MEDIUM: "medium",
  HIGH: "high",
  CRITICAL: "critical",
} as const;

// Estados de tareas
export const TASK_STATUSES = {
  PENDING: "pending",
  IN_PROGRESS: "in_progress",
  REVIEW: "review",
  COMPLETED: "completed",
} as const;

// Colores por prioridad
export const PRIORITY_COLORS = {
  low: "#4CAF50",      // Verde
  medium: "#FFC107",   // Amarillo
  high: "#FF9800",     // Naranja
  critical: "#F44336", // Rojo
} as const;

// Mensajes de error comunes
export const ERROR_MESSAGES = {
  NETWORK_ERROR: "Error de conexión. Intenta de nuevo.",
  UNAUTHORIZED: "No autorizado. Por favor inicia sesión.",
  FORBIDDEN: "No tienes permiso para realizar esta acción.",
  NOT_FOUND: "Recurso no encontrado.",
  SERVER_ERROR: "Error del servidor. Intenta más tarde.",
  VALIDATION_ERROR: "Por favor verifica los datos ingresados.",
} as const;

// Storage keys
export const STORAGE_KEYS = {
  TOKEN: "taskflow_token",
  USER: "taskflow_user",
  THEME: "taskflow_theme",
  LANGUAGE: "taskflow_language",
} as const;

// Límites de paginación
export const PAGINATION = {
  DEFAULT_PAGE_SIZE: 10,
  MAX_PAGE_SIZE: 100,
  DEFAULT_TASKS_LIMIT: 50,
} as const;
