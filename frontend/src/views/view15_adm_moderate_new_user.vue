<script setup lang="ts">
// fichier: src/views/view15_adm_moderate_new_user.vue
// controller associé: src/Controller/ModerateNewUserController.php

import { ref } from "vue";
import { state } from "../store";
import component02_adm_navbar from "../components/component02_adm_navbar.vue";

const message = ref("");
const parsedMessage = ref ({});

const errorMessage = ref("");
const errorOccurred = ref(false);

const emit = defineEmits(["update-nav-items"]);

// ============================================================================

// Create a new function to fetch data
const fetchData = async () => {
  try {
    const response = await fetch(`${apiBase}/adm/moderate_new_user`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });

    if (!response.ok) {
      throw new Error("Error 01 from view15_adm_moderate_new_user, network response was not ok");
    }
    const data = await response.json();

    if (data.status === "Error, stopped") {
      errorOccurred.value = true;
      errorMessage.value = data.message;
    } else {
      message.value = JSON.stringify(data);
      parsedMessage.value = data;

      // Update the state object with the fetched user data
      state.isLoggedIn = data.status === "Success";
      state.user = data.user;
    }
  } catch (error) {
    console.log(error);
  }

  // Emit the 'update-nav-items' event after the form is submitted
  emit("update-nav-items");
};

// ============================================================================

// allow 1 proxy to use every route starting with "adm"
// look for value VITE_API_BASE_URL defined to .env
const apiBase = import.meta.env.VITE_API_BASE_URL;

// Call fetchData() initially to load data
fetchData();

//
const handleSubmitChoiceForUser = async (userId, action) => {
    const response = await fetch(`${apiBase}/adm/moderate_new_user_step2`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
      body: JSON.stringify({ userId, action }),
    });

    if (!response.ok) {
      console.error("Error 02 from view15_adm_moderate_new_user while submitting user ID:", userId);
    } else {
      // console.log("from view15_adm_moderate_new_user: User ID submitted successfully:", userId);

      // Call fetchData() to refresh the data after submitting the form
      fetchData();

      // Emit the 'update-nav-items' event after the form is submitted
      emit("update-nav-items");

    }
  };

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
                :newRepliesCount="parsedMessage.replies.filter(reply => reply.isNew).length">

        </component02_adm_navbar>
        
    </div>

    <section class = "section01_connected_user_informations">
      
      <div v-if = "errorOccurred" class = "error-message">
            Message from view15: An error occurred: {{ errorMessage }}
      </div>
    

      <!-- DISPLAY ONLY CONNECTED USER DATAS -->
      <!--
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
        <br>
        inscriptionDate: {{ parsedMessage.user.inscriptionDate }}
        <br>
        is_new: {{ parsedMessage.user.is_new }}
      </div>
      -->
    </section>

    <!-- DISPLAY ONLY COMMENTS, NOT REPLIES -->
    <!--
    <section class = "section02_section_comments">
      <h2>Comments (not replies):</h2>
      <div class = "comment_container">
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
      <div class = "replies_container">
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
      <div class = "all_users_container">
        <div v-for = "user in parsedMessage.allUsers" :key = "user.id" class = "user">
          <p>ID: {{ user._id }}</p>
          <p>Nickname: {{ user.nickname }}</p>
          <p>Email: {{ user.email }}</p>
          <p>Inscription date: {{ user.inscriptionDate }}</p>
          <p>is_new: {{ user.is_new }}</p>
          <hr>
        </div>
      </div>
    </section>
    -->

    <!-- DISPLAY ALL NEW USERS DATAS -->
    <section class = "section05_new_users">
      <h2>NEW Users:</h2>
      <div class = "new_users_container">
        <div v-for = "newuser in parsedMessage.areNewUsers" :key = "newuser.id" class = "newuser">
          <p>ID: {{ newuser._id }}</p>
          <p>Nickname: {{ newuser.nickname }}</p>
          <p>Email: {{ newuser.email }}</p>
          <p>Inscription date: {{ newuser.inscriptionDate }}</p>
          <p>is_new: {{ newuser.is_new }}</p>

          <form @submit.prevent="handleSubmitChoiceForUser(newuser._id, 'accept')">
                <button type="submit">Accepter le user</button>
          </form>
                <br>
          <form @submit.prevent="handleSubmitChoiceForUser(newuser._id, 'refuse')">
                <button type="submit">Refuse this user</button>
          </form>
          <hr>
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

.comment_container {
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

.reply_container {
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

.all_users_container {
  padding-left: 1rem;
}

.section05_new_users {
  background-color: grey;
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
  text-align: left;
  width: 100%;
}

.new_users_container {
  padding-left: 1rem;
}

</style>
