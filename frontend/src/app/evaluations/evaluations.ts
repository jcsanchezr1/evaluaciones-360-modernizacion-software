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
export class Evaluations implements OnInit {
  evaluations: EvaluacionUI[] = [];
  originalEvaluation: any = null;
  editingId: number | null = null;
  selectedEvaluacion: Evaluacion | null = null;

  constructor(
    private evaluacionService: EvaluacionService,
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
    const hasEmpty = this.evaluations.some((e) => e.nombre.trim() === '');

    if (hasEmpty || this.editingId !== null) {
      alert('El nombre de la evaluación no puede estar vacío.');
      return;
    }

    const newEvaluation: EvaluacionUI = {
      id: '', // se sobrescribirá después del POST
      id_consecutivo: 0,
      nombre: '',
      instrucciones: '',
      nombre_formulario: '',
      fecha_insercion: '',
      esta_eliminada: false,
      esNueva: true,
    };

    this.evaluations.push(newEvaluation);
    this.editingId = this.evaluations.length - 1;
  }

  saveEvaluations(): void {
    if (this.editingId === null) return;

    const evaluacion = this.evaluations[this.editingId];
    if (!evaluacion || evaluacion.nombre.trim() === '') {
      alert('El nombre no puede estar vacío.');
      return;
    }

    const payload = {
      nombre: evaluacion.nombre,
      instrucciones: evaluacion.instrucciones,
      nombre_formulario: evaluacion.nombre_formulario,
    };

    const request$ = evaluacion.esNueva
      ? this.evaluacionService.crearEvaluacion(payload)
      : this.evaluacionService.actualizarEvaluacion(evaluacion.id, payload);

    request$.subscribe({
      next: (response) => {
        if (evaluacion.esNueva) {
          // Actualizar los campos desde la respuesta
          evaluacion.id = response.id;
          evaluacion.id_consecutivo = response.id_consecutivo;
          evaluacion.fecha_insercion = response.fecha_insercion;
          evaluacion.esta_eliminada = response.esta_eliminada;
          evaluacion.esNueva = false;
        }

        alert('Evaluación guardada correctamente.');
        this.editingId = null;
      },
      error: (err) => {
        console.error('Error al guardar:', err);
        alert('Error al guardar evaluación.');
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

  configurarEvaluacion(id: string): void {
    this.router.navigate(['/evaluations', id, 'configuracion']);
  }
}
interface EvaluacionUI extends Evaluacion {
  esNueva?: boolean; // propiedad auxiliar para saber si es nueva
}
