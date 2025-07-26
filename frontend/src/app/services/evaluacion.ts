import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Evaluacion } from '../models/evaluacion.model';

export interface CrearEvaluacionPayload {
  nombre: string;
  instrucciones: string;
  nombre_formulario: string;
}

@Injectable({
  providedIn: 'root'
})
export class EvaluacionService {
  private baseUrl = 'http://localhost:8080/evaluaciones';

  constructor(private http: HttpClient) {}

  obtenerEvaluaciones() {
    return this.http.get<Evaluacion[]>(this.baseUrl);
  }

  crearEvaluacion(payload: CrearEvaluacionPayload): Observable<any> {
    return this.http.post(this.baseUrl, payload);
  }

  eliminarEvaluacion(id: string) {
  return this.http.delete(`${this.baseUrl}/${id}`);
}
}
