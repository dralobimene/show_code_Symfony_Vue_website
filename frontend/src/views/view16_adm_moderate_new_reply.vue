<script setup lang="ts">
// fichier: src/views/view16_adm_moderate_new_reply.vue
// controller associé: src/Controller/ModerateNewReplyController.php

import { ref, computed, defineEmits } from "vue";
import { useRouter } from 'vue-router';
import { state } from "../store";
import component02_adm_navbar from "../components/component02_adm_navbar.vue";

// ============================================================================

const router = useRouter();

// ----------------------------------------------------------------------------

//
const message = ref("");

// ----------------------------------------------------------------------------

//
const parsedMessage = ref ({});

// ----------------------------------------------------------------------------

//
const errorMessage = ref("");

// ----------------------------------------------------------------------------

//
const errorOccurred = ref(false);

// ----------------------------------------------------------------------------

// variable pr n'afficher que les fils de discussion qui ont au
// moins 1 reply avec l'attribut is_new a true
// fonctio anonyme computed qui cree une propriete calculée
const filteredCommentsWithReplies = computed(() => {
  if (parsedMessage.value.commentsWithReplies) {
    return parsedMessage.value.commentsWithReplies.filter((fil) =>
      fil.replies.some((reply) => reply.is_new)
    );
  } else {
    return [];
  }
});

// ----------------------------------------------------------------------------

// Compte le nbre de replies avec l'attribut is_new
const newRepliesCount = computed(() => {
  if (parsedMessage.value.replies) {
    console.log('CONTENU: ', parsedMessage.value.replies.filter((reply) => reply.is_new === false).length);
    return parsedMessage.value.replies.filter((reply) => reply.is_new === false).length;
  } else {
    return 0;
  }
});

// ----------------------------------------------------------------------------

//
const emit = defineEmits(["update-nav-items"]);

// ----------------------------------------------------------------------------

// lien dynamique
const navigateToSpecificFil = (filId) => {
  router.push({ name: "view22_adm_moderate_new_specific_reply", params: { filId } });
};

// fonct°
const goToSommaire = () => {
    router.push({ name: "view11_adm_sommaire" });
  };

// ============================================================================

// fonct°
const showGoToSommaireButton = computed(() => {
  return parsedMessage.value.areNewComments && parsedMessage.value.areNewComments.length === 0;
});
// ============================================================================

// fonct° pr recuperer les données
const fetchData = async () => {
  try {
    const response = await fetch(`${apiBase}/adm/moderate_new_reply`, {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });

    if (!response.ok) {
      throw new Error("Error 01 from view16_adm_moderate_new_reply: Network response was not ok");
    }
    const data = await response.json();

    if (data.status === "Error, stopped") {
      errorOccurred.value = true;
      errorMessage.value = data.message;
      router.push({ name: "view01" });
    } else {
      message.value = JSON.stringify(data);
      parsedMessage.value = data;


      // MAJ les données avec les infos de l'utilisateur retrouvé'
      state.isLoggedIn = data.status === "Success";
      state.user = data.user;
    }
  } catch (error) {
    console.log("Error 02 from view16_adm_moderate_new_reply: ", error);
  }

  // emettre l'evenement ' 'update-nac-items' apres que le formulaire
  // ait été soumis
  emit("update-nav-items");
};

// allow 1 proxy to use every route starting with "adm"
// look for value VITE_API_BASE_URL defined to .env
const apiBase = import.meta.env.VITE_API_BASE_URL;

// Call fetchData() initially to load data
fetchData();

// ============================================================================

const handleSubmitChoiceForReply = async (replyId, action) => {
  const response = await fetch(`${apiBase}/adm/moderate_new_reply_step2`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
    body: JSON.stringify({ replyId, action }),
  });

  if (!response.ok) {
    console.error("Error submitting reply ID:", replyId);
  } else {
    console.log("Reply ID submitted successfully:", replyId);

      // appelle fetchData() pr MAJ les données apres soumiss° du form
      fetchData();

      // emettre l'evenement ' 'update-nac-items' apres que le formulaire
      // ait été soumis

      emit("update-nav-items");

  }
};

</script>

