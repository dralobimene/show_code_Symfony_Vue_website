<script setup lang="ts">
// src/App.vue

import { watch, ref, provide } from 'vue';
import { computed } from 'vue';
import { state } from './store.ts';

// ============================================================================

/*
watch is a function from the Vue 3.
It takes two arguments: the reactive property to observe, and a callback
function to execute when the observed property changes.
The callback function receives two parameters:
    newValue: The updated value of the observed property.
    oldValue: The value of the observed property before the change.

useful for debugging purposes, to track how the value of parsedMessage
changes over time, or to perform additional actions whenever the value
of the parsedMessage ref changes
*/
watch(
  () => state.isLoggedIn,
  (newValue) => {
    isLoggedIn.value = newValue;
  }
);

// ============================================================================

// isLoggedIn fait ref a celle du fichier
// src/store.ts
const isLoggedIn = ref(state.isLoggedIn);

// bind les 2 variables (a faire confirmer par CHAT)
provide('isLoggedIn', isLoggedIn);

//
const user = computed(() => state.user);
</script>

<template>
  <main>
    <section class="section01">
      <div class="container">

        <div class="header">
          Header
        </div>
        
        <div class="nav">

          <div class="item">
            <RouterLink to="/view01">Home</RouterLink>
          </div>
          <div class="item" v-if="!isLoggedIn">
            <RouterLink to="/view02_subscribe">Subscribe</RouterLink>
          </div>
          <div class="item" v-if="!isLoggedIn">
            <RouterLink to="/view04_connect">Connect</RouterLink>
          </div>
          <div class="item" v-if="isLoggedIn">
            <RouterLink to="/view06_logout">Logout</RouterLink>
          </div>
          <div class="item" v-if="isLoggedIn">
            <RouterLink to="/view08_comment_user_post">New comment</RouterLink>
          </div>
          <div class="item" v-if="isLoggedIn">
            <RouterLink to="/view05_secured_user_personal_panel">Panel</RouterLink>
          </div>
          <div class="item">
            <RouterLink to="/view21_contact">Contact</RouterLink>
          </div>


        </div>

        <br>

        <!--
        <div class="message-container">
            <div v-if="isLoggedIn && user">
                Welcome, {{ user.nickname }}
                <br>
                roles: {{ user.roles }}
                <div v-if="user.nickname === 'laurent_adm'">
                    <a href="/view11_adm_sommaire">Admin</a>
                </div>
            </div>
            <div v-else>
                Message from App.vue: User is not logged in.
            </div>
        </div>
        -->
        
        <div class="scrollable-content">
          <div class="contentView">
            <RouterView />
          </div>
        </div>
        
        <div class="footer">
          <div v-if="isLoggedIn && user">
                -----
                Welcome, {{ user.nickname }}
                -----
                roles: {{ user.roles }}
                -----
                <span v-if="user.nickname === 'laurent_adm'">
                    <a href="/view11_adm_sommaire">Admin</a>
                </span>
            </div>
            <div v-else>
                Message from App.vue: User is not logged in.
            </div>
        </div>

      </div>
      
      <br>
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

  body {
    overflow-y: hidden;
  }
  
  .section01 {
    display: flex;
    flex-direction: column;
    height: 100vh;
    width: 100%;
    margin-left: 0;
    align-items: center;
    margin-top: 20px;
  }

  .container {
    display: flex;
    flex-direction: column;
    width: 100%;
    /*max-width: 900px;*/
  }

  .header {
    background-color: #b0c4de;
    display: flex;
    padding: 20px;
    border: 1px solid black;
  }

  .nav {
    background-color: #ddd;
    display: flex;
    padding: 20px;
    border: 1px solid black;

  }

  .item {
    text-align: left;
    margin-right: 20px;
  }

  .message-container {
    text-align: left;
    width: 100%;
  }

  .scrollable-content {
    flex-grow: 1;
    overflow-y: auto;
    width: 100%;
    height: calc(100vh - 40px - 20px - 40px - 100px - 20px);
  }

  .contentView {
    aspect-ratio: 16/9;
    width: 100%;
  }

  .footer {
    background-color: #b0c4de;
    display: flex;
    padding: 20px;
    position: sticky;
    bottom: 0;
    border: 1px solid black;
  }
</style>
