import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { Categoria, Ristorante, Piatto, Recensione } from '../models/models';

@Injectable({ providedIn: 'root' })
export class ApiService {

  private base = environment.apiUrl;

  constructor(private http: HttpClient) {}

  // ── Categorie ─────────────────────────────────────────────────────
  getCategorie(): Observable<Categoria[]> {
    return this.http.get<Categoria[]>(`${this.base}/categorie/`);
  }

  // ── Ristoranti ────────────────────────────────────────────────────
  getRistoranti(idCategoria?: number, cerca?: string): Observable<Ristorante[]> {
    let params = new HttpParams();
    if (idCategoria) params = params.set('categoria', idCategoria);
    if (cerca)       params = params.set('cerca', cerca);
    return this.http.get<Ristorante[]>(`${this.base}/ristoranti/`, { params });
  }

  getRistorante(id: number): Observable<Ristorante> {
    return this.http.get<Ristorante>(`${this.base}/ristoranti/${id}`);
  }

  creaRistorante(data: Partial<Ristorante>): Observable<any> {
    return this.http.post(`${this.base}/ristoranti/`, data);
  }

  aggiornaRistorante(id: number, data: Partial<Ristorante>): Observable<any> {
    return this.http.put(`${this.base}/ristoranti/${id}`, data);
  }

  eliminaRistorante(id: number): Observable<any> {
    return this.http.delete(`${this.base}/ristoranti/${id}`);
  }

  // ── Piatti ───────────────────────────────────────────────────────
  getPiatti(idRistorante?: number, cerca?: string): Observable<Piatto[]> {
    let params = new HttpParams();
    if (idRistorante) params = params.set('ristorante', idRistorante);
    if (cerca)        params = params.set('cerca', cerca);
    return this.http.get<Piatto[]>(`${this.base}/piatti/`, { params });
  }

  getPiatto(id: number): Observable<Piatto> {
    return this.http.get<Piatto>(`${this.base}/piatti/${id}`);
  }

  // ── Recensioni ────────────────────────────────────────────────────
  getRecensioni(idRistorante?: number): Observable<Recensione[]> {
    let params = new HttpParams();
    if (idRistorante) params = params.set('ristorante', idRistorante);
    return this.http.get<Recensione[]>(`${this.base}/recensioni/`, { params });
  }

  creaRecensione(data: Partial<Recensione>): Observable<any> {
    return this.http.post(`${this.base}/recensioni/`, data);
  }
}
