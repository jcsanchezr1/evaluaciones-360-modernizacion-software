import { Component, Input, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Evaluacion } from '../../models/evaluacion.model';
import { EvaluacionService } from '../../services/evaluacion';

@Component({
  selector: 'app-evaluation-details',
  standalone: false,
  templateUrl: './evaluation-details.html',
  styleUrl: './evaluation-details.scss',
})
export class EvaluationDetails {
  evaluacion!: Evaluacion;
  evaluacionOriginal!: Evaluacion;
  idEvaluacion!: string;

  constructor(
    private route: ActivatedRoute,
    private evaluacionService: EvaluacionService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.idEvaluacion = this.route.snapshot.paramMap.get('id')!;
    if (this.idEvaluacion) {
      this.evaluacionService.obtenerEvaluaciones().subscribe({
        next: (data) => {
          const match = data.find((e: Evaluacion) => e.id === this.idEvaluacion);
          if (match) {
            this.evaluacion = { ...match };
            this.evaluacionOriginal = { ...match };
          } else {
            console.warn(`Evaluación con id ${this.idEvaluacion} no encontrada`);
          }
        },
        error: (err) => {
          console.error('Error al cargar evaluaciones:', err);
        },
      });
    }
  }

  updateValor(nuevoValor: string) {
    this.evaluacion.instrucciones = nuevoValor;
  }

  volver(): void {
    this.router.navigate(['/evaluations']);
  }

  guardar(): void {
   const payload = {
      nombre: this.evaluacion.nombre,
      instrucciones: this.evaluacion.instrucciones,
      nombre_formulario: this.evaluacion.nombre_formulario,
    };

    this.evaluacionService
      .actualizarEvaluacion(this.evaluacion.id, payload)
      .subscribe({
        next: () => {
          alert('Instrucción actualizada correctamente');
          this.evaluacionOriginal = { ...this.evaluacion }; 
          this.router.navigate(['/evaluations']);
        },
        error: (err) => {
          console.error('Error al guardar:', err);
          alert('No se pudo actualizar la evaluación.');
        },
      });
  }

  descartar() {
    this.evaluacion.instrucciones = this.evaluacionOriginal.instrucciones;
  }
  eliminar() {
    const payload = {
      nombre: this.evaluacion.nombre,
      instrucciones: "",
      nombre_formulario: this.evaluacion.nombre_formulario,
    };
    
    this.evaluacionService
      .actualizarEvaluacion(this.evaluacion.id, payload)
      .subscribe({
        next: () => {
          alert('Instrucción eliminada correctamente');
          this.evaluacionOriginal = { ...this.evaluacion }; 
          this.router.navigate(['/evaluations']);
        },
        error: (err) => {
          console.error('Error al guardar:', err);
          alert('No se pudo actualizar la evaluación.');
        },
      });
  }
}
