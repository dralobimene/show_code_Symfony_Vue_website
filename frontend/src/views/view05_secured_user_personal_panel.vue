<script setup lang="ts">
// src/views/view05_secured_user_personal_panel.vue
// controller associé: src/Controller/PersonalPanelController.php

import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";

// ============================================================================

const user = ref(null);

// ----------------------------------------------------------------------------

const router = useRouter();

// ============================================================================

// fct° anonyme
onMounted(async () => {
  // retour de la valeur depuis le controller SF
  const response = await fetch("/secured_user/personal_panel", {
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
  });

  const jsonResponse = await response.json();

  if (jsonResponse.status === 'Success') {
    user.value = jsonResponse.user;
  } else {
    console.error('Server returned error:', jsonResponse.message);
  }
});
</script>

<template>
    <main>
        <section class="section01">
          <div class="description">

              <div>
                
                <h2>Your personal panel</h2>
                <br>
                
                <div v-if="user">
                  <p>ID: {{ user.id }}</p>
                  <p>Nickname: {{ user.nickname }}</p>
                  <p>Email: {{ user.email }}</p>
                  <p>Password: {{ user.password }}</p>
                  <p>Roles: {{ user.roles }}</p>
                  <p>Is Verified: {{ user.is_verified }}</p>
                  <p>inscription_date: {{ user.inscription_date }}</p>
                </div>
                <div v-else>
                  <p>An error occured, please contact us. Thank you.</p>
                </div>
              </div>

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
  background-color: lightblue;
  text-align: left;
  padding: 15px;
  margin-bottom: 20px;
  border: 1px solid black;
}
</style>
