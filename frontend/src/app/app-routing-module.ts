import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { Evaluations } from './evaluations/evaluations';

const routes: Routes = [
  { path: '', redirectTo: 'evaluations', pathMatch: 'full' },
  { path: 'evaluations', component: Evaluations },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
