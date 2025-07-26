import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { Evaluations } from './evaluations/evaluations';
import { EvaluationDetails } from './evaluations/evaluation-details/evaluation-details';
import { EvaluationConfiguration } from './evaluations/evaluation-configuration/evaluation-configuration';

const routes: Routes = [
  { path: '', redirectTo: 'evaluations', pathMatch: 'full' },
  { path: 'evaluations', component: Evaluations },
  { path: 'evaluations/:id/detalles', component: EvaluationDetails },
  { path: 'evaluations/:id/configuracion', component: EvaluationConfiguration }

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
