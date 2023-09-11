<script setup lang="ts">
// fichier: src/components/component01.vue

import { ref, inject, defineProps, watchEffect } from "vue";

// ----------------------------------------------------------------------------

// Définit les props que ce composant attend.
const props = defineProps({
  filteredComments: Array,
  filteredReplies: Array,
});

// Initialise une référence Vue pour les réponses affichées.
const displayedComments = ref(props.filteredComments);

// declare 1 json vide
const user = ref({});

//
const isLoggedIn = inject('isLoggedIn');

// declare 1 tableau vide
const replies = ref([]);

// ----------------------------------------------------------------------------

// Met à jour les réponses affichées chaque fois que les props changent.
watchEffect(() => {
  displayedComments.value = props.filteredComments;
  replies.value = props.filteredReplies;
});

// ----------------------------------------------------------------------------

// Définit une méthode pour obtenir les réponses à un commentaire.
const getReplies = (id) => {
  return replies.value.filter((reply) => reply.parent_id === id);
};

// ============================================================================

// Définit une méthode pour basculer l'affichage des réponses à un commentaire.
const toggleReplies = (id) => {
  const comment = displayedComments.value.find((comment) => comment.id === id);
  if (comment) {
    comment.showReplies = !comment.showReplies;
  }
};

</script>

<template>
  <div>

    <!--
    <h2>Filtered Comments</h2>
    -->
    
    <div v-for="comment in displayedComments" :key="comment.id" class="comment">
      <h3>title: {{ comment.title }}</h3>
      <!--
      <p>_id: {{ comment.id }}</p>
      -->
      <p>author: {{ comment.author }}</p>
      <p>category: {{ comment.category }}</p>
      <p>content: {{ comment.content }}</p>
      
      <p>created_at: {{ comment.created_at }}</p>
      <p>flag: {{ comment.flag }}</p>
      <p>is_published: {{ comment.is_published }}</p>
      <p>parent_id: {{ comment.parent_id }}</p>
      <p>is_new: {{ comment.is_new }}</p>
      <p>published_at: {{ comment.published_at }}</p>
      

      <div v-if="comment.parent_id === null && isLoggedIn">
        <router-link :to="{ name: 'view09_reply_user_post', params: { p_id: comment.id } }">
          <button>Reply</button>
        </router-link>
      </div>

      <br>
      <br>

      <div class="replies">
        <div v-for="reply in getReplies(comment.id)" :key="reply.id" class="reply">
          <h4>title: {{ reply.title }}</h4>
          <p>author: {{ reply.author }}</p>
          <p>category: {{ reply.category }}</p>
          <p>content: {{ reply.content }}</p>
          
          <p>created_at: {{ reply.created_at }}</p>
          <p>flag: {{ reply.flag }}</p>
          <p>is_published: {{ reply.is_published }}</p>
          <p>parent_id: {{ reply.parent_id }}</p>
          <p>is_new: {{ reply.is_new }}</p>
          <p>published_at: {{ reply.published_at }}</p>
          
        </div>
      </div>

    </div>

  </div>
</template>

<style scoped>

/* RDC */
.comment {
  background-color: lightblue;
  padding: 20px;
  margin-bottom: 20px;
  border: 1px solid black;
}

.replies {

}

.reply {
  background-color: lightgray;
  padding: 10px;
  margin-bottom: 10px;
  margin-left: 20px;
  border: 1px solid black;
}
</style>
