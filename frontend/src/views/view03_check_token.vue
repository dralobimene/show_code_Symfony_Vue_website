<script setup lang="ts">
// fichier: src/views:view03_check_token.vue
// controller associé: ???

import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";

const message = ref(null);
const route = useRoute();

onMounted(async () => {
  const token = route.params.token;
  console.log('Token:', token);

  try {
    const response = await fetch(`/check_token/${token}`);
    console.log('Response:', response);

    if (response.ok) {
      message.value = await response.json();
      console.log('Message:', message.value);
    } else {
      console.error("Erreur lors de la vérification du token");
    }
  } catch (error) {
    console.error(error);
  }
});
</script>

<template>
  <div class="message_content">
    <h1 v-if="message">{{ message.message }}</h1>
    <h1 v-else>Chargement du message...</h1>
  </div>
</template>

<style scoped>
.message_content {
  background-color: green;
  display: flex;
  flex-direction: column;
  aspect-ratio: 16/9;
  height: min(100vh, calc(16vw / 9));
  width: 100%;
  text-align: left;
}
</style>
