/**
 * TaskForm.test.tsx
 * Tests unitarios para componente TaskForm
 */

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import '@testing-library/jest-dom';
import TaskForm from '../TaskForm';

describe('TaskForm Component', () => {
  const mockOnSubmit = jest.fn();
  const mockOnCancel = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('debe renderizar el formulario vacío para crear tarea', () => {
    render(
      <TaskForm
        projectId={1}
        onSubmit={mockOnSubmit}
        onCancel={mockOnCancel}
      />
    );

    expect(screen.getByLabelText(/Título/)).toHaveValue('');
    expect(screen.getByLabelText(/Descripción/)).toHaveValue('');
    expect(screen.getByDisplayValue('medium')).toBeInTheDocument();
  });

  it('debe validar que el título sea requerido', async () => {
    render(
      <TaskForm
        projectId={1}
        onSubmit={mockOnSubmit}
        onCancel={mockOnCancel}
      />
    );

    const submitBtn = screen.getByText('Crear Tarea');
    fireEvent.click(submitBtn);

    await waitFor(() => {
      expect(screen.getByText('El título es requerido')).toBeInTheDocument();
    });

    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  it('debe validar que la descripción sea requerida', async () => {
    render(
      <TaskForm
        projectId={1}
        onSubmit={mockOnSubmit}
        onCancel={mockOnCancel}
      />
    );

    const titleInput = screen.getByLabelText(/Título/);
    await userEvent.type(titleInput, 'Nueva tarea');

    const submitBtn = screen.getByText('Crear Tarea');
    fireEvent.click(submitBtn);

    await waitFor(() => {
      expect(screen.getByText('La descripción es requerida')).toBeInTheDocument();
    });

    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  it('debe enviar el formulario con datos válidos', async () => {
    render(
      <TaskForm
        projectId={1}
        onSubmit={mockOnSubmit}
        onCancel={mockOnCancel}
      />
    );

    const titleInput = screen.getByLabelText(/Título/);
    const descriptionInput = screen.getByLabelText(/Descripción/);

    await userEvent.type(titleInput, 'Implementar feature');
    await userEvent.type(descriptionInput, 'Esta es una descripción de prueba');

    const submitBtn = screen.getByText('Crear Tarea');
    fireEvent.click(submitBtn);

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith(
        expect.objectContaining({
          title: 'Implementar feature',
          description: 'Esta es una descripción de prueba',
          priority: 'medium',
          status: 'pending',
        })
      );
    });
  });

  it('debe mostrar el contador de caracteres del título', async () => {
    render(
      <TaskForm
        projectId={1}
        onSubmit={mockOnSubmit}
        onCancel={mockOnCancel}
      />
    );

    const titleInput = screen.getByLabelText(/Título/);
    await userEvent.type(titleInput, 'Test');

    expect(screen.getByText('4/100')).toBeInTheDocument();
  });

  it('debe mostrar el contador de caracteres de la descripción', async () => {
    render(
      <TaskForm
        projectId={1}
        onSubmit={mockOnSubmit}
        onCancel={mockOnCancel}
      />
    );

    const descriptionInput = screen.getByLabelText(/Descripción/);
    await userEvent.type(descriptionInput, 'Test description');

    expect(screen.getByText('16/500')).toBeInTheDocument();
  });

  it('debe permitir cambiar la prioridad', async () => {
    render(
      <TaskForm
        projectId={1}
        onSubmit={mockOnSubmit}
        onCancel={mockOnCancel}
      />
    );

    const prioritySelect = screen.getByDisplayValue('medium');
    fireEvent.change(prioritySelect, { target: { value: 'critical' } });

    expect(screen.getByDisplayValue('critical')).toBeInTheDocument();
  });

  it('debe permitir cambiar el estado', async () => {
    render(
      <TaskForm
        projectId={1}
        onSubmit={mockOnSubmit}
        onCancel={mockOnCancel}
      />
    );

    const statusSelect = screen.getByDisplayValue('pending');
    fireEvent.change(statusSelect, { target: { value: 'in_progress' } });

    expect(screen.getByDisplayValue('in_progress')).toBeInTheDocument();
  });

  it('debe permitir establecer una fecha de vencimiento', async () => {
    render(
      <TaskForm
        projectId={1}
        onSubmit={mockOnSubmit}
        onCancel={mockOnCancel}
      />
    );

    const dateInput = screen.getByLabelText(/Fecha de Vencimiento/);
    await userEvent.type(dateInput, '2025-12-31');

    expect(dateInput).toHaveValue('2025-12-31');
  });

  it('debe llamar a onCancel cuando se hace clic en Cancelar', () => {
    render(
      <TaskForm
        projectId={1}
        onSubmit={mockOnSubmit}
        onCancel={mockOnCancel}
      />
    );

    const cancelBtn = screen.getByText('Cancelar');
    fireEvent.click(cancelBtn);

    expect(mockOnCancel).toHaveBeenCalled();
  });

  it('debe deshabilitar botones mientras se envía', async () => {
    const delayedSubmit = jest.fn(() => new Promise(resolve => setTimeout(resolve, 100)));

    render(
      <TaskForm
        projectId={1}
        onSubmit={delayedSubmit}
        onCancel={mockOnCancel}
        isLoading={true}
      />
    );

    const submitBtn = screen.getByText('Guardando...');
    expect(submitBtn).toBeDisabled();

    const cancelBtn = screen.getByText('Cancelar');
    expect(cancelBtn).toBeDisabled();
  });

  it('debe mostrar "Actualizar Tarea" cuando se edita', () => {
    const mockTask = {
      id: 1,
      title: 'Tarea existente',
      description: 'Descripción existente',
      status: 'pending',
      priority: 'high',
      dueDate: '2025-01-15',
      assignedToId: 1,
      assignedToName: 'Juan',
      projectId: 1,
      createdBy: 1,
      createdAt: '2025-01-01T10:00:00Z',
      updatedAt: '2025-01-01T10:00:00Z',
    };

    render(
      <TaskForm
        projectId={1}
        task={mockTask}
        onSubmit={mockOnSubmit}
        onCancel={mockOnCancel}
      />
    );

    expect(screen.getByText('Actualizar Tarea')).toBeInTheDocument();
    expect(screen.getByDisplayValue('Tarea existente')).toBeInTheDocument();
  });

  it('debe limpiar errores al escribir', async () => {
    render(
      <TaskForm
        projectId={1}
        onSubmit={mockOnSubmit}
        onCancel={mockOnCancel}
      />
    );

    const submitBtn = screen.getByText('Crear Tarea');
    fireEvent.click(submitBtn);

    await waitFor(() => {
      expect(screen.getByText('El título es requerido')).toBeInTheDocument();
    });

    const titleInput = screen.getByLabelText(/Título/);
    await userEvent.type(titleInput, 'Test');

    expect(screen.queryByText('El título es requerido')).not.toBeInTheDocument();
  });
});
