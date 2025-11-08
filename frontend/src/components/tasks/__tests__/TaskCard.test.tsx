/**
 * TaskCard.test.tsx
 * Tests unitarios para componente TaskCard
 */

import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import TaskCard from '../TaskCard';
import { Task } from '../../types/task.types';

describe('TaskCard Component', () => {
  const mockTask: Task = {
    id: 1,
    title: 'Implementar autenticación',
    description: 'Crear sistema de login y registro con JWT',
    status: 'in_progress',
    priority: 'high',
    dueDate: '2025-01-15',
    assignedToId: 2,
    assignedToName: 'Juan García',
    projectId: 1,
    createdBy: 1,
    createdAt: '2025-01-01T10:00:00Z',
    updatedAt: '2025-01-05T10:00:00Z',
  };

  it('debe renderizar la tarjeta de tarea correctamente', () => {
    render(
      <TaskCard task={mockTask} onStatusChange={() => {}} onDelete={() => {}} />
    );

    expect(screen.getByText('Implementar autenticación')).toBeInTheDocument();
    expect(screen.getByText(/Crear sistema de login/)).toBeInTheDocument();
  });

  it('debe mostrar la prioridad correctamente', () => {
    render(
      <TaskCard task={mockTask} onStatusChange={() => {}} onDelete={() => {}} />
    );

    expect(screen.getByText('High')).toBeInTheDocument();
  });

  it('debe mostrar el nombre del asignado', () => {
    render(
      <TaskCard task={mockTask} onStatusChange={() => {}} onDelete={() => {}} />
    );

    expect(screen.getByText(/Juan García/)).toBeInTheDocument();
  });

  it('debe cambiar estado cuando el usuario selecciona una opción', () => {
    const mockStatusChange = jest.fn();
    render(
      <TaskCard task={mockTask} onStatusChange={mockStatusChange} onDelete={() => {}} />
    );

    const statusSelect = screen.getByDisplayValue('in_progress');
    fireEvent.change(statusSelect, { target: { value: 'completed' } });

    expect(mockStatusChange).toHaveBeenCalledWith('completed');
  });

  it('debe llamar a onDelete cuando se hace clic en el botón eliminar', () => {
    const mockDelete = jest.fn();
    render(
      <TaskCard task={mockTask} onStatusChange={() => {}} onDelete={mockDelete} />
    );

    const deleteBtn = screen.getByTitle('Eliminar tarea');
    fireEvent.click(deleteBtn);

    expect(mockDelete).toHaveBeenCalled();
  });

  it('debe aplicar la clase de prioridad correcta', () => {
    const { container } = render(
      <TaskCard task={mockTask} onStatusChange={() => {}} onDelete={() => {}} />
    );

    expect(container.querySelector('.task-card.priority-high')).toBeInTheDocument();
  });

  it('debe formatear la fecha de vencimiento correctamente', () => {
    render(
      <TaskCard task={mockTask} onStatusChange={() => {}} onDelete={() => {}} />
    );

    // Debería mostrar algo como "15 ene"
    expect(screen.getByText(/ene/)).toBeInTheDocument();
  });

  it('debe renderizar sin mostrar fecha si no está disponible', () => {
    const taskSinFecha = { ...mockTask, dueDate: undefined };
    const { container } = render(
      <TaskCard task={taskSinFecha} onStatusChange={() => {}} onDelete={() => {}} />
    );

    expect(container.querySelector('.task-due-date')).not.toBeInTheDocument();
  });

  it('debe no mostrar asignado si no está disponible', () => {
    const taskSinAsignado = { ...mockTask, assignedToName: undefined };
    render(
      <TaskCard task={taskSinAsignado} onStatusChange={() => {}} onDelete={() => {}} />
    );

    expect(screen.queryByText(/Asignado a:/)).not.toBeInTheDocument();
  });

  it('debe aplicar la clase de estado correcta al selector', () => {
    const { container } = render(
      <TaskCard task={mockTask} onStatusChange={() => {}} onDelete={() => {}} />
    );

    const statusSelect = container.querySelector('.status-select.status-in_progress');
    expect(statusSelect).toBeInTheDocument();
  });
});
