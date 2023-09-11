<script setup lang="ts">
// fichier: src/views/view01.vue
// controller associé: src/Controller/IndexController.php

// Importe les fonctions ref et computed de Vue.
import { ref, computed } from "vue";

// Importe l'état global de l'application.
import { state } from "../store";

// Importe le composant component01.
import component01 from "../components/component01.vue";

// Initialise une référence Vue pour le message.
const message = ref("");

// Initialise une référence Vue pour le message parsé.
const parsedMessage = ref ({});

// Initialise une référence Vue pour les commentaires filtrés.
const filteredComments = ref([]);

// Initialise une référence Vue pour les réponses filtrées.
const filteredReplies = ref([]);

// Effectue une requête HTTP à la route '/index'.
fetch("/index", {
  headers: {
    // Ajoute le token JWT au header de la requête.
    Authorization: `Bearer ${localStorage.getItem("token")}`,
  },
})
  .then((response) => {
    // Transforme la réponse en JSON.
    return response.json();
  })
  .then((data) => {
    // Stocke le message en tant que chaîne JSON.
    message.value = JSON.stringify(data);

    // Stocke le message parsés.
    parsedMessage.value = data;

    // Met à jour l'état de connexion.
    state.isLoggedIn = data.status === "Success";

    // Met à jour les informations de l'utilisateur.
    state.user = data.user;

    // Met à jour les commentaires filtrés.
    filteredComments.value = data.comments;

    // Filtre et trie les commentaires qui doivent être affihés.
    filteredComments.value = data.comments
        .filter((comment) =>
            comment.parent_id === null &&
            !comment.is_new &&
            comment.flag === "Modéré, accepté" &&
            comment.is_published === true
        )
        .sort((a, b) => new Date(b.published_at.date) - new Date(a.published_at.date));
    
    // Filtre et trie les réponses qui doivent être affichées.
    filteredReplies.value = data.replies
        .filter((reply) =>
            reply.parent_id !== null &&
            !reply.is_new &&
            reply.flag == "Modéré, accepté" &&
            reply.is_published === true
        )
        .sort((a, b) => new Date(b.published_at.date) - new Date(a.published_at.date));
    
  })
  .catch((error) => {
    console.log(error);
  });
</script>

<template>
  <main>
    <section class="section01">
      
      <div class="description">
        <component01 :filtered-comments="filteredComments" :filtered-replies="filteredReplies"></component01>
      </div>

    </section>
  </main>
</template>

<style scoped>
.section01 {
  background-color: white;
  display: flex;
  flex-direction: column;
  aspect-ratio: 16/9;
  height: min(100vh, calc(16vw / 9));
  width: 100%;
  text-align: left;
}

.description {
  background-color: blue;
  width: 100%;
  text-align: left;
}
</style>
