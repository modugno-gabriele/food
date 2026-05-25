import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../enviroments/enviroments';
import { Recensione } from '../models';

@Injectable({ providedIn: 'root' })
export class RecensioniService {
  private http = inject(HttpClient);
  private base = `${environment.apiUrl}/recensioni`;

  getAll(ristorante?: number, cliente?: number): Observable<Recensione[]> {
    let params = new HttpParams();
    if (ristorante) params = params.set('ristorante', ristorante);
    if (cliente) params = params.set('cliente', cliente);
    return this.http.get<Recensione[]>(`${this.base}/`, { params });
  }
  getById(id: number): Observable<Recensione> {
    return this.http.get<Recensione>(`${this.base}/${id}`);
  }
  create(data: Partial<Recensione>): Observable<any> {
    return this.http.post(`${this.base}/`, data);
  }
  update(id: number, data: Partial<Recensione>): Observable<any> {
    return this.http.put(`${this.base}/${id}`, data);
  }
  delete(id: number): Observable<any> {
    return this.http.delete(`${this.base}/${id}`);
  }
}