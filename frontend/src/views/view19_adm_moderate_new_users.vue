<script setup lang="ts">
// fichier: src/views/view19_adm_moderate_new_users.vue
// controller associé: src/Controller/ModerateNewUsersController.php

import { ref } from "vue";
import { computed } from "vue";
import { useRouter } from 'vue-router';
import { state } from "../store";

import component02_adm_navbar from "../components/component02_adm_navbar.vue";

// ============================================================================

const router = useRouter();

// ----------------------------------------------------------------------------

const message = ref("");
const parsedMessage = ref ({});

// ----------------------------------------------------------------------------

const errorMessage = ref("");
const errorOccurred = ref(false);

// ----------------------------------------------------------------------------

//
const emit = defineEmits(["update-nav-items"]);

// ----------------------------------------------------------------------------

//
const selectedValues = ref({});

// ============================================================================

// function
const newUsers = computed(() => {
  return parsedMessage.value.areNewUsers || [];
});

// ============================================================================

// function
const goToSommaire = () => {
    router.push({ name: "view11_adm_sommaire" });
  };

// ============================================================================

// function
const showGoToSommaireButton = computed(() => {
  return parsedMessage.value.areNewComments && parsedMessage.value.areNewComments.length === 0;
});

// ============================================================================

// dynamic link to navigate to the new specific user to moderate
const navigateToSpecificUser = (userId) => {
  router.push({ name: "view20_adm_moderate_new_specific_user", params: { userId } });
};

// ============================================================================

// Create a new function to fetch data
const fetchData = async () => {
  try {
    const response = await fetch(`${apiBase}/adm/moderate_new_users`, {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });

    if (!response.ok) {
      throw new Error("Error 01 from view19_adm_moderate_new_users, network response was not ok");
    }
    const data = await response.json();

    if (data.status === "Error, stopped") {
      console.log("Error 02 from view19_adm_moderate_new_users: ", data.status);
      errorOccurred.value = true;
      errorMessage.value = data.message;
    } else {
      console.log("Success 01 from view19_adm_moderate_new_users: ", data.status);
      message.value = JSON.stringify(data);
      parsedMessage.value = data;

      // Update the state object with the fetched user data
      state.isLoggedIn = data.status === "Success";
      state.user = data.user;
    }
  } catch (error) {
    console.log("Error 03 from view19_adm_moderate_new_users: ", error);
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

// ============================================================================
const handleSubmit = async () => {
  // Prepare the data to send to the Symfony controller
  const jsonString = JSON.stringify(selectedValues.value);

  // Send the data to the Symfony controller
  try {
    const response = await fetch(`${apiBase}/adm/moderate_new_users_step2`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
      body: jsonString,
    });

    if (!response.ok) {
      console.log("Error 04 from view19_adm_moderate_new_users: ", response.status, response.statusText);
    } else {
      console.log("Success 02 from view19_adm_moderate_new_users");
      
      //
      const data = await response.json();
      console.log(`Unmanaged users: ${data.unmanagedUsersCount}`);

      if (data.unmanagedUsersCount === 0) {
            router.push({ name: 'view11_adm_sommaire' });
          } else {
            location.reload();
          }
    }

  } catch (error) {
    console.log(error);
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
            Message from view19: An error occurred: {{ errorMessage }}
      </div>
    </section>

<!-- DISPLAY ALL USERS DATAS -->
    <section class = "section04_all_users">
      <h2>All Users, mass moderation:</h2>
      <div class = "all-users-container">
        <form @submit.prevent="handleSubmit">
        <div v-for = "user in newUsers" :key = "user._id" class = "user">
          <a @click="() => navigateToSpecificUser(user._id)">
            <p>ID: {{ user._id }}</p>
          </a>
          <p>Nickname: {{ user.nickname }}</p>

          <br>
          <div>
            <input type="radio" :id="'accept-' + user._id" :name="'user-' + user._id" value="accept" v-model="selectedValues[user._id]" />
            <label :for="'accept-' + user._id">Accept</label>

            <input type="radio" :id="'refuse-' + user._id" :name="'user-' + user._id" value="refuse" v-model="selectedValues[user._id]" />
            <label :for="'refuse-' + user.id">Refuse</label>
          </div>
          <hr>
        </div>
        <button v-if="parsedMessage.areNewUsers && parsedMessage.areNewUsers.length > 0" type="submit">Submit</button>

          <br>
          <br>
          
          <button v-if="showGoToSommaireButton" @click="goToSommaire" type="button">Go to Sommaire</button>
          
        </form>
        <br>
      </div>
    </section>
    

  </main>
</template>

<style scoped>
/*
codes couleurs
lightblue: #add8e6
white snow: #fffafa
lightstellblue: #b0c4de
*/

.section01_connected_user_informations {
  background-color: grey;
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
  align-items: center;
  text-align: left;
}

.section02_section_users {
  background-color: grey;
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
  text-align: left;
  width: 100%;
}

.user-container {
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
  background-color: #808080;
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
  text-align: left;
  padding-left: 1rem;
  border-left: 1px solid black;
  border-right: 1px solid black;
  border-bottom: 1px solid black;
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
