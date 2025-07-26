import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { Evaluations } from './evaluations/evaluations';
import { EvaluationDetails } from './evaluations/evaluation-details/evaluation-details';

const routes: Routes = [
  { path: '', redirectTo: 'evaluations', pathMatch: 'full' },
  { path: 'evaluations', component: Evaluations },
  { path: 'evaluations/:id/detalles', component: EvaluationDetails },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
