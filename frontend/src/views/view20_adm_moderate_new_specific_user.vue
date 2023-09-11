<script setup lang="ts">
// fichier: src/Controller/ModerateNewSpecificUserController {userId}
// vue associée: src/views/view20_adm_moderate_new_specific_user.vue

import { ref } from "vue";
import { useRouter } from "vue-router";

import component02_adm_navbar from "../components/component02_adm_navbar.vue";

// ============================================================================

//
const router = useRouter();

// ----------------------------------------------------------------------------

//
const message = ref("");

// ----------------------------------------------------------------------------

// parsedMessage est une référence à un objet
// Les propriétés de parsedMessage sont déterminées par la structure de l'objet qui lui est assigné
const parsedMessage = ref ({});
/*
Ajoutez des propriétés à parsedMessage et assignez-leur des valeurs dynamiquement
en fonction de la logique de votre application. Par exemple, vous pouvez définir des propriétés
comme user, comment, and replies:
Exemple:
parsedMessage.value = {
  user: { name: 'John', age: 30 },
  comment: { text: 'This is a comment' },
  replies: [{ id: 1, text: 'Reply 1' }, { id: 2, text: 'Reply 2' }],
};
*/

// ----------------------------------------------------------------------------

// Crée une nouvelle référence appelée areNewUsers et assigne la valeur
// de parsedMessage.value.areNewUsers à celle-ci
const areNewUsers = ref([]);

// ----------------------------------------------------------------------------
// Crée une nouvelle référence appelée specificUser et l'initialise à un objet vide
const specificUser = ref({});

// ----------------------------------------------------------------------------

// Extrait la valeur du paramètre userId de la route actuelle, permettant
// de l'utiliser dans le composant pour accéder ou manipuler des données
// en fonction de l'ID utilisateur actuel
const userId = router.currentRoute.value.params.userId;

// ----------------------------------------------------------------------------

//
const action = ref("");

// ----------------------------------------------------------------------------

// Autorise 1 proxy à utiliser chaque route commençant par "adm"
// Cherche la valeur VITE_API_BASE_URL définie dans .env
const apiBase = import.meta.env.VITE_API_BASE_URL;

// ============================================================================

// Crée une nouvelle fonction pour récupérer des données
const fetchData = async () => {
  try {
    const response = await fetch(`${apiBase}/adm/moderate_new_specific_user/${userId}`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });

    if (!response.ok) {
      throw new Error("Error 04 from view20_adm_moderate_new_specific_user, network response was not ok");
    }
    const data = await response.json();

    if (data.status === "Error, stopped") {
      console.log("Error 06 from view20_adm_moderate_new_specific_user: ", data.message);
      errorOccurred.value = true;
      errorMessage.value = data.message;
    } else {
      console.log("Success 02 from view20_adm_moderate_new_specific_user: ", data.message);
      message.value = JSON.stringify(data);
      parsedMessage.value = data;

      // Trouve l'utilisateur spécifique dans le tableau areNewUsers en utilisant l'userId
      specificUser.value = data.areNewUsers.find(user => user._id === userId);

    }
  } catch (error) {
    console.log("Error 07 from view20_adm_moderate_new_specific_user:", error);
  }

};

// ============================================================================
// Appelle fetchData() initialement pour charger les données
fetchData();

// ============================================================================

// Ajoute la méthode handleSubmitChoiceForUser
const handleSubmitChoiceForUser = async (UserId, action) => {
  try {
    const response = await fetch(`${apiBase}/adm/moderate_new_specific_user_step2`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
      body: JSON.stringify({ userId, action }),
    });

    if (!response.ok) {
      throw new Error("Error 03 from view20_adm_moderate_new_specific_user, network response was not ok");
    }
    const data = await response.json();

    if (data.status === "Success") {
      console.log("Success 01 from view20_adm_moderate_new_specific_user: ", data.message);
      router.push({ name: 'view11_adm_sommaire' });
      
      fetchData();
    } else {
      console.error("Error 01 from view20_adm_moderate_new_specific_user", data.message);
    }
  } catch (error) {
    console.log("Error 02 from view20_adm_moderate_new_specific_user", error);
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

    <section class="section01">
      <div class="description">
        <h2>User Details</h2>
        <div v-if="specificUser && specificUser._id">
          <h3>Id: {{ specificUser._id }}</h3>
          <h3>nickname: {{ specificUser.nickname }}</h3>
          <h3>Email: {{ specificUser.email }}</h3>
          <h3>password: {{ specificUser.password }}</h3>
          <h3>is_verified: {{ specificUser.is_verified }}</h3>
          <h3>Roles: {{ specificUser.roles }}</h3>
          <h3>is_new: {{ specificUser.is_new }}</h3>
          <h3>Inscription date: {{ specificUser.inscriptionDate }}</h3>
          
          <br>
        
          <form v-if="specificUser.is_new"
              @submit.prevent="handleSubmitChoiceForUser(specificUser.id, 'accept')">
              <button type="submit">Accept this User</button>
          </form>
          <br v-if="specificUser.is_new">
          
          <form v-if="specificUser.is_new"
              @submit.prevent="handleSubmitChoiceForUser(specificUser.id, 'refuse')">
              <button type="submit">Refuse this user</button>
          </form>

        </div>
        <div v-else>
          <p>No user data found.</p>
        </div>
      </div>
    </section>
  </main>
</template>

<style scoped>
/*
codes couleurs
#0fc0fc =
lightblue: #add8e6
white snow: #fffafa
lightsteelblue: #b0c4de
grey: #808080
*/

.section01 {
  background-color: #fffafa;
  display: flex;
  flex-direction: column;
  aspect-ratio: 16/9;
  height: min(100vh, calc(16vw / 9));
  width: 96%;
  text-align: left;
}

.description {
  background-color: #b0c4de;
  width: 100%;
  text-align: left;
  padding: 20px;
  margin-bottom: 20px;
  border: 1px solid black;
}

</style>
