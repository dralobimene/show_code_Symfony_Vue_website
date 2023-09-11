<script setup lang="ts">
// fichier: src/views/view13_adm_delete_user.vue
// controller associé: src/Controller/DeleteUserController.php

import { ref } from "vue";
import { state } from "../store";
import component02_adm_navbar from "../components/component02_adm_navbar.vue";

const message = ref("");
const parsedMessage = ref ({});

const errorMessage = ref("");
const errorOccurred = ref(false);

// allow 1 proxy to use every route starting with "adm"
// look for value VITE_API_BASE_URL defined to .env
const apiBase = import.meta.env.VITE_API_BASE_URL;

fetch(`${apiBase}/adm/delete_user`, {
  headers: {
    Authorization: `Bearer ${localStorage.getItem("token")}`,
  },
})
  .then((response) => {
    if (!response.ok) {
      throw new Error("Error 01 from view13_adm_delete_user, network response was not ok");
    }
    return response.json();
  })
  .then((data) => {
    if (data.status === 'Error, stopped') {
        errorOccurred.value = true;
        errorMessage.value = data.message;
    } else {
        message.value = JSON.stringify(data);
        parsedMessage.value = data;

        // Update the state object with the fetched user data
        // permet de savoir si 1 utilisateur est loggué
        // on affiche son nickname et son roles
        state.isLoggedIn = data.status === "Success";
        state.user = data.user;
        
    }
  })
  .catch((error) => {
    console.log("Error 02 from view13_adm_delete_user: ", error);
    errorMessage.value = error.message;
  });
</script>

<template>
  <main>

    <div class = "adm_navbar">
        <!-- allow to communicate datas to component02 -->
        
        <component02_adm_navbar
            v-if = "parsedMessage.user && parsedMessage.comments && parsedMessage.replies"
                :userData = "parsedMessage.user"
                :usersCount = "parsedMessage.allUsers.length"
                :newUsersCount="parsedMessage.areNewUsers.length"
                :commentsCount = "parsedMessage.comments.length"
                :newCommentsCount="parsedMessage.areNewComments.length"
                :repliesCount = "parsedMessage.replies.length"
                :filsCount = "parsedMessage.commentsWithReplies.length"
                :newFilsCount="parsedMessage.commentsWithReplies.filter(fil => fil.containNewReply).length">

        </component02_adm_navbar>
        <!--
        <component02_adm_navbar></component02_adm_navbar>
        -->
    </div>

    <section class = "section01_connected_user_informations">
      
      <div v-if = "errorOccurred" class = "error-message">
            Message from view13: An error occurred: {{ errorMessage }}
      </div>
    

      <!-- DISPLAY ONLY CONNECTED USER DATAS -->
      <div v-else-if = "parsedMessage.user" class = "user">
        <h2>Connected user datas:</h2>
        token: {{ parsedMessage.user.token }}
        <br>
        id: {{ parsedMessage.user.id }}
        <br>
        nickname: {{ parsedMessage.user.nickname }}
        <br>
        email: {{ parsedMessage.user.email }}
        <br>
        password: {{ parsedMessage.user.password }}
        <br>
        roles: {{ parsedMessage.user.roles }}
        <br>
        is_verified: {{ parsedMessage.user.is_verified }}
      </div>

    </section>

    <!-- DISPLAY ONLY COMMENTS, NOT REPLIES -->
    <section class = "section02_section_comments">
      <h2>Comments (not replies):</h2>
      <div class = "comment-container">
          <div v-for = "comment in parsedMessage.comments" :key = "comment.id" class = "comment">
            <p>Comment ID: {{ comment.id }}</p>
            <p>Author: {{ comment.author }}</p>
            <hr>
            <!-- Add any other properties you'd like to display -->
          </div>
      </div>
    </section>

    <!-- DISPLAY ONLY REPLIES, NOT COMMENTS -->
    <section class = "section03_section_replies">
      <h2>replies without comments:</h2>
      <div class = "replies-container">
          <div v-for = "reply in parsedMessage.replies" :key = "reply.id" class = "reply">
            <p>Reply ID: {{ reply.id }}</p>
            <p>Author: {{ reply.author }}</p>
            <hr>
            <!-- Add any other properties you'd like to display -->
          </div>
      </div>
    </section>

    <!-- DISPLAY ALL USERS DATAS -->
    <section class = "section04_all_users">
          <h2>All Users:</h2>
          <div class = "all-users-container">
            <div v-for = "user in parsedMessage.allUsers" :key = "user.id" class = "user">
              <p>ID: {{ user._id }}</p>
              <p>Nickname: {{ user.nickname }}</p>
              <p>Email: {{ user.email }}</p>
              <hr>
              <!-- Add any other properties you'd like to display -->
            </div>
          </div>
        </section>

  </main>
</template>

<style scoped>

.section01_connected_user_informations {
  background-color: grey;
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
  align-items: center;
  text-align: left;
}

.section02_section_comments {
  background-color: grey;
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
  text-align: left;
  width: 100%;
}

.comment-container {
  padding-left: 1rem;
}

.section03_section_replies {
  background-color: grey;
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
  text-align: left;
  width: 100%;
}

.reply-container {
  padding-left: 1rem;
}

.section04_all_users {
  background-color: grey;
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
  text-align: left;
  width: 100%;
}

.all-users-container {
  padding-left: 1rem;
}

</style>
