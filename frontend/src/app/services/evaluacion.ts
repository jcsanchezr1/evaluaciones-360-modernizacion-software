import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

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

  crearEvaluacion(payload: CrearEvaluacionPayload): Observable<any> {
    return this.http.post(this.baseUrl, payload);
  }
}
