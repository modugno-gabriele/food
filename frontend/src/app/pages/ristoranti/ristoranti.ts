import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RistorantiService } from '../../core/services/ristoranti.services';
import { CategorieService } from '../../core/services/categoria.services';
import { Ristorante, Categoria } from '../../core/models';

@Component({
  selector: 'app-ristoranti',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './ristoranti.component.html',
  styleUrl: './ristoranti.component.css'
})
export class RistorantiComponent implements OnInit {
  private svc = inject(RistorantiService);
  private catSvc = inject(CategorieService);

  ristoranti: Ristorante[] = [];
  categorie: Categoria[] = [];
  caricamento = false;
  errore = '';

  filtroNome = '';
  filtroCategoria = '';

  modaleAperto = false;
  editing = false;
  editingId: number | null = null;
  form: Partial<Ristorante> = {};

  ngOnInit() {
    this.carica();
    this.catSvc.getAll().subscribe({ next: c => this.categorie = c });
  }

  carica() {
    this.caricamento = true;
    this.svc.getAll(
      this.filtroNome || undefined,
      this.filtroCategoria ? +this.filtroCategoria : undefined
    ).subscribe({
      next: r => { this.ristoranti = r; this.caricamento = false; },
      error: e => { this.errore = e.message; this.caricamento = false; }
    });
  }

  apriModale(r?: Ristorante) {
    if (r) {
      this.editing = true;
      this.editingId = r.id_ristorante;
      this.form = {
        nome: r.nome,
        indirizzo: r.indirizzo,
        telefono: r.telefono,
        id_categoria: r.id_categoria
      };
    } else {
      this.editing = false;
      this.editingId = null;
      this.form = {};
    }
    this.modaleAperto = true;
  }

  chiudiModale() {
    this.modaleAperto = false;
  }

  salva() {
    if (!this.form.nome) return;
    const op = this.editing
      ? this.svc.update(this.editingId!, this.form)
      : this.svc.create(this.form);

    op.subscribe({
      next: () => { this.chiudiModale(); this.carica(); },
      error: e => { this.errore = e.message; }
    });
  }

  elimina(id: number) {
    if (!confirm('Eliminare questo ristorante?')) return;
    this.svc.delete(id).subscribe({
      next: () => this.carica(),
      error: e => { this.errore = e.message; }
    });
  }
}