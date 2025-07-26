import { Component, OnInit } from '@angular/core';
import { Evaluacion } from '../../models/evaluacion.model';
import { ActivatedRoute, Router } from '@angular/router';
import { EvaluacionService } from '../../services/evaluacion';

@Component({
  selector: 'app-evaluation-configuration',
  standalone: false,
  templateUrl: './evaluation-configuration.html',
  styleUrl: './evaluation-configuration.scss'
})
export class EvaluationConfiguration implements OnInit {
  evaluacion!: Evaluacion;
  evaluacionOriginal!: Evaluacion;
  idEvaluacion!: string;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private evaluacionService: EvaluacionService
  ) {}

  ngOnInit(): void {
    this.idEvaluacion = this.route.snapshot.paramMap.get('id')!;
    this.evaluacionService.obtenerEvaluaciones().subscribe({
      next: (evaluaciones) => {
        const encontrada = evaluaciones.find(e => e.id === this.idEvaluacion);
        if (encontrada) {
          this.evaluacion = { ...encontrada };
          this.evaluacionOriginal = { ...encontrada };
        } else {
          alert('Evaluación no encontrada');
        }
      },
      error: (err) => {
        console.error('Error al obtener evaluación:', err);
      },
    });
  }

  guardar(): void {
    if (!this.evaluacion.nombre_formulario || this.evaluacion.nombre_formulario === '') {
      alert('Debe seleccionar un formulario');
      return;
    }

    const payload = {
      nombre: this.evaluacion.nombre,
      instrucciones: this.evaluacion.instrucciones,
      nombre_formulario: this.evaluacion.nombre_formulario,
    };

    this.evaluacionService.actualizarEvaluacion(this.evaluacion.id, payload).subscribe({
      next: () => {
        alert('Formulario asignado correctamente');
        this.router.navigate(['/evaluations']);
      },
      error: (err) => {
        console.error('Error al guardar:', err);
        alert('No se pudo guardar');
      },
    });
  }

  eliminarFormulario(): void {
    this.evaluacion.nombre_formulario = '';
  }

  descartar(): void {
    this.evaluacion.nombre_formulario = this.evaluacionOriginal.nombre_formulario;
  }

  volver(): void {
    this.router.navigate(['/evaluations']);
  }
}
