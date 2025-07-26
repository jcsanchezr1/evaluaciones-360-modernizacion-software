import { Component } from '@angular/core';
import { EvaluacionService } from '../services/evaluacion';
import { Evaluacion } from '../models/evaluacion.model';

@Component({
  selector: 'app-evaluations',
  standalone: false,
  templateUrl: './evaluations.html',
  styleUrl: './evaluations.scss',
})
export class Evaluations {
  evaluations: Partial<Evaluacion & { id: number }>[] = [
    {
      nombre: 'EVALUACIÓN DE DESEMPEÑO',
      instrucciones: 'Instrucciones para EVALUACIÓN DE DESEMPEÑO',
      nombre_formulario: 'Formulario_1',
      fecha_insercion: new Date().toISOString(),
      esta_eliminada: false,
    },
    {
      nombre: 'Evaluación Design Thinking',
      instrucciones: 'Instrucciones para Evaluación Design Thinking',
      nombre_formulario: 'Formulario_2',
      fecha_insercion: new Date().toISOString(),
      esta_eliminada: false,
    },
  ];

  editingId: number | null = null;

  constructor(private evaluacionService: EvaluacionService) {}

  setEditing(index: number): void {
    this.editingId = index;
  }

  updateName(index: number, event: Event): void {
    const input = event.target as HTMLInputElement;
    const newValue = input.value.trim();
    const evaluation = this.evaluations[index];
    if (!evaluation) return;

    if (newValue === '') {
      input.classList.add('is-invalid');
      return;
    }

    input.classList.remove('is-invalid');
    evaluation.nombre = newValue;
  }

  clearEditing(): void {
    const evaluation = this.evaluations[this.editingId!];
    if (evaluation && evaluation.nombre?.trim() === '') {
      return;
    }
    this.editingId = null;
  }

  addEvaluation(): void {
    const hasEmpty = this.evaluations.some((e) => e.nombre?.trim() === '');

    if (hasEmpty || this.editingId !== null) {
      alert('Debes completar la evaluación actual antes de agregar una nueva.');
      return;
    }

    const newEvaluation = {
      nombre: '',
      instrucciones: '',
      nombre_formulario: '',
    };

    this.evaluations.push(newEvaluation);
    this.editingId = this.evaluations.length - 1; // usa el índice como identificador temporal
  }

  saveEvaluations(): void {
    if (this.editingId === null) {
      alert('No hay ninguna evaluación en edición.');
      return;
    }

    const evalToSave = this.evaluations[this.editingId];
    if (!evalToSave || !evalToSave.nombre || evalToSave.nombre.trim() === '') {
      alert('El nombre de la evaluación es obligatorio.');
      return;
    }

    const payload = {
      nombre: evalToSave.nombre.trim(),
      instrucciones: "la siguiente evaluación es para evaluar el desempeño del personal, selecione las opciones que mejor describan el desempeño del evaluado.",
      nombre_formulario: "Asperctos academicos",
    };

    this.evaluacionService.crearEvaluacion(payload).subscribe({
      next: (response) => {
        console.log('Evaluación creada:', response);
        alert('Evaluación guardada exitosamente.');
        this.editingId = null; // salimos del modo edición
      },
      error: (err) => {
        console.error('Error al guardar:', err.message);
        alert('Hubo un error al guardar la evaluación.');
      },
    });
  }
}
