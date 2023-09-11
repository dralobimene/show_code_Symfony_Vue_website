<script setup lang="ts">
// fichier src/views/view09_reply_user_post.vue
// controller associé: src/Controller/ReplyUserPostController.php

import { ref, watch } from "vue";
import { useRouter } from "vue-router";
import { defineProps } from "vue";

import axios from 'axios';
/*
Axios est une bibliothèque cliente HTTP basée pour les navigateurs
et les applications Node.js, ce qui signifie qu'elle peut être utilisée
à la fois dans les applications JavaScript frontales et les serveurs.
*/

// ----------------------------------------------------------------------------

// Obtenir l'instance du routeur pour naviguer entre les vues
const router = useRouter();

// ----------------------------------------------------------------------------

const message = ref("");

// ----------------------------------------------------------------------------

const errorMessage = ref("");

// parsedMessage = object avec 3 proprietes
const parsedMessage = ref({
  // object
  user: {},
  // object
  comment: {},
  // array
  replies: [],
});

// ----------------------------------------------------------------------------

// les props sont définies en utilisant la fonction defineProps
// la fonction defineProps est utilisée pour définir les propriétés attendues
// que le composant recevra de son composant parent ou du routeur
const props = defineProps({
  p_id: {
    type: String,
    required: true,
  },
});

/*
En définissant les props de cette manière, vous pouvez vous assurer que le composant reçoit
le bon type de données et renforce l'obligation de la propriété p_id.
Cela rend également le composant plus réutilisable et plus facile à maintenir,
car les propriétés attendues sont clairement définies
*/

// ----------------------------------------------------------------------------

const additionalData_title = ref("");
const additionalData_content = ref("");
const successMessage = ref("");

// ============================================================================

