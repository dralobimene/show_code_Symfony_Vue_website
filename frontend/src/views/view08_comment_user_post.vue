<script setup lang="ts">
// fichier: src/views/view08_comment_user_post.vue
// controller associée: src/Controller/CommentUserPostController.php

import { ref } from "vue";
import { useRouter } from 'vue-router';

// ============================================================================

const router = useRouter();

// initialise propriétés réactives
const message = ref("");
const parsedMessage = ref ({});
const author = ref("");
const title = ref("");
const content = ref("");
const category = ref("");

// ============================================================================

// lorsque le composant est crée, 1 requete initiale GET est effectuée vers
// le controller SF
// l'objet de reponse est transformée en json'
fetch("/comment_user/post", {
  method: "GET",
  headers: {
    "Content-Type": "application/json",
    Authorization: `Bearer ${localStorage.getItem("token")}`,
  },
})
  .then((response) => {
    // leve une erreur si la reponse n'est pas ok
    if (!response.ok) {
      throw new Error(response.statusText);
    }
    // retourne la reponse format Json
    return response.json();
  })
  .then((data) => {
    console.log("data.status1: ", data.status1);
    console.log("data.status2: ", data.status2);
    
    // utilise les données parsées pour MAJ les proprietes
    message.value = JSON.stringify(data);
    parsedMessage.value = data;

    // Counting the number of keys in message and parsedMessage
    console.log("Number of keys in message: ", Object.keys(JSON.parse(message.value)).length);
    console.log("Number of keys in parsedMessage: ", Object.keys(parsedMessage.value).length);

    // compte le nbre de clés ds l'objet response' et
    // et console.log en fonct° du nbre de clé.
    // UTILITE: deboggage
    if(Object.keys(JSON.parse(message.value)).length == Object.keys(parsedMessage.value).length) {
        
        //
        let nbreClesDsMessage = Object.keys(JSON.parse(message.value)).length;
        let nbreClesDsParsedMessage = Object.keys(parsedMessage.value).length;

        //
        if(nbreClesDsMessage == 2 && nbreClesDsParsedMessage == 2) {
            console.log("meme nbre de cles: 2, erreur à la validation de l'etape 01");
            console.log("src/Controller/CommentUserPostController.php");
            console.log("Access denied");
        } else if(nbreClesDsMessage == 3 && nbreClesDsParsedMessage == 3) {
            console.log("meme nbre de cles: 3, erreur à la validation de l'etape 02");
            console.log("src/Controller/CommentUserPostController.php");
            console.log("Invalid token");
        } else if(nbreClesDsMessage == 6 && nbreClesDsParsedMessage == 6) {
            console.log("meme nbre de cles: 6, erreur à la validation de l'etape 03");
            console.log("src/Controller/CommentUserPostController.php");
            console.log("User not found");
        } else if(nbreClesDsMessage == 10 && nbreClesDsParsedMessage == 10) {
            console.log("meme nbre de cles: 10. Il faut maintenant soumettre");
            console.log("le formulaire pr creer la request");
            console.log("src/Controller/CommentUserPostController.php");
            console.log("Please submit form to make request");
        }
    } else {
        console.log("Erreur: nbre de cles différent");
    }

    // si l'utilisater existe dans la reponse parsée, l'utiliser pr
    // MAJ le champs author
    author.value = parsedMessage.value.user?.nickname || '';
  })
  .catch((error) => {
    if (error.message.includes('Forbidden')) {
      router.push({ name: 'view04_connect' });
    } else {
      console.log("Error 02 from view08_comment_user_post: ",error);
    }
  });

// ============================================================================

// soumettre le formulaire
const submitForm = async () => {

  // Verifie si les 3 champs st remplis
  if (title.value.trim() === "" || content.value.trim() === "" || category.value.trim() === "") {
    alert("Please fill in all 3 fields");
    return;
  }

  //
  const data = {
    title: title.value,
    content: content.value,
    category: category.value,
  };

  // effectue 1 requete en POST au controller SF
  // avec l'objet en corps de requete'
  try {
    const response = await fetch("/comment_user/post", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      if (response.status === 403) {
        router.push({ name: 'view04_connect' });
        return;
      }
      throw new Error(await response.text());
    }

    const responseData = await response.json();
    message.value = JSON.stringify(responseData);
    parsedMessage.value = responseData;
    author.value = parsedMessage.value.user?.nickname || '';

    // Redirect to view01.vue
    router.push({ name: 'view01' });

  } catch (error) {
    if (error.message.includes('Access Denied from JwtAuthListener')) {
      router.push({ name: 'view04_connect' });
    } else {
      alert("Error 01 from view08_comment_user_post: ", error);
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
          -->

          <div class="subscribe_form">
              <form @submit.prevent="submitForm">
                <label>You will post as:</label>
                <br>
                <input type="text" v-model="author" readonly />
                <br>
                <br>
                <label>Please enter a title for your comment:</label>
                <br>
                <input type="text" id="title" v-model="title" required />
                <br>
                <br>
                <label>Please add content for your comment:</label>
                <br>
                <textarea
                    cols="100" rows="10"
                    v-model="content" 
                    placeholder="Enter content"
                    required>
                </textarea>
                <br>
                <br>
                <label>Please choose a category for your comment:</label>
                <br>
                <select id="category" v-model="category" required>
                  <option value="">Select a category</option>
                  <option value="character">Character</option>
                  <option value="improvments">Improvments</option>
                </select>

                <br>
                <br>
                <button type="submit">Submit</button>
              </form>
          </div>
      
      </div>

    </section>
  </main>
</template>

<style scoped>
/*
.section01 {
  background-color: blue;
  display: flex;
  flex-direction: column;
  aspect-ratio: 16/9;
  height: min(100vh, calc(16vw / 9));
  width: 100%;
  text-align: left;
}
*/

.description {
  background-color: lightblue;
  width: 95%;
  text-align: left;
  padding: 20px;
  margin-bottom: 20px;
  border: 1px solid black;
}
</style>
