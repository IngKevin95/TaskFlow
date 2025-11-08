# TaskFlow Frontend

SPA (Single Page Application) desarrollada con React 18, TypeScript, Vite y Tailwind CSS.

## 🚀 Inicio Rápido

### Requisitos Previos

- Node.js 16+ y npm/yarn
- Backend API corriendo en http://localhost:8000

### Instalación

1. **Instalar dependencias**
```bash
npm install
```

2. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env si es necesario (por defecto apunta a localhost:8000)
```

3. **Ejecutar servidor de desarrollo**
```bash
npm run dev
```

La aplicación abrirá automáticamente en http://localhost:5173

## 📁 Estructura del Proyecto

```
src/
├── api/                   # Servicios de API
│   ├── auth.api.ts
│   ├── projects.api.ts
│   ├── tasks.api.ts
│   └── axiosInstance.ts   # Cliente HTTP configurado
├── components/            # Componentes React
│   ├── auth/              # Componentes de autenticación (LoginForm, RegisterForm, ProtectedRoute)
│   ├── projects/          # Componentes de proyectos (ProjectCard, ProjectForm)
│   ├── tasks/             # Componentes de tareas (TaskCard, TaskForm, etc)
│   └── styles/            # Estilos de componentes
├── context/               # Context API
│   └── AuthContext.tsx
├── hooks/                 # Custom Hooks
│   ├── useAuth.ts
│   ├── useProject.ts
│   └── useTask.ts
├── pages/                 # Páginas (AuthPage, ProjectsPage, ProjectDetailPage, etc)
├── layouts/               # Layouts (MainLayout, etc)
├── router/                # Configuración de rutas (AppRouter)
├── types/                 # TypeScript types
├── utils/                 # Funciones utilitarias
├── config/                # Configuración
│   ├── api.config.ts
│   └── constants.ts
├── styles/                # Estilos globales (index.css)
├── App.tsx                # Componente principal
├── main.tsx               # Punto de entrada
└── vite-env.d.ts          # Tipos de Vite
```

## 🏗️ Características Principales

### ✅ Autenticación
- Registro de usuarios con validación
- Login con JWT
- Rutas protegidas con ProtectedRoute
- Persistencia de sesión en localStorage
- Logout automático en 401

### 📊 Gestión de Proyectos (FASE 3 ✅)
- Listado con búsqueda en tiempo real
- Crear nuevos proyectos
- Ver detalles del proyecto
- Tablero Kanban con tareas por estado
- Listar miembros del proyecto
- Eliminar proyectos

### 📝 Gestión de Tareas (FASE 4 ✅)
- Vista personal de tareas asignadas (TasksPage)
- Tablero Kanban con 4 columnas (Pendiente, En Progreso, En Revisión, Completado)
- Cambiar estado de tareas desde selectores
- Buscar tareas en tiempo real
- Filtrar por prioridad (Baja, Media, Alta, Crítica)
- Filtrar por estado
- Indicadores visuales de prioridad
- Formulario completo para crear/editar tareas
- Contadores de caracteres en formulario
- Selector de fecha de vencimiento
- Asignar tareas (mostrar asignado)
- Eliminar tareas con confirmación
- Estadísticas en vivo (total, completadas, en progreso)

### 🎨 Interfaz de Usuario
- Diseño responsivo con Tailwind CSS
- Componentes Material-UI
- Indicadores visuales de prioridad
- Estados de carga y error
- Notificaciones

## 📦 Dependencias Principales

- **react**: Framework UI
- **react-router-dom**: Routing
- **axios**: Cliente HTTP
- **@mui/material**: Componentes UI
- **@reduxjs/toolkit**: State management
- **tailwindcss**: Styling
- **vite**: Build tool y dev server

## 🧪 Testing

```bash
# Ejecutar tests
npm run test

# Ejecutar tests en watch mode
npm run test:watch

# Generar coverage report
npm run test:coverage

# UI de tests
npm run test:ui
```

## 🛠️ Desarrollo

### Scripts Disponibles

- `npm run dev` - Iniciar servidor de desarrollo
- `npm run build` - Construir para producción
- `npm run preview` - Previsualizar build de producción
- `npm run lint` - Ejecutar linter (ESLint)
- `npm run type-check` - Verificar tipos con TypeScript
- `npm run format` - Formatear código con Prettier

### Convenciones de Código

- **Componentes**: PascalCase (`TaskCard.tsx`)
- **Archivos**: camelCase para utilities y hooks
- **Variables**: camelCase
- **Constantes**: UPPER_CASE
- **Tipos/Interfaces**: PascalCase

### Estructura de Componentes

```typescript
// Ejemplo de componente bien estructurado
interface TaskCardProps {
  task: Task;
  onEdit: (id: number) => void;
  onDelete: (id: number) => void;
}

const TaskCard: React.FC<TaskCardProps> = ({ task, onEdit, onDelete }) => {
  return (
    // Componente aquí
  );
};

export default TaskCard;
```

## 📚 Patrones y Best Practices

### Custom Hooks
Encapsulan lógica reutilizable:
```typescript
const { tasks, isLoading, error, fetchProjectTasks } = useTasks();
```

### Context API
Para estado global como autenticación:
```typescript
const { user, isAuthenticated, login, logout } = useAuth();
```

### API Services
Centralizan llamadas HTTP:
```typescript
import projectsAPI from '@/api/projects.api';
await projectsAPI.getAll();
```

## 🔐 Seguridad

- ✅ Tokens JWT almacenados en localStorage
- ✅ Validación en cliente y servidor
- ✅ CORS configurado en backend
- ✅ HTTPS recomendado en producción
- ✅ No exponer tokens en URLs

## 📈 Performance

- Code splitting automático con Vite
- Lazy loading de componentes
- Memoización de componentes
- Optimización de renders
- Tree shaking de dependencias

## 🚀 Despliegue

### Producción

1. **Build**
```bash
npm run build
```

2. **Distribuir contenido de `dist/`**

3. **Configurar servidor web** (nginx, Apache, etc.)

4. **Ejemplo nginx.conf**
```nginx
server {
  listen 80;
  server_name taskflow.example.com;
  
  root /var/www/taskflow/dist;
  
  location / {
    try_files $uri $uri/ /index.html;
  }
  
  location /api {
    proxy_pass http://backend:8000;
  }
}
```

## 🐛 Troubleshooting

### "API_BASE_URL is not defined"
Asegúrate de que `.env` está configurado correctamente.

### CORS errors
Verifica que el backend permite CORS desde tu dominio frontend.

### Componentes no aparecen
Verifica la consola para errores de import y asegúrate que los componentes están exportados.

## 📝 Contribuir

1. Crear rama (`git checkout -b feature/NewFeature`)
2. Commit cambios (`git commit -m 'Add NewFeature'`)
3. Push a rama (`git push origin feature/NewFeature`)
4. Abrir Pull Request

## 📄 Licencia

Proyecto bajo Licencia MIT.

## 📞 Soporte

Para issues o sugerencias, crear un issue en el repositorio.