// function pr recuperer les reponses
async function fetchReplies() {
  try {
    // axios.get est utilisé pour faire une requête HTTP GET vers le point
    // de terminaison spécifié, qui est /reply_user_post/${props.p_id}
    // Le props.p_id est une partie dynamique de l'URL, et il est remplacé par
    // la valeur réelle de la propriété p_id passée au composant.
    // En utilisant le mot-clé await devant l'appel axios.get, cela fait
    // pause l'exécution de la fonction jusqu'à ce que la promesse retournée par axios.get
    // soit résolue ou rejetée. Cela vous permet de travailler avec la
    // réponse de manière plus synchrone, rendant le code plus
    // lisible et facile à comprendre
    // asynchrone
    const response = await axios.get(`/reply_user_post/${props.p_id}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });

    // variable
    const data = response.data;
    // several properties ob object response:
    // en rapport avec le json envoyé par le controller SF
    // - data:
    // - status (200, 201, 400, 401, 404, 500, ...)
    // - statusText
    // - headers
    // - config
    // - request

    // token invalide, pas d'user connecté
    // on redirige
    if (data.operation1 === "Check token" && data.status1 === "Error, stopped") {
      console.log("errormessage.value: ", data.message1);
      errorMessage.value = data.message1;
      router.push({ name: 'view01' });
      return;
    }

    // variable
    const filteredReplies = data.replies.filter(reply => {
      return (
        reply.reply_is_published === true &&
        reply.reply_flag === "Modéré, accepté" &&
        reply.reply_is_new === false
      );
    });

    // variable
    data.replies = filteredReplies;

    // 
    data.replies.sort((a, b) => {
      if (!a.reply_published_at || !b.reply_published_at) {
        return 0;
      }
      return new Date(b.reply_published_at.date) - new Date(a.reply_published_at.date);
    });

    //
    parsedMessage.value = {
      user: data.user,
      comment: data.comment,
      replies: data.replies || [],
    };

    if(!data.replies) {
        data.replies = [];
    }

    if(!parsedMessage.value.user) {
        console.log("parsedMessage.value.user: aucun user, impossible");
    } else {
        console.log("parsedMessage.value.user: ", parsedMessage.value.user);
    }
    
    if(!parsedMessage.value.comment) {
        console.log("parsedMessage.value.comment: aucun comment, impossible");
    } else {
        console.log("parsedMessage.value.comment: ", parsedMessage.value.comment);
    }

    if(!parsedMessage.value.replies) {
        console.log("parsedMessage.value.replies: aucune reply, possible");
    } else {
        console.log("parsedMessage.value.replies: ", parsedMessage.value.replies);
    }


  } catch (error) {
    console.error("Error 01 from view09_reply_user_post while fetching replies:", error);
    if (error.response && error.response.data) {
        console.log("errormessage.value: ", error.response.data);
        errorMessage.value = error.response.data.message1;
              router.push({ name: 'view01' });

    }
  }
}

// ============================================================================

watch(parsedMessage, (newValue, oldValue) => {
  console.log('Old value:', oldValue);
  console.log('New value:', newValue);
});
/*
watch est une fonction de Vue 3.
Elle prend deux arguments : la propriété réactive à observer, et une fonction de rappel
à exécuter lorsque la propriété observée change.
La fonction de rappel reçoit deux paramètres :
    newValue: La valeur mise à jour de la propriété observée.
    oldValue: La valeur de la propriété observée avant le changement.

utile pour le débogage, pour suivre comment la valeur de parsedMessage
change au fil du temps, ou pour effectuer des actions supplémentaires chaque fois que la valeur
de la réf parsedMessage change
*/

// ============================================================================

fetchReplies();

// ============================================================================

const submitForm = async () => {
  try {
    
    //
    const formData = new FormData();
    formData.append('user', JSON.stringify(parsedMessage.value.user));
    formData.append('comment', JSON.stringify(parsedMessage.value.comment));
    formData.append('additionalData', JSON.stringify({
      title: additionalData_title.value,
      content: additionalData_content.value
    }));

    //
    const response = await axios.post('/reply_user_post_step2', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        Authorization: `Bearer ${localStorage.getItem('token')}`,
      },
    });

    if (response.status === 200) {
      console.log('Form submitted successfully');
      console.log('Response data:', response.data);

      additionalData_title.value = "";
      additionalData_content.value = "";
      successMessage.value = "Reply recorded successfully. You will be redirected to the home in 1 seconds. Thank you.";

      setTimeout(() => {
        router.push({ name: 'view01' });
      }, 1000);

    } else {
      console.error('Error 02 from view09_reply_user_post while submitting form');
    }
  } catch (error) {
    console.error(error);
    if (error.response && error.response.data) {
        console.log("errorMessage.value from submitForm: ", error.response.data.message1);
        errorMessage.value = error.response.data.message1;
  }
  }
};
</script>

<template>
  <main>
    <section class="section01">
      
      <div class="description">

          <!--
          <div v-if="parsedMessage.user" class="user">
            <h3>Connected User Details</h3>
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
            <br>
          </div>
          -->

          <h2>Post your reply</h2>
          <p>Please, post your reply.</p>

          <form @submit.prevent="submitForm">
            <input type="text" v-model="additionalData_title" placeholder="Enter a title">
            <br>
            <br>
            <textarea
                cols="100" rows="10"
                v-model="additionalData_content" 
                placeholder="Enter content">
            </textarea>
            <br>
            <br>
            <button type="submit">Submit</button>
          </form>

          <br>
          <br>

          <hr>
          <hr>

          <!-- Display comment data -->
          <div v-if="parsedMessage.comment" class="comment">
            <h3>Comment Details</h3>
            <hr>
            <strong>title: </strong>{{ parsedMessage.comment.comment_title }}
            <br>
            <strong>id: </strong>{{ parsedMessage.comment.comment_id }}
            <br>
            <strong>author: </strong>{{ parsedMessage.comment.comment_author }}
            <br>
            <strong>content: </strong>{{ parsedMessage.comment.comment_content }}
            <br>
            <strong>category: </strong>{{ parsedMessage.comment.comment_category }}
            <br>
            <strong>created_at: </strong>{{ parsedMessage.comment.comment_created_at }}
            <br>
            <strong>flag: </strong>{{ parsedMessage.comment.comment_flag }}
            <br>
            <strong>is_published: </strong>{{ parsedMessage.comment.comment_is_published }}
            <br>
            <strong>parent_id: </strong>{{ parsedMessage.comment.comment_parent_id }}
            <br>
            <strong>is_new: </strong>{{ parsedMessage.comment.comment_is_new }}
            <br>
            <strong>published_at: </strong>{{ parsedMessage.comment.comment_published_at }}
            <hr>
          </div>

          <hr>

          <!-- Display replies data -->
          <div v-if="parsedMessage.replies && parsedMessage.replies.length > 0" class="replies">
            <h3>Replies</h3>
            <div v-for="reply in parsedMessage.replies" :key="reply.reply_id">
              <hr>
              <strong>Reply ID:</strong> {{ reply.reply_id }}
              <br>
              <strong>Title:</strong> {{ reply.reply_title }}
              <br>
              <strong>Author:</strong> {{ reply.reply_author }}
              <br>
              <strong>Content:</strong> {{ reply.reply_content }}
              <br>
              <strong>Category:</strong> {{ reply.reply_category }}
              <br>
              <strong>Created At:</strong> {{ reply.reply_created_at }}
              <br>
              <strong>Flag:</strong> {{ reply.reply_flag }}
              <br>
              <strong>Is Published:</strong> {{ reply.reply_is_published }}
              <br>
              <strong>Parent ID:</strong> {{ reply.reply_parent_id }}
              <br>
              <strong>is_new:</strong> {{ reply.reply_is_new }}
              <br>
              <strong>published_at:</strong> {{ reply.reply_published_at }}
              <br>
            </div>

            <hr>

          </div>

          <div v-if="successMessage" class="success-message">
            {{ successMessage }}
          </div>

      </div>

    </section>
  </main>
</template>

<style scoped>

.description {
  background-color: lightblue;
  width: 95%;
  text-align: left;
  padding: 20px;
  margin-bottom: 20px;
  border: 1px solid black;
}

</style>
