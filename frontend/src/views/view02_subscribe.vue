<script setup lang="ts">
// src/views/view02_subscribe.vue
// controller: src/Controller/subscribeController.php

import { ref } from "vue";
import { useRouter } from 'vue-router';
import { state } from "../store";
import axios from "axios";

const router = useRouter();

const nickname = ref("");
const email = ref("");
const password = ref("");
const message = ref("");
const isSubmitted = ref(false);

// ============================================================================

const submitForm = async () => {
  try {
    const response = await axios.post(import.meta.env.VITE_API_BASE_URL + "/subscribe", {
      nickname: nickname.value,
      email: email.value,
      password: password.value,
    });

    if (response.data.valid) {

      //
      message.value = response.data.message;

      //
      isSubmitted.value = true;

      // permet de MAJ la variable definie ds le fichier
      // src/store.ts pr ensuite MAJ le lien concerné qui
      // se trouve ds la navbar
      state.isLoggedIn = true;

      //
      setTimeout(() => {
        router.push('/view04_connect');
      }, 1000);

    } else {
      message.value = response.data.message;
    }
  } catch (error) {
    console.error("Error 01 from view02_subscribe.vue while sending data:", error);
  }
};
</script>

<template>
  <div class="subscribe">
    <h2>Subscribe</h2>
    <form @submit.prevent="submitForm">
      <div>
        <input
          v-model="nickname"
          type="text"
          placeholder="Enter a nickname"
        />
        Nickname must contain at least 1 letter, and may contain digits and 3 special characters (@, -, _).
        <br>
        Length: min = 3, max = 20.
      </div>

      <br>

      <div>
        <input
          v-model="email"
          type="email"
          placeholder="Enter your email"
        />
        Email classic validation.
      </div>

      <br>

      <div>
        <input
          v-model="password"
          type="password"
          placeholder="Enter your password"
        />
        Password must contain at least 1 digit, 1 uppercase letter, and 1 special character (either @, -, or _).
        <br>
        Length: min = 10, max = 20.
      </div>

      <br>

      <div v-if="message">
        <p>{{ message }}</p>
      </div>
      
      <button v-if="!isSubmitted" type="submit">Submit</button>
    </form>
  </div>
</template>

<style scoped>
.subscribe {
  background-color: grey;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 2rem;
  box-sizing: border-box;
  text-align: left;
  border: 1px solid black;
}

form {
  width: 100%;
  height: 40vh;
}

input {
  display: block;
  margin-bottom: 10px;
  width: 100%;
}
</style>
