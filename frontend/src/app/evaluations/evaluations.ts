import { Component } from '@angular/core';

@Component({
  selector: 'app-evaluations',
  standalone: false,
  templateUrl: './evaluations.html',
  styleUrl: './evaluations.scss'
})
export class Evaluations {
evaluations = [
    { id: 1, name: 'EVALUACIÓN DE DESEMPEÑO' },
    { id: 2, name: 'Evaluación Design Thinking' },
  ];
}
