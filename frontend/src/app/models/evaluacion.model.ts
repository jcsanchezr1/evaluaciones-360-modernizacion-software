export interface Evaluacion {
  id: string;
  id_consecutivo: number;
  nombre: string;
  instrucciones: string;
  nombre_formulario: string;
  fecha_insercion: string; // o Date si lo parseas
  esta_eliminada: boolean;
}