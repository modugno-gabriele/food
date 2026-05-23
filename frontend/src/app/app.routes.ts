import { Routes } from '@angular/router';
import { CategorieComponent } from './components/categorie/categorie.component';
import { RistorantiComponent } from './components/ristoranti/ristoranti.component';
import { DettaglioRistoranteComponent } from './components/ristoranti/dettaglio-ristorante.component';
import { DettaglioPiattoComponent } from './components/piatti/dettaglio-piatto.component';

export const routes: Routes = [
  { path: '',                              redirectTo: 'categorie', pathMatch: 'full' },
  { path: 'categorie',                     component: CategorieComponent },
  { path: 'ristoranti',                    component: RistorantiComponent },
  { path: 'ristoranti/categoria/:id',      component: RistorantiComponent },
  { path: 'ristoranti/:id',               component: DettaglioRistoranteComponent },
  { path: 'piatti/:id',                    component: DettaglioPiattoComponent },
  { path: '**',                            redirectTo: 'categorie' }
];
