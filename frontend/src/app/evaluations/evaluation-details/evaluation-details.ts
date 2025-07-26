import { Component, Input, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Evaluacion } from '../../models/evaluacion.model';

@Component({
  selector: 'app-evaluation-details',
  standalone: false,
  templateUrl: './evaluation-details.html',
  styleUrl: './evaluation-details.scss'
})
export class EvaluationDetails {
 @Input() evaluacion!: Evaluacion;

  editing = false;

  get detalles() {
    return [
      {
        id: 1,
        tipo: 'Instrucciones',
        valor: this.evaluacion.instrucciones
      }
    ];
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
}
