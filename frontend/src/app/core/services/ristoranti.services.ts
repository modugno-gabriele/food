import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../enviroments/enviroments';
import { Ristorante } from '../models';

@Injectable({ providedIn: 'root' })
export class RistorantiService {
  private http = inject(HttpClient);
  private base = `${environment.apiUrl}/ristoranti`;

  getAll(cerca?: string, categoria?: number): Observable<Ristorante[]> {
    let params = new HttpParams();
    if (cerca) params = params.set('cerca', cerca);
    if (categoria) params = params.set('categoria', categoria);
    return this.http.get<Ristorante[]>(`${this.base}/`, { params });
  }
  getById(id: number): Observable<Ristorante> {
    return this.http.get<Ristorante>(`${this.base}/${id}`);
  }
  create(data: Partial<Ristorante>): Observable<any> {
    return this.http.post(`${this.base}/`, data);
  }
  update(id: number, data: Partial<Ristorante>): Observable<any> {
    return this.http.put(`${this.base}/${id}`, data);
  }
  delete(id: number): Observable<any> {
    return this.http.delete(`${this.base}/${id}`);
  }
}