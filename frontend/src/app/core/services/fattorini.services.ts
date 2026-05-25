import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../enviroments/enviroments';
import { Fattorino } from '../models';

@Injectable({ providedIn: 'root' })
export class FattoriniService {
  private http = inject(HttpClient);
  private base = `${environment.apiUrl}/fattorini`;

  getAll(disponibile?: boolean): Observable<Fattorino[]> {
    let params = new HttpParams();
    if (disponibile !== undefined) params = params.set('disponibile', disponibile ? '1' : '0');
    return this.http.get<Fattorino[]>(`${this.base}/`, { params });
  }
  getById(id: number): Observable<Fattorino> {
    return this.http.get<Fattorino>(`${this.base}/${id}`);
  }
  create(data: Partial<Fattorino>): Observable<any> {
    return this.http.post(`${this.base}/`, data);
  }
  update(id: number, data: Partial<Fattorino>): Observable<any> {
    return this.http.put(`${this.base}/${id}`, data);
  }
  delete(id: number): Observable<any> {
    return this.http.delete(`${this.base}/${id}`);
  }
}