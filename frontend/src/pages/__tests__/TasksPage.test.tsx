/**
 * TasksPage.test.tsx
 * Tests unitarios para componente TasksPage
 */

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import '@testing-library/jest-dom';
import TasksPage from '../../TasksPage';

// Mock del hook useTask
jest.mock('../../../hooks/useTask', () => ({
  useTask: () => ({
    myTasks: [
      {
        id: 1,
        title: 'Tarea pendiente',
        description: 'Esta es una tarea pendiente',
        status: 'pending',
        priority: 'high',
        dueDate: '2025-01-15',
        assignedToId: 1,
        assignedToName: 'Juan',
        projectId: 1,
        createdBy: 1,
        createdAt: '2025-01-01T10:00:00Z',
        updatedAt: '2025-01-01T10:00:00Z',
      },
      {
        id: 2,
        title: 'Tarea en progreso',
        description: 'Esta es una tarea en progreso',
        status: 'in_progress',
        priority: 'medium',
        dueDate: '2025-01-20',
        assignedToId: 1,
        assignedToName: 'Juan',
        projectId: 1,
        createdBy: 1,
        createdAt: '2025-01-01T10:00:00Z',
        updatedAt: '2025-01-01T10:00:00Z',
      },
      {
        id: 3,
        title: 'Tarea completada',
        description: 'Esta es una tarea completada',
        status: 'completed',
        priority: 'low',
        dueDate: '2025-01-10',
        assignedToId: 1,
        assignedToName: 'Juan',
        projectId: 1,
        createdBy: 1,
        createdAt: '2025-01-01T10:00:00Z',
        updatedAt: '2025-01-01T10:00:00Z',
      },
    ],
    isLoading: false,
    error: null,
    fetchMyTasks: jest.fn(),
    updateStatus: jest.fn(),
    deleteTask: jest.fn(),
  }),
}));

describe('TasksPage Component', () => {
  it('debe renderizar la página de tareas', () => {
    render(<TasksPage />);

    expect(screen.getByText('Mis Tareas')).toBeInTheDocument();
  });

  it('debe mostrar el tablero Kanban con 4 columnas', () => {
    render(<TasksPage />);

    expect(screen.getByText('PENDIENTE')).toBeInTheDocument();
    expect(screen.getByText('EN PROGRESO')).toBeInTheDocument();
    expect(screen.getByText('EN REVISIÓN')).toBeInTheDocument();
    expect(screen.getByText('COMPLETADO')).toBeInTheDocument();
  });

  it('debe mostrar tareas en sus columnas correspondientes', () => {
    render(<TasksPage />);

    expect(screen.getByText('Tarea pendiente')).toBeInTheDocument();
    expect(screen.getByText('Tarea en progreso')).toBeInTheDocument();
    expect(screen.getByText('Tarea completada')).toBeInTheDocument();
  });

  it('debe filtrar tareas por estado', async () => {
    render(<TasksPage />);

    const statusFilter = screen.getByDisplayValue('all');
    fireEvent.change(statusFilter, { target: { value: 'completed' } });

    await waitFor(() => {
      expect(screen.getByText('Tarea completada')).toBeInTheDocument();
      expect(screen.queryByText('Tarea pendiente')).not.toBeInTheDocument();
    });
  });

  it('debe filtrar tareas por prioridad', async () => {
    render(<TasksPage />);

    const priorityFilter = screen.getByDisplayValue('all');
    fireEvent.change(priorityFilter, { target: { value: 'high' } });

    await waitFor(() => {
      expect(screen.getByText('Tarea pendiente')).toBeInTheDocument();
    });
  });

  it('debe buscar tareas por título', async () => {
    render(<TasksPage />);

    const searchInput = screen.getByPlaceholderText('Buscar tareas...');
    await userEvent.type(searchInput, 'pendiente');

    await waitFor(() => {
      expect(screen.getByText('Tarea pendiente')).toBeInTheDocument();
      expect(screen.queryByText('Tarea en progreso')).not.toBeInTheDocument();
    });
  });

  it('debe buscar tareas por descripción', async () => {
    render(<TasksPage />);

    const searchInput = screen.getByPlaceholderText('Buscar tareas...');
    await userEvent.type(searchInput, 'completada');

    await waitFor(() => {
      expect(screen.getByText('Tarea completada')).toBeInTheDocument();
    });
  });

  it('debe mostrar los contadores de tareas por columna', () => {
    render(<TasksPage />);

    // Verificar que existen badges con contadores
    const countBadges = screen.getAllByText(/^\d+$/);
    expect(countBadges.length).toBeGreaterThan(0);
  });

  it('debe mostrar estadísticas totales', () => {
    render(<TasksPage />);

    expect(screen.getByText('Total:')).toBeInTheDocument();
    expect(screen.getByText('Completado:')).toBeInTheDocument();
    expect(screen.getByText('En Progreso:')).toBeInTheDocument();
  });

  it('debe mostrar mensaje cuando no hay resultados de búsqueda', async () => {
    render(<TasksPage />);

    const searchInput = screen.getByPlaceholderText('Buscar tareas...');
    await userEvent.type(searchInput, 'tareaquenoexiste');

    await waitFor(() => {
      expect(screen.getAllByText('Sin tareas').length).toBeGreaterThan(0);
    });
  });

  it('debe limpiar la búsqueda cuando se borra el input', async () => {
    render(<TasksPage />);

    const searchInput = screen.getByPlaceholderText('Buscar tareas...');
    await userEvent.type(searchInput, 'pendiente');

    await waitFor(() => {
      expect(screen.getByText('Tarea pendiente')).toBeInTheDocument();
    });

    await userEvent.clear(searchInput);

    await waitFor(() => {
      expect(screen.getByText('Tarea en progreso')).toBeInTheDocument();
    });
  });

  it('debe resetear los filtros correctamente', async () => {
    render(<TasksPage />);

    const statusFilter = screen.getByDisplayValue('all');
    fireEvent.change(statusFilter, { target: { value: 'pending' } });

    await waitFor(() => {
      expect(screen.getByText('Tarea pendiente')).toBeInTheDocument();
    });

    fireEvent.change(statusFilter, { target: { value: 'all' } });

    await waitFor(() => {
      expect(screen.getByText('Tarea en progreso')).toBeInTheDocument();
      expect(screen.getByText('Tarea completada')).toBeInTheDocument();
    });
  });
});
