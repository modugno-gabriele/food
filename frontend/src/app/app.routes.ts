import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', redirectTo: 'ristoranti', pathMatch: 'full' },
  {
    path: 'ristoranti',
    loadComponent: () =>
      import('./pages/ristoranti/ristoranti.component').then(m => m.RistorantiComponent)
  },
  {
    path: 'categorie',
    loadComponent: () =>
      import('./pages/categorie/categorie.component').then(m => m.CategorieComponent)
  },
  {
    path: 'piatti',
    loadComponent: () =>
      import('./pages/piatti/piatti.component').then(m => m.PiattiComponent)
  },
  {
    path: 'ingredienti',
    loadComponent: () =>
      import('./pages/ingredienti/ingredienti.component').then(m => m.IngredientiComponent)
  },
  {
    path: 'clienti',
    loadComponent: () =>
      import('./pages/clienti/clienti.component').then(m => m.ClientiComponent)
  },
  {
    path: 'ordini',
    loadComponent: () =>
      import('./pages/ordini/ordini.component').then(m => m.OrdiniComponent)
  },
  {
    path: 'fattorini',
    loadComponent: () =>
      import('./pages/fattorini/fattorini.component').then(m => m.FattoriniComponent)
  },
  {
    path: 'recensioni',
    loadComponent: () =>
      import('./pages/recensioni/recensioni.component').then(m => m.RecensioniComponent)
  },
  { path: '**', redirectTo: 'ristoranti' }
];