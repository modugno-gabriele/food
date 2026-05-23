// ── Modelli dati (interfacce TypeScript) ─────────────────────────────

export interface Categoria {
  id_categoria: number;
  nome: string;
  descrizione: string;
}

export interface Ristorante {
  id_ristorante: number;
  id_categoria: number;
  nome: string;
  indirizzo: string;
  telefono: string;
  categoria?: string;
  media_voto?: number;
  num_recensioni?: number;
  piatti?: Piatto[];
}

export interface Piatto {
  id_piatto: number;
  id_ristorante: number;
  nome: string;
  prezzo: number;
  disponibile: boolean;
  ristorante?: string;
  ingredienti?: Ingrediente[];
}

export interface Ingrediente {
  id_ingrediente: number;
  nome: string;
  allergenico: boolean;
}

export interface Recensione {
  id_recensione: number;
  id_cliente: number;
  id_ristorante: number;
  data: string;
  commento: string;
  voto: number;
  cliente?: string;
  ristorante?: string;
}

export interface Ordine {
  id_ordine: number;
  id_cliente: number;
  id_fattorino: number;
  data_ora: string;
  stato: string;
  totale: number;
  cliente?: string;
  fattorino?: string;
}
