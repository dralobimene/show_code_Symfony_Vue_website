<script>
// fichier: src/VIEWS/view07_approve.vue

import axios from 'axios';

export default {
  // definit une propriete 'token'
  props: {
    token: {
      type: String,
      required: true,
    },
  },
  // retourne des données pr suivre si la requete axios
  // est en cours d'execution ou non
  data() {
    return {
      loading: true,
      success: false,
      successMessage: 'Account activated successfully.',
      errorMessage: 'Failed to activate account.',
    };
  },
  // methode executee lorsque le composant est crée (affiché)
  // envoie 1 requete GET
  async created() {
    try {
      const response = await axios.get(`https://localhost:8000/approve/${this.token}`);
      if (response.status === 200) {
        this.success = true;
      }
    } catch (error) {
      this.errorMessage = error.response?.data?.error || this.errorMessage;
    } finally {
      this.loading = false;
    }
  },
};
</script>

<template>
  <div>
    <h1>Account Activation</h1>
    <div v-if="loading">
      <p>Loading...</p>
    </div>
    <div v-else>
      <p v-if="success">{{ successMessage }}</p>
      <p v-else>{{ errorMessage }}</p>
    </div>
  </div>
</template>
