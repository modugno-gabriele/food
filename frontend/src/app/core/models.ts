export interface Categoria {
  id_categoria: number;
  nome: string;
  descrizione?: string;
}

export interface Ristorante {
  id_ristorante: number;
  id_categoria: number;
  nome: string;
  indirizzo?: string;
  telefono?: string;
  categoria?: string;
  media_voto?: number;
  num_recensioni?: number;
}

export interface Piatto {
  id_piatto: number;
  id_ristorante: number;
  nome: string;
  prezzo: number;
  disponibile: boolean;
  ristorante?: string;
}

export interface Ingrediente {
  id_ingrediente: number;
  nome: string;
  allergenico: boolean;
}

export interface Cliente {
  id_cliente: number;
  nome: string;
  cognome: string;
  email?: string;
  ind_consegna?: string;
}

export interface Ordine {
  id_ordine: number;
  id_cliente: number;
  id_fattorino?: number;
  data_ora: string;
  stato: string;
  totale: number;
  cliente?: string;
  fattorino?: string;
}

export interface DettaglioOrdine {
  id_ordine: number;
  id_piatto: number;
  quantita: number;
  prez_unit: number;
  piatto?: string;
}

export interface Fattorino {
  id_fattorino: number;
  nome: string;
  mezzo?: string;
  disponibile: boolean;
}

export interface Recensione {
  id_recensione: number;
  id_cliente: number;
  id_ristorante: number;
  data: string;
  commento?: string;
  voto: number;
  cliente?: string;
  ristorante?: string;
}