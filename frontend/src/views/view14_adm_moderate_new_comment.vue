<script setup lang="ts">
// fichier: src/views/view14_adm_moderate_new_comment.vue
// controller associé: src/Controller/ModerateNewCommentController.php

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
    const response = await fetch(`${apiBase}/adm/moderate_new_comment`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });

    if (!response.ok) {
      throw new Error("Error 01 from view14_adm_moderate_new_comment, network response was not ok");
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

  // emettre l'event 'update-nav-items' apres que le formulaire ait ete sousmis
  emit("update-nav-items");
};

// ============================================================================

// permet à 1 proxy d'utiliser toutes les routes commençant par "adm"
// cherche la valeur VITE_API_BASE_URL définie dans .env
const apiBase = import.meta.env.VITE_API_BASE_URL;

// Call fetchData() initially to load data
fetchData();

// ============================================================================

// method to handle submit button click
const handleSubmitChoice = async (commentId, action) => {
    const response = await fetch(`${apiBase}/adm/moderate_new_comment_step2`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
      body: JSON.stringify({ commentId, action }),
    });

    if (!response.ok) {
      console.error("Error 02 from view14_adm_moderate_new_comment, submitting comment ID:", commentId);
    } else {
      // console.log("from view14_adm_moderate_new_comment: Comment ID submitted successfully:", commentId);

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
            Message from view14: An error occurred: {{ errorMessage }}
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
      <div class = "comment-container">
          <div v-for = "comment in parsedMessage.comments" :key = "comment.id" class = "comment">
            <p>Comment ID: {{ comment.id }}</p>
            <p>Author: {{ comment.author }}</p>
            <p>Title: {{ comment.title }}</p>
            <p>category: {{ comment.category }}</p>
            <p>Content: {{ comment.content }}</p>
            <p>Created_at: {{ comment.created_at }}</p>
            <p>Flag: {{ comment.flag }}</p>
            <p>is_published: {{ comment.is_published }}</p>
            <p>Parent_id: {{ comment.parent_id }}</p>
            <p>is_new: {{ comment.is_new }}</p>
            <hr>
          </div>
      </div>
    </section>
    -->

    <!-- DISPLAY ONLY NEW COMMENTS, NOT REPLIES -->
    <section class = "section05_new_comments">
      <h2>Comments (not replies):</h2>
      <div class = "new_comments_container">
          <div v-for = "new_comment in parsedMessage.areNewComments" :key = "new_comment.id" class = "new_comment">
            <p>Comment ID: {{ new_comment.id }}</p>
            <p>Author: {{ new_comment.author }}</p>
            <p>Title: {{ new_comment.title }}</p>
            <p>category: {{ new_comment.category }}</p>
            <p>Content: {{ new_comment.content }}</p>
            <p>Created_at: {{ new_comment.created_at }}</p>
            <p>Flag: {{ new_comment.flag }}</p>
            <p>is_published: {{ new_comment.is_published }}</p>
            <p>Parent_id: {{ new_comment.parent_id }}</p>
            <p>is_new: {{ new_comment.is_new }}</p>
            
            <form @submit.prevent="handleSubmitChoice(new_comment.id, 'accept')">
                <button type="submit">Accepter le commentaire</button>
            </form>
            <br>
            <form @submit.prevent="handleSubmitChoice(new_comment.id, 'refuse')">
                <button type="submit">Refuse this comment</button>
            </form>

            <hr>
          </div>
      </div>
    </section>

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
          <p>Inscription date: {{ user.inscriptionDate }}</p>
          <p>is_new: {{ user.is_new }}</p>
          <hr>
        </div>
      </div>
    </section>
    -->

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

.section05_new_comments {
  background-color: grey;
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
  text-align: left;
  width: 100%;
}

.new_comments_container {
  padding-left: 1rem;
}

</style>
