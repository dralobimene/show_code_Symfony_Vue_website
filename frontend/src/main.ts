import { createApp } from 'vue';

import App from './App.vue'
import router from './router';
import axios from "axios";
import './style.css';

// Set up axios
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  withCredentials: false,
  headers: {
    Accept: "application/json",
    "Content-Type": "application/json",
  },
});

const app = createApp(App);

app.use(router);
app.provide("$axios", apiClient);
app.mount('#app');
