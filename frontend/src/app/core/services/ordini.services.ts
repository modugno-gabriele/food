import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../enviroments/enviroments';
import { Ordine } from '../models';

@Injectable({ providedIn: 'root' })
export class OrdiniService {
  private http = inject(HttpClient);
  private base = `${environment.apiUrl}/ordini`;

  getAll(stato?: string, cliente?: number): Observable<Ordine[]> {
    let params = new HttpParams();
    if (stato) params = params.set('stato', stato);
    if (cliente) params = params.set('cliente', cliente);
    return this.http.get<Ordine[]>(`${this.base}/`, { params });
  }
  getById(id: number): Observable<Ordine> {
    return this.http.get<Ordine>(`${this.base}/${id}`);
  }
  create(data: Partial<Ordine>): Observable<any> {
    return this.http.post(`${this.base}/`, data);
  }
  update(id: number, data: Partial<Ordine>): Observable<any> {
    return this.http.put(`${this.base}/${id}`, data);
  }
  delete(id: number): Observable<any> {
    return this.http.delete(`${this.base}/${id}`);
  }
}