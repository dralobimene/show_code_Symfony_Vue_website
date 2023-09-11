<script setup lang="ts">

// Importation de la fonction 'ref' depuis 'vue' pour définir
// des références réactives
import { ref } from "vue";

// Déclaration des constantes réactives pour stocker le message,
// le message analysé, le sujet et le contenu
const message = ref("");
const parsedMessage = ref ({});

const subject = ref("");
const content = ref("");

// ============================================================================

// Déclaration de la fonction asynchrone handleSubmit qui sera exécutée
// lors de la soumission du formulaire
const handleSubmit = async () => {
  // Création d'un objet formData avec le sujet et le contenu
  // saisis par l'utilisateur
  const formData = {
    subject: subject.value,
    content: content.value,
  };

  try {
    // Envoi d'une requête POST à l'URL '/contact' avec le contenu du formulaire
    const response = await fetch("/contact", {
      method: "POST",
      headers: {
        // Définition des entêtes de la requête
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,

      },
      // Conversion de l'objet formData en chaîne JSON
      body: JSON.stringify(formData),
    });

    // Si la réponse n'est pas OK, on lance une exception
    if (!response.ok) {
      throw new Error("Failed to submit the form");
    }

    // Conversion de la réponse en JSON
    const result = await response.json();

  } catch (error) {
    console.error("Error submitting form:", error.message);
  }
};

</script>

<template>
  <main>
    <section class="section01">
      
      <div class="description">
        <h2><strong>Contact us.</strong></h2>
      
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <input 
            v-model="subject"
            type="text"
            placeholder="Enter a subject for your email"
            required: true
          />
          <br>
          <br>
          <textarea 
            cols="100" rows="10"
            v-model="content" 
            placeholder="Enter content"
            required>
          </textarea>

        </div>
        <br>
        <div class="form-group">
          <button type="submit">Submit</button>
        </div>
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
*/
.section01 {
  background-color: #fffafa;
  display: flex;
  flex-direction: column;
  aspect-ratio: 16/9;
  height: min(100vh, calc(16vw / 9));
  width: 100%;
  text-align: left;
}

.description {
  background-color: #add8e6;
  width: 95%;
  text-align: left;
  padding: 20px;
  margin-bottom: 20px;
  border: 1px solid black;
}
</style>
