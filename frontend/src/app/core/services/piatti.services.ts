import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../enviroments/enviroments';
import { Piatto } from '../models';
@Injectable({ providedIn: 'root' })
export class PiattiService {
  private http = inject(HttpClient);
  private base = `${environment.apiUrl}/piatti`;

  getAll(cerca?: string, ristorante?: number, disponibile?: boolean): Observable<Piatto[]> {
    let params = new HttpParams();
    if (cerca) params = params.set('cerca', cerca);
    if (ristorante) params = params.set('ristorante', ristorante);
    if (disponibile !== undefined) params = params.set('disponibile', disponibile ? '1' : '0');
    return this.http.get<Piatto[]>(`${this.base}/`, { params });
  }
  getById(id: number): Observable<Piatto> {
    return this.http.get<Piatto>(`${this.base}/${id}`);
  }
  create(data: Partial<Piatto>): Observable<any> {
    return this.http.post(`${this.base}/`, data);
  }
  update(id: number, data: Partial<Piatto>): Observable<any> {
    return this.http.put(`${this.base}/${id}`, data);
  }
  delete(id: number): Observable<any> {
    return this.http.delete(`${this.base}/${id}`);
  }
}