<script setup lang="ts">
// src/views/view06_logout.vue
// controller associé: src/Controller/LogoutController.php

import { ref } from "vue";
import { useRouter } from "vue-router";
import { state } from "../store";

// ============================================================================

const router = useRouter();

// ============================================================================

const message = ref("");
const parsedMessage = ref ({});

// ============================================================================

// permet la redirection vers view 01 si l'utilisateur
// arrive sur cette page directement depuis la barre d'adresse
// sans token de connection
fetch("/logout", {
  method: "GET",
  headers: {
    "Content-Type": "application/json",
    Authorization: `Bearer ${localStorage.getItem("token")}`,
  },
})
  .then((response) => {
    if (!response.ok) {
      throw new Error(response.statusText);
    }
    return response.json();
  })
  .then((data) => {
    message.value = JSON.stringify(data);
    parsedMessage.value = data;

  })
  .catch((error) => {
    if (error.message.includes('Forbidden')) {
      router.push({ name: 'view01' });
    } else {
      console.log("Error 02 from view06_logout: ",error);
    }
  });

// ============================================================================

// function to handle submit
const handleLogout = async () => {
  try {
    // Send a request to the /logout endpoint to clear the token cookie
    const response = await fetch("/logout", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });

    if (!response.ok) {
      console.log("L'utilisateur est arrivé sur cette page d'1 maniere détournée.");
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    // Handle success, e.g., display a success message or redirect

    // Remove the token cookie from local storage
    localStorage.removeItem("token");
    
    // permet de MAJ la variable definie ds le fichier
    // src/store.ts pr ensuite MAJ le lien concerné qui
    // se trouve ds la navbar
    state.isLoggedIn = false;

    // Redirect the user to the login page
    router.push({ name: "view01" });
  } catch (error) {
    console.error("Error logging out: ", error);
  }
};

</script>

<template>
  <main>
    <section class="section01">
      
      <div class="description">
        <h2>Logout</h2>
        <p>Are you sure you want to log out?</p>
        <button @click="handleLogout">Logout</button>
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
