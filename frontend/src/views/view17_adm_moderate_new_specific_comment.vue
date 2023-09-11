<script setup lang="ts">
// fichier: src/Controller/ModerateNewSpecificCommentController {commentId}
// vue associée: src/views/view17_adm_moderate_new_specific_comment.vue

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

//
const parsedMessage = ref ({});

// ----------------------------------------------------------------------------

// create a new ref called areNewComments and assign the value
const areNewComments = ref([]);

// ----------------------------------------------------------------------------

// Create a new ref called specificComment and initialize it to an empty object
const specificComment = ref({});

// ----------------------------------------------------------------------------

//
const commentId = router.currentRoute.value.params.commentId;

// ----------------------------------------------------------------------------

//
const action = ref("");

// ----------------------------------------------------------------------------

//
const errorMessage = ref("");

// ----------------------------------------------------------------------------

//
const errorOccurred = ref(false);


// ----------------------------------------------------------------------------

// allow 1 proxy to use every route starting with "adm"
// look for value VITE_API_BASE_URL defined to .env
const apiBase = import.meta.env.VITE_API_BASE_URL;

// ============================================================================

// Create a new function to fetch data
const fetchData = async () => {
  try {
    const response = await fetch(`${apiBase}/adm/moderate_new_specific_comment/${commentId}`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });

    if (!response.ok) {
      throw new Error("Error 01 from view17_adm_moderate_new_specific_comment, network response was not ok");
    }
    const data = await response.json();

    if (data.status === "Error, stopped") {
      console.log("Error 02 from view17_adm_moderate_new_specific_comment: ", data.status);
      errorOccurred.value = true;
      errorMessage.value = data.message;
    } else {
      console.log("Success 01 from view17_adm_moderate_new_specific_comment");
      message.value = JSON.stringify(data);
      parsedMessage.value = data;

      // Find the specific comment from the areNewComments array using the commentId
      specificComment.value = data.areNewComments.find(comment => comment.id === commentId);

    }
  } catch (error) {
    console.log("Error 03 from view17_adm_moderate_new_specific_comment: ", error);
  }

};

// ============================================================================

// Call fetchData() initially to load data
fetchData();

// ============================================================================

// Methode handleSubmitChoiceForComment
const handleSubmitChoiceForComment = async (commentId, action) => {
  try {
    const response = await fetch(`${apiBase}/adm/moderate_new_specific_comment_step2`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
      body: JSON.stringify({ commentId, action }),
    });

    if (!response.ok) {
      throw new Error("Error 04 from view17_adm_moderate_new_specific_comment, network response was not ok");
    }
    const data = await response.json();

    if (data.status === "Success") {
      console.log("Success 02 from view17_adm_moderate_new_specific_comment: ", data.message);
      router.push({ name: 'view11_adm_sommaire' });
      
      fetchData();
    } else {
      console.error("Error 05 from view17_adm_moderate_new_specific_comment: ", data.message);
    }
  } catch (error) {
    console.log("Error 06 from view17_adm_moderate_new_specific_comment: ", error);
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
        <h2>Comment Details</h2>
        <div v-if="specificComment && specificComment.id">
          <h3>Title: {{ specificComment.title }}</h3>
          <h3>Id: {{ specificComment.id }}</h3>
          <h3>Author: {{ specificComment.author }}</h3>
          <h3>content: {{ specificComment.content }}</h3>
          <h3>Category: {{ specificComment.category }}</h3>
          <h3>is_published: {{ specificComment.is_published }}</h3>
          <h3>created_at: {{ specificComment.created_at }}</h3>
          <h3>published_at: {{ specificComment.published_at }}</h3>
          <h3>is_new: {{ specificComment.is_new }}</h3>
          <h3>parent_id: {{ specificComment.parent_id }}</h3>
          
          <br>
        
          <form v-if="specificComment.is_new"
          @submit.prevent="handleSubmitChoiceForComment(specificComment.id, 'accept')">
              <button type="submit">Accept this comment</button>
            </form>
            <br v-if="specificComment.is_new">
            <form v-if="specificComment.is_new"
            @submit.prevent="handleSubmitChoiceForComment(specificComment.id, 'refuse')">
              <button type="submit">Refuse this comment</button>
          </form>
        
        </div>
        <div v-else>
          <p>No comment data found.</p>
        </div>
      </div>
    </section>
  </main>
</template>

<style scoped>

.section01 {
  background-color: blue;
  display: flex;
  flex-direction: column;
  aspect-ratio: 16/9;
  height: min(100vh, calc(16vw / 9));
  width: 96%;
  text-align: left;
}

.description {
  background-color: lightblue;
  width: 100%;
  text-align: left;
  padding: 20px;
  margin-bottom: 20px;
  border: 1px solid black;
}

</style>
