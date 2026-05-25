import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../enviroments/enviroments';
import { Categoria } from '../models';

@Injectable({ providedIn: 'root' })
export class CategorieService {
  private http = inject(HttpClient);
  private base = `${environment.apiUrl}/categorie`;

  getAll(): Observable<Categoria[]> {
    return this.http.get<Categoria[]>(`${this.base}/`);
  }
  getById(id: number): Observable<Categoria> {
    return this.http.get<Categoria>(`${this.base}/${id}`);
  }
  create(data: Partial<Categoria>): Observable<any> {
    return this.http.post(`${this.base}/`, data);
  }
  update(id: number, data: Partial<Categoria>): Observable<any> {
    return this.http.put(`${this.base}/${id}`, data);
  }
  delete(id: number): Observable<any> {
    return this.http.delete(`${this.base}/${id}`);
  }
}