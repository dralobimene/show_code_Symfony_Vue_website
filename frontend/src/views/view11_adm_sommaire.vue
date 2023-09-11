<script setup lang="ts">
// fichier: src/views/view11_adm_sommaire.vue
// controller associé: src/Controller/AdmSommaireController.php

import { ref } from "vue";
import { state } from "../store";
import component02_adm_navbar from "../components/component02_adm_navbar.vue";

const message = ref("");
const parsedMessage = ref ({});

// pr les messages d'erreur
const errorMessage = ref("");
const errorOccurred = ref(false);

// allow 1 proxy to use every route starting with "adm"
// look for value VITE_API_BASE_URL defined to .env
const apiBase = import.meta.env.VITE_API_BASE_URL;

fetch(`${apiBase}/adm/sommaire`, {
  headers: {
    Authorization: `Bearer ${localStorage.getItem("token")}`,
  },
})
  .then((response) => {
    if (!response.ok) {
      throw new Error("Error 01 from view11_adm_sommaire, network response was not ok");
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
        state.isLoggedIn = data.status === "Success";
        state.user = data.user;

        // console.log('values: ', parsedMessage.value.areNewComments);
        
    }
  })
  .catch((error) => {
    console.log("Error 02 from view11_adm_sommaire.vue while sending data:", error);
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
                :newFilsCount="parsedMessage.commentsWithReplies.filter(fil => fil.containNewReply).length"
                :newRepliesCount="parsedMessage.replies.filter(reply => reply.is_new).length">

        </component02_adm_navbar>

    </div>


        <section class = "section01_connected_user_informations">
          <div v-if = "errorOccurred" class = "error-message">
                Message from view11: An error occurred: {{ errorMessage }}
          </div>
        

          <!-- DISPLAY ONLY CONNECTED USER DATAS -->
          <!--
          <div v-else-if = "parsedMessage.user" class = "user">
            <h2>Connected user datas:</h2>
            <div v-for="(value, key) in parsedMessage.user" :key="key">
                {{ key }}: {{ value }}
            </div>
          </div>
          -->

          <div v-else-if = "parsedMessage.user" class = "user">
            <h2>Explications:</h2>
            <p>
                comments (A, ?B):
                <br>
                comments: Hyperlink, display unmoderated comments
                <br>
                A: total number comments.
                <br>
                ?B: optional, hyperlink, displayed only if some comments not moderated.
            </p>
            <p>
                users: (A, ?B):
                <br>
                users: Hyperlink, display all unmoderated users. Mass moderation
                and links to specific modération.
                <br>
                A: total number users.
                <br>
                ?B: optional, hyperlink, displayed only if some users not moderated.
            </p>
            <p>
                fils: (A, ?B, ?C):
                <br>
                fils: Hyperlink, display comments and unmoderated replies.
                <br>
                A: total number of fils. Fils are comments with their own replies. Must be equal to total number comments.
                <br>
                ?B: optional, displayed only if some replies not moderated.
                <br>
                ?C: optional, already moderated replies
            </p>
            <br>
            <br>
          </div>
          
        </section>
        

        <!-- DISPLAY ONLY COMMENTS, NOT REPLIES -->
        <!--
        <section class = "section02_section_comments">
          <h2>Comments (not replies):</h2>
          <div class = "comment-container">
              <div v-for = "comment in parsedMessage.comments" :key = "comment.id" class = "comment">
                <p>Comment ID: {{ comment.id }}</p>
                <p>Author: {{ comment.author }}</p>
                <hr>
              </div>
          </div>
        </section>
        -->

        <!-- DISPLAY ONLY REPLIES, NOT COMMENTS -->
        <!--
        <section class = "section03_section_replies">
          <h2>replies without comments:</h2>
          <div class = "replies-container">
              <div v-for = "reply in parsedMessage.replies" :key = "reply.id" class = "reply">
                <p>Reply ID: {{ reply.id }}</p>
                <p>Author: {{ reply.author }}</p>
                <hr>
              </div>
          </div>
        </section>
        -->

        <!-- DISPLAY ALL USERS DATAS -->
        <!--
        <section class = "section04_all_users">
          <h2>All Users:</h2>
          <div class = "all-users-container">
            <div v-for = "user in parsedMessage.allUsers" :key = "user.id" class = "user">
              <p>ID: {{ user._id }}</p>
              <p>Nickname: {{ user.nickname }}</p>
              <p>Email: {{ user.email }}</p>
              <hr>
            </div>
          </div>
        </section>
        -->


  </main>
</template>

<style scoped>
/*
codes couleurs
lightblue: #add8e6
white snow: #fffafa
lightstellblue: #b0c4de
*/

.adm_navbar {
    position: sticky;
    bottom: 0;
    left: 0;
    right: 0;
    z-index: 1000;
  }

.section00 {
  background-color: blue;
  display: flex;
  flex-direction: column;
  aspect-ratio: 16/9;
  height: min(100vh, calc(16vw / 9));
  width: 100%;
  text-align: left;
  }

/*
.main_content {
    padding-top: 1rem;
  }
*/

.section01_connected_user_informations {
  background-color: grey;
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
  align-items: center;
  text-align: left;
  border: 1px solid black;
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
