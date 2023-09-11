<script setup lang="ts">
// fichier: src/Controller/ModerateNewSpecifificReplyController {filId}
// vue associée: src/views/view22_adm_moderate_new_specific_reply

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

// objet
// Les propriétés de parsedMessage sont déterminées par la structure de l'objet qui lui est assigné
const parsedMessage = ref ({});
/*
ajoute des propriétés à parsedMessage et leur attribue des valeurs de 
manière dynamique en fonction de la logique de votre application. 
Par exemple, vous pouvez définir des propriétés 
comme user, comment, et replies :
Exemple:
parsedMessage.value = {
  user: { name: 'John', age: 30 },
  comment: { text: 'This is a comment' },
  replies: [{ id: 1, text: 'Reply 1' }, { id: 2, text: 'Reply 2' }],
};
*/

// ----------------------------------------------------------------------------

// créer une nouvelle référence appelée commentsWithReplies et lui 
// attribuer la valeur de parsedMessage.value.commentsWithReplies
const commentsWithReplies = ref([]);

// ----------------------------------------------------------------------------

// Crée une nouvelle référence appelée specificComment et l'initialise à null
// doit représenter 1 fil de discussion
const specificComment = ref(null);

// ----------------------------------------------------------------------------
// extrait la valeur du paramètre userId de la route actuelle, permettant
// de l'utiliser dans le composant pour accéder ou manipuler des données 
// en fonction de l'ID de l'utilisateur actuel
const filId = router.currentRoute.value.params.filId;

// ----------------------------------------------------------------------------

//
const action = ref("");

// ----------------------------------------------------------------------------

const errorMessage = ref("");
const errorOccurred = ref(false);

// ----------------------------------------------------------------------------

// permet à 1 proxy d'utiliser toutes les routes commençant par "adm"
// cherche la valeur VITE_API_BASE_URL définie dans .env
const apiBase = import.meta.env.VITE_API_BASE_URL;

// ============================================================================

// Crée une nouvelle fonction pour récupérer les données
const fetchData = async () => {
  try {
    const response = await fetch(`${apiBase}/adm/moderate_new_specific_reply/${filId}`, {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });

    if (!response.ok) {
      throw new Error("Error 04 from view20_adm_moderate_new_specific_user, network response was not ok");
    }
    const data = await response.json();

    if (data.status === "Error, stopped") {
      // console.log("Error 06 from view20_adm_moderate_new_specific_user: ", data.message);
      errorOccurred.value = true;
      errorMessage.value = data.message;
    } else {
      console.log("Success 02 from view20_adm_moderate_new_specific_user: ", data.message);
      message.value = JSON.stringify(data);
      parsedMessage.value = data;

      /*
      console.log("data: ", data);
      console.log("API response: ", data);
      console.log("parsedMessage.value: ", parsedMessage.value);
      console.log("filId: ", filId);
      console.log("commentsWithReplies: ", parsedMessage.value.commentsWithReplies);
      */

      // Trouver le commentaire spécifique dans le tableau commentsWithReplies
      // en utilisant le filId
      specificComment.value = parsedMessage.value.commentsWithReplies.find(comment => comment.comment.id === filId);

      // console.log("specificComment.value: ", specificComment.value);

    }
  } catch (error) {
    console.log("Error 07 from view20_adm_moderate_new_specific_user:", error);
  }

};

// ============================================================================

// Call fetchData() initially to load data
fetchData();

// ============================================================================

