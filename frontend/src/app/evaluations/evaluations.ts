import { Component, OnInit } from '@angular/core';
import { EvaluacionService } from '../services/evaluacion';
import { Evaluacion } from '../models/evaluacion.model';
import { Router } from '@angular/router';

@Component({
  selector: 'app-evaluations',
  standalone: false,
  templateUrl: './evaluations.html',
  styleUrl: './evaluations.scss',
})
export class Evaluations implements OnInit{
  evaluations: Partial<Evaluacion>[] = [];
  originalEvaluation: any = null;
  editingId: number | null = null;

  constructor(private evaluacionService: EvaluacionService,
              private router: Router
  ) {}
  ngOnInit(): void {
    this.getEvaluaciones();
  }

  getEvaluaciones(): void {
    this.evaluacionService.obtenerEvaluaciones().subscribe({
      next: (data) => {
        this.evaluations = data.filter((e) => !e.esta_eliminada);
      },
      error: (err) => {
        console.error('Error cargando evaluaciones:', err);
        alert('Hubo un error al obtener las evaluaciones.');
      },
    });
  }

  setEditing(index: number): void {
    this.editingId = index;
    this.originalEvaluation = { ...this.evaluations[index] };
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
      instrucciones: '',
      nombre_formulario: '',
    };

    this.evaluacionService.crearEvaluacion(payload).subscribe({
      next: (response) => {
        console.log('Evaluación creada:', response);
        alert('Evaluación guardada exitosamente.');
        this.editingId = null; // salimos del modo edición
        this.getEvaluaciones();
      },
      error: (err) => {
        console.error('Error al guardar:', err.message);
        alert('Hubo un error al guardar la evaluación.');
      },
    });
  }

  descartarCambios(): void {
    if (this.editingId === null) return;

    const evalActual = this.evaluations[this.editingId];

    const isNueva = !evalActual.id; // si no tiene ID del backend, es nueva

    if (isNueva) {
      this.evaluations.splice(this.editingId, 1); // eliminarla
    } else if (this.originalEvaluation) {
      this.evaluations[this.editingId] = { ...this.originalEvaluation }; // restaurar valores
    }

    this.editingId = null;
    this.originalEvaluation = null;
  }

  eliminarEvaluacion(index: number): void {
    const evaluacion = this.evaluations[index];

    const confirmacion = confirm('¿Estás seguro de eliminar esta evaluación?');
    if (!confirmacion) return;

    // Evaluación aún no guardada (sin ID del backend)
    if (!evaluacion.id) {
      this.evaluations.splice(index, 1);
      if (this.editingId === index) {
        this.editingId = null;
        this.originalEvaluation = null;
      }
      return;
    }

    // Evaluación ya existente
    this.evaluacionService.eliminarEvaluacion(evaluacion.id).subscribe({
      next: () => {
        this.evaluations.splice(index, 1);
        alert('Evaluación eliminada exitosamente.');
      },
      error: (err) => {
        console.error('Error eliminando evaluación:', err);
        alert('Error al eliminar la evaluación.');
      },
    });
  }
  verDetallesEvaluacion(id: string) {
  this.router.navigate(['/evaluations', id, 'detalles']);
}
}
