import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../enviroments/enviroments';
import { Ingrediente } from '../models';

@Injectable({ providedIn: 'root' })
export class IngredientiService {
  private http = inject(HttpClient);
  private base = `${environment.apiUrl}/ingredienti`;

  getAll(cerca?: string, allergenico?: boolean): Observable<Ingrediente[]> {
    let params = new HttpParams();
    if (cerca) params = params.set('cerca', cerca);
    if (allergenico !== undefined) params = params.set('allergenico', allergenico ? '1' : '0');
    return this.http.get<Ingrediente[]>(`${this.base}/`, { params });
  }
  getById(id: number): Observable<Ingrediente> {
    return this.http.get<Ingrediente>(`${this.base}/${id}`);
  }
  create(data: Partial<Ingrediente>): Observable<any> {
    return this.http.post(`${this.base}/`, data);
  }
  update(id: number, data: Partial<Ingrediente>): Observable<any> {
    return this.http.put(`${this.base}/${id}`, data);
  }
  delete(id: number): Observable<any> {
    return this.http.delete(`${this.base}/${id}`);
  }
}