import { Component, Input, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
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

  constructor(
    private route: ActivatedRoute,
    private evaluacionService: EvaluacionService
  ) {}

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.evaluacionService.obtenerEvaluaciones().subscribe({
        next: (data) => {
          const match = data.find((e: Evaluacion) => e.id === id);
          if (match) {
            this.evaluacion = match;
          } else {
            console.warn(`Evaluación con id ${id} no encontrada`);
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

  guardar() {
    // Aquí podrías llamar a una función del padre para persistir
    alert('Guardado localmente en el modelo Evaluacion');
  }

  descartar() {
    // Restablecer el campo instrucciones desde una copia original si la guardas
    alert('Cambios descartados');
  }
  eliminar() {
    // Restablecer el campo instrucciones desde una copia original si la guardas
    alert('Cambios descartados');
  }
}
