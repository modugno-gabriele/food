import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../enviroments/enviroments';
import { Cliente } from '../models';

@Injectable({ providedIn: 'root' })
export class ClientiService {
  private http = inject(HttpClient);
  private base = `${environment.apiUrl}/clienti`;

  getAll(cerca?: string): Observable<Cliente[]> {
    let params = new HttpParams();
    if (cerca) params = params.set('cerca', cerca);
    return this.http.get<Cliente[]>(`${this.base}/`, { params });
  }
  getById(id: number): Observable<Cliente> {
    return this.http.get<Cliente>(`${this.base}/${id}`);
  }
  create(data: Partial<Cliente>): Observable<any> {
    return this.http.post(`${this.base}/`, data);
  }
  update(id: number, data: Partial<Cliente>): Observable<any> {
    return this.http.put(`${this.base}/${id}`, data);
  }
  delete(id: number): Observable<any> {
    return this.http.delete(`${this.base}/${id}`);
  }
}