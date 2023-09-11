<script setup lang="ts">
// src/views/view04_connect.vue

import { ref } from "vue";
import { useRouter } from "vue-router";
import { state } from "../store";

const router = useRouter();

const message = ref("");
const usernameOrEmail = ref("");
const password = ref("");

const responseMessage = ref("");

// fonct° anonyme
const formattedResponseMessage = () => {
  if (responseMessage.value) {
    const data = JSON.parse(responseMessage.value);
    let userDetails = '';
    if (data.user) {
    userDetails = `
        User ID: ${data.user.id}<br>
        Nickname: ${data.user.nickname}<br>
        Email: ${data.user.email}<br>
        Roles: ${data.user.roles}<br>
        Password: ${data.user.password}<br>
        is_verified: ${data.user.is_verified}<br>
        token: ${data.user.token}
        `;
    }
    return `Status: ${data.status}<br>
            Message: ${data.message}<br>
            Nickname count: ${data.nicknameCount}<br>
            Email count: ${data.emailCount}<br>
            Username or Email: ${data.usernameOrEmail}<br>
            Password: ${data.password}<br>
            ${userDetails}<br>
            Confirmation: ${data.Confirmation}<br>
            Token: ${data.Token}`;
  } else {
    return '';
  }
};

const submitForm = () => {
  const data = {
    usernameOrEmail: usernameOrEmail.value,
    password: password.value
  };

  fetch("/connect", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    // transforme l'objet data en chaine de caracteres au format json'
    body: JSON.stringify(data)
  })
  .then((response) => {
    return response.json();
  })
  .then((data) => {
    responseMessage.value = JSON.stringify(data);
    if (data.Token) {
      
      // stocker le token ds le local storage
      localStorage.setItem('token', data.Token);
      
      // permet de MAJ la variable definie ds le fichier
      // src/store.ts pr ensuite MAJ les liens concernés qui
      // se trouvent ds la navbar
      state.isLoggedIn = true;
      
      // Redirect the user to ...
      setTimeout(() => {
        if (data.user.roles.includes('ROLE_ADMIN')) {
          router.push({ name: "view11_adm_sommaire" });
        } else if (data.user.roles.includes('ROLE_USER')) {
          router.push({ name: "view01" });
        } else {
          // Handle other cases, if necessary
        }
      }, 3000);
    }
  })
  .catch((error) => {
    console.log(error);
  });
};

</script>

<template>
  <main>
    <section class="section01">
      
      <div class="description">

          <div class="connex_formulaire">
            <form @submit.prevent="submitForm">
                <label for="usernameOrEmail">Please enter your nickname OR your email.</label>
                <br>
                <input type="text" id="usernameOrEmail" v-model="usernameOrEmail">

                <br>
                <br>

                <label for="password">Please enter your password.</label>
                <br>
                <input type="password" id="password" v-model="password">

                <br>
                <br>
                <button type="submit">Submit</button>
            </form>

            <br>

          </div>

          <div class="response-message" v-if="responseMessage" v-html="formattedResponseMessage()"></div>

      </div>

    </section>
  </main>
</template>

<style scoped>

.section01 {
  background-color: lightblue;
  display: flex;
  flex-direction: column;
  aspect-ratio: 16/9;
  height: min(100vh, calc(16vw / 9));
  width: 100%;
  text-align: left;
}

.description {
  background-color: lightblue;
  width: 100%;
  text-align: left;
  padding: 20px;
  margin-bottom: 20px;
  border: 1px solid black;
}

.name {
  background-color: blue;
  width: 100%;
  text-align: left;
}

</style>
