// src/store.ts
// importe une directive "reactive" pr MAJ la navbar selon
// qu'1 utilisateur est connecté ou pas
import { reactive } from 'vue';

interface State {
  isLoggedIn: boolean;
  user: object | null;
}

export const state: State = reactive({
  isLoggedIn: false,
  user: null,
});