<template>
  <main>

    <div class = "adm_navbar">
        <!-- allow to communicate datas to component02 -->
        <!-- la derniere props permet de filtrer les elts du tableau -->
        <!-- commentsWithReplies qui ont le booleen containNewReply à true -->
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

    <!-- SI decommenté, il faut aussi décommenter la balise </section> -->
    <!-- qui se trouve 10 L au-dessous -->
    <!--
    <section class = "section01_connected_user_informations">
      
      <div v-if = "errorOccurred" class = "error-message">
            Message from view16: An error occurred: {{ errorMessage }}
      </div>
    -->
    

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

    <!--
    </section>
    -->

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
    <!--
    <section class = "section05_new_users">
      <h2>NEW Users:</h2>
      <div class = "new_users_container">
        <div v-for = "newuser in parsedMessage.areNewUsers" :key = "newuser.id" class = "newuser">
          <p>ID: {{ newuser._id }}</p>
          <p>Nickname: {{ newuser.nickname }}</p>
          <p>Email: {{ newuser.email }}</p>
          <p>Inscription date: {{ newuser.inscriptionDate }}</p>
          <p>is_new: {{ newuser.is_new }}</p>
          <hr>
        </div>
      </div>
    </section>
    -->

    <section class="section06_fils">
      <h2>Fils de discussion:</h2>
      <br>
      Affiche tous les commentaires et leur reply ("Modéré, accepté" - "Modéré,
      refusé" et "En attente de modération").

      <div v-if="filteredCommentsWithReplies.length === 0">
        <br>
        <button v-if="showGoToSommaireButton" @click="goToSommaire" type="button">Go to Sommaire</button>
        <br>
        <br>
      </div>

      <div v-else class="fils_container">
        <!-- PERMET D'AFFICHER tous LES COMMENTAIRES AVEC LEUR(S) REPONSE(S) -->
        <br>
        
        <div v-for="(fil, index) in filteredCommentsWithReplies" :key="`fil-${index}`" class="fil comment-container">
              <div class="comment-container">
                  <p><strong>Comment</strong></p>

                  <a @click="() => navigateToSpecificFil(fil.comment.id)">
                    <p>ID: {{ fil.comment.id }}</p>
                  </a>

                  <p>Author: {{ fil.comment.author }}</p>
                  <p>title: {{ fil.comment.title }}</p>
                  <p>Content: {{ fil.comment.content }}</p>
                  <p>Category: {{ fil.comment.category }}</p>
                  <p>created_at: {{ fil.comment.created_at }}</p>
                  <p>Flag: {{ fil.comment.flag }}</p>
                  <p>is_new: {{ fil.comment.is_new }}</p>
                  <p>is_published: {{ fil.comment.is_published }}</p>
                  <p>parent_id: {{ fil.comment.parent_id }}</p>
                  <p>published_at: {{ fil.comment.published_at }}</p>
              </div>

              <h4>Replies:</h4>
              <div v-for="(reply, replyIndex) in fil.replies"
                    :key="`reply-${replyIndex}`"
                    :class="{ 'reply-new': reply.is_new, 'last-reply-container': replyIndex === fil.replies.length - 1 }"
                    class="reply">

                <div class="old_replies-container">
                    <p><strong>Reply ID: {{ reply.id }}</strong></p>
                    <p>Author: {{ reply.author }}</p>
                    <p>title: {{ reply.title }}</p>
                    <p>Content: {{ reply.content }}</p>
                    <p>Category: {{ reply.category }}</p>
                    <p>created_at: {{ reply.created_at }}</p>
                    <p>Flag: {{ reply.flag }}</p>
                    <p>is_new: {{ reply.is_new }}</p>
                    <p>is_published: {{ reply.is_published }}</p>
                    <p>parent_id: {{ reply.parent_id }}</p>
                </div>

                <form v-if="reply.is_new" @submit.prevent="handleSubmitChoiceForReply(reply.id, 'accept')">
                  <button type="submit">Accept this reply</button>
                </form>
                
                <br v-if="reply.is_new">

                <form v-if="reply.is_new" @submit.prevent="handleSubmitChoiceForReply(reply.id, 'refuse')">
                  <button type="submit">Refuse this reply</button>
                </form>
                <br>
                <br>

              </div>

              <div v-if="fil.containNewReply" class="new-reply-info">
                This comment thread contains at leat a new reply.
              </div>

              <hr>
         
          </div>
          
        </div>

    </section>
  </main>
</template>

<style scoped>

/*
Codes couleur
#0fc0fc =
lightblue: #add8e6
white snow: #fffafa
lightsteelblue: #b0c4de
grey: #808080
*/

/*
container pr 1 cadre qui se trouve
au-dessous de la adm navbar
et qui ne contient rien
Mettre 1 width à 100% fait depasser le cadre
cadre visible si on le definit
*/
.section01_connected_user_informations {
  background-color: #808080;
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
  align-items: center;
  text-align: left;
  padding: 2rem;
  border-left: 1px solid black;
  border-right: 1px solid black;
}

/*
couleur de fond invisible
cadre invisible
*/
.section02_section_comments {
  background-color: #808080;
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
  text-align: left;
  /*
  border: 1px solid black;
  */
}

/*
cadre invisible
*/
.comment_container {
  background-color: blue;
  padding-left: 1rem;
}

/*
cadre invisible
*/
.section03_section_replies {
  background-color: #808080;
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
  text-align: left;
  /*
  border: 1px solid black;
  */
}

/*
cadre invisible
*/
.reply_container {
  padding-left: 1rem;
}

.section04_all_users {
  background-color: #808080;
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
  text-align: left;
  /*
  border: 1px solid black;
  */
}

.all_users_container {
  padding-left: 1rem;
}

.section05_new_users {
  background-color: #808080;
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
  text-align: left;
  /*
  border: 1px solid black;
  */
}

.new_users_container {
  padding-left: 1rem;
}

/*
container pr le fil de discuss°
gris foncé
*/
.section06_fils {
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

/*
container pr le commentaire
*/
.comment-container {
  background-color: #add8e6;
  border: 1px solid black;
  padding: 10px;
  margin-bottom: 15px;
  width: 95%;
  }

/*
container pr chacune des anciennes reponses,
celles qui ont ete modérées
*/
.old_replies-container {
  background-color: #add8e6;
  border: 1px solid black;
  padding: 10px;
  margin-bottom: 15px;
  }

/*
container pr le comment et les éventuelles
reponses déja modérées
*/
.fils_container {
  background-color: #add8e6;
  width: 95%;
  padding-left: 1rem;
  border: 1px solid black;
}

/*
Le container de la (ou des) réponse(s)
qu'il faut modérer
avec les 2 boutons
background-color = 
*/
.reply-new {
  background-color: red;
  padding: 10px;
  border: 1px solid black;
}

.last-reply-container {
  background-color: #0fc0fc;
  color: black;
  border: 10px solid #b0c4de;
}

</style>