// Add the handleSubmitChoiceForUser method
const handleSubmitChoiceForReply = async (filId, action) => {
    try {
        const response = await fetch(`${apiBase}/adm/moderate_new_specific_reply_step2`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
          body: JSON.stringify({ filId, action }),
        });

        if (!response.ok) {
          throw new Error("Error 03 from view22_adm_moderate_new_specific_reply, network response was not ok");
        }
        const data = await response.json();

        if (data.status === "Success") {
          console.log("Success 01 from view22_adm_moderate_new_specific_reply: ", data.message);
          
          fetchData();
        } else {
          console.error("Error 01 from view22_adm_moderate_new_specific_reply", data.message);
        }
      } catch (error) {
        console.log("Error 02 from view22_adm_moderate_new_specific_reply", error);
  }
}

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
 
      <div v-if="specificComment">
       
       <br>

        <div class="comment-section">
          <h2>Comment</h2>

          <p><strong>Id:</strong> {{ specificComment.comment.id }}</p>
          <p><strong>Author:</strong> {{ specificComment.comment.author }}</p>
          <p><strong>Title:</strong> {{ specificComment.comment.title }}</p>
          <p><strong>Text:</strong> {{ specificComment.comment.content }}</p>
          <p><strong>Category:</strong> {{ specificComment.comment.category }}</p>
          <p><strong>Flag:</strong> {{ specificComment.comment.flag }}</p>
          <p><strong>is_published:</strong> {{ specificComment.comment.is_published }}</p>
          <p><strong>Created_at:</strong> {{ specificComment.comment.created_at }}</p>
          <p><strong>parent_id:</strong> {{ specificComment.comment.parent_id }}</p>
          <p><strong>is_new:</strong> {{ specificComment.comment.is_new }}</p>
          <p><strong>published_at:</strong> {{ specificComment.comment.published_at }}</p>
        </div>

        <br>

        <div class="replies-section" v-if="specificComment.replies && specificComment.replies.length > 0">
          
          <h2>Replies</h2>

          <div v-for="(reply, index) in specificComment.replies" :key="index">
            <hr>
            <p><strong>Reply Id:</strong> {{ reply.id }}</p>
            <p><strong>Reply Author:</strong> {{ reply.author }}</p>
            <p><strong>Reply title:</strong> {{ reply.title }}</p>
            <p><strong>Reply Content:</strong> {{ reply.content }}</p>
            <p><strong>Reply Category:</strong> {{ reply.category }}</p>
            <p><strong>Reply Flag:</strong> {{ reply.flag }}</p>
            <p><strong>Reply is_published:</strong> {{ reply.is_published }}</p>
            <p><strong>Reply created_at:</strong> {{ reply.created_at }}</p>
            <p><strong>Reply parent_id:</strong> {{ reply.parent_id }}</p>
            <p><strong>Reply is_new:</strong> {{ reply.is_new }}</p>

            <br>

            <form v-if="reply.is_new"
              @submit.prevent="handleSubmitChoiceForReply(reply.id, 'accept')">
              <button type="submit">Accept this Reply</button>
            </form>
            <br v-if="reply.is_new">
          
            <form v-if="reply.is_new"
              @submit.prevent="handleSubmitChoiceForReply(reply.id, 'refuse')">
              <button type="submit">Refuse this Reply</button>
            </form>

            <hr>
          </div>

        </div>

        <br>
          
        <div class="information">

            <div v-if="specificComment.containNewReply">
              <p>This comment contains a new reply!</p>
            </div>
      
          <div v-else>
            <p>No new reply found.</p>
          </div>
        
        </div>

        <br>
      
      </div>
      </section>
  </main>
</template>



<style scoped>
/*
code couleurs
#0fc0fc =
lightblue: #add8e6
white snow: #fffafa
lightsteelblue: #b0c4de
grey: #808080
*/

.section01 {
  background-color: grey;
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
  align-items: center;
  text-align: left;
  border: 1px solid black;
}

.comment-section {
    background-color: #add8e6;
    border: 1px solid black;
    display: flex;
    flex-direction: column;
    flex-wrap: wrap;
    text-align: left;
    padding-left: 1rem;
}

.replies-section {
    background-color: #add8e6;
    border: 1px solid black;
    display: flex;
    flex-direction: column;
    flex-wrap: wrap;
    text-align: left;
    padding-left: 1rem;
}

.information {
    background-color: #add8e6;
    border: 1px solid black;
    display: flex;
    flex-direction: column;
    flex-wrap: wrap;
    text-align: left;
    padding-left: 1rem;
}
</style>
