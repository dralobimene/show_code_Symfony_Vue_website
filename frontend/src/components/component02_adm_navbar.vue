<script setup lang="ts">
// fichier: src/components/component02_adm_navbar.vue

import { ref } from 'vue';
import { watchEffect } from 'vue';
import { defineProps } from 'vue';
import { computed } from 'vue';

// ----------------------------------------------------------------------------

interface NavItem {
  title: string;
  link: string;
  count?: number;
  countText?: string;
  newUsersCount?: number;
  newCommentsCount?: number;
  newFilsCount?: number;
  newRepliesCount?: number;
}
/*
TypeScript interface definition named NavItem. An interface in TypeScript
is a way to define the shape of an object, specifying the types of
its properties. This can be helpful for ensuring that objects with a
specific structure are used correctly within the codebase
*/

// ----------------------------------------------------------------------------

// Define props
// allow to get datas
const props = defineProps<{
  userData: Object,
  usersCount: number,
  commentsCount: number,
  repliesCount: number,
  newUsersCount: number,
  newCommentsCount: number,
  filsCount: number,
  newFilsCount: number,
  newRepliesCount: number;
}>();
/*
defines props using the defineProps function in Vue 3 with TypeScript.
Props are a way to pass data from a parent component to a child component in Vue.
The defineProps function allows you to specify the types and requirements
for the props that the component expects to receive.
*/

// ----------------------------------------------------------------------------

// Define computed property for newRepliesCount
const newRepliesCount = computed(() => {
  if (props.repliesCount) {
    return props.repliesCount - props.newRepliesCount;
  } else {
    return 0;
  }
});

// ----------------------------------------------------------------------------

const navItems = ref<NavItem[]>([
  { title: 'Home', link: '/view11_adm_sommaire' },

  {
    title: 'comments',
    link: '/view14_adm_moderate_new_comment',
    altLink: '/view18_adm_moderate_new_comments',
    countText: `(${props.commentsCount}, `,
    newCommentsCount: props.newCommentsCount,
  },

  {
    title: 'users',
    link: '/view15_adm_moderate_new_user',
    altLink: '/view19_adm_moderate_new_users',
    countText: `(${props.usersCount}, `,
    newUsersCount: props.newUsersCount,
  },

  {
    title: 'fils',
    link: '/view16_adm_moderate_new_reply',
    countText: `(${props.filsCount}, `,
    // countText: `(${props.filsCount}${props.newRepliesCount ? `, ${props.newRepliesCount}` : ''}), `,
    newFilsCount: props.newFilsCount,
    /*
    newRepliesCount: computed(() => {
      if (props.repliesCount) {
        return props.repliesCount - props.newRepliesCount;
      } else {
        return 0;
      }
    }),
    */
    newRepliesCount: newRepliesCount,
  },

]);

// ----------------------------------------------------------------------------

const updateNavItems = () => {
  navItems.value = [
    { title: 'Home', link: '/view11_adm_sommaire' },

    {
      title: 'comments',
      link: '/view14_adm_moderate_new_comment',
      altLink: '/view18_adm_moderate_new_comments',
      countText: `(${props.commentsCount}, `,
      newCommentsCount: props.newCommentsCount,
    },

    {
      title: 'users',
      link: '/view15_adm_moderate_new_user',
      altLink: '/view19_adm_moderate_new_users',
      countText: `(${props.usersCount}, `,
      newUsersCount: props.newUsersCount,
    },

    {
      title: 'fils',
      link: '/view16_adm_moderate_new_reply',
      countText: `(${props.filsCount}, `,
      // countText: `(${props.filsCount}${props.newRepliesCount ? `, ${props.newRepliesCount}` : ''}), `,
      newFilsCount: props.newFilsCount,
      /*
      newRepliesCount: computed(() => {
      if (props.repliesCount) {
        return props.repliesCount - props.newRepliesCount;
      } else {
        return 0;
      }
    }),
    */
    newRepliesCount: newRepliesCount,

    },
  ];

  // console.log('Updated navItems:', navItems.value);
};

// ----------------------------------------------------------------------------

// Wrap updateNavItems in a watchEffect
watchEffect(() => {
  // console.log('watchEffect triggered');
  updateNavItems();
});
/*
watchEffect is a function from the Vue 3 Composition API that allows you
to run a function whenever one or more of its reactive dependencies change.
It's similar to watch, but instead of watching a specific reactive property,
it tracks all the reactive properties used inside the given function.
*/

</script>

<template>
  <nav class="navbar">
    <ul class="navbar-links">
      <li v-for="(item, index) in navItems" :key="index">

        <a v-if="item.countText" :href="item.altLink ? item.altLink : item.link" class="white-text">
          {{ item.title }}{{ item.countText }}
        </a>
        <a v-else :href="item.link" class="white-text">
          {{ item.title }} {{ item.count }}
        </a>
        <a v-if="item.newUsersCount" :href="item.link" class="red-text">
          {{ item.newUsersCount }}
        </a>
        <a v-if="item.newCommentsCount" :href="item.link" class="red-text">
          {{ item.newCommentsCount }}
        </a>
        <a v-if="item.newFilsCount" :href="item.link" class="red-text">
          {{ item.newFilsCount }}
        </a>
        <a v-if="item.newRepliesCount" :href="item.link" class="green-text">
          , {{ item.newRepliesCount }}
        </a>
        <span v-if="item.countText" class="white-text">
          )
        </span>
      </li>
    </ul>
  </nav>
</template>

<style scoped>

.navbar {
  display: flex;
  background-color: #333;
  padding: 1rem;
}

.navbar-links {
  display: flex;
  list-style-type: none;
  margin: 0;
  padding: 0;
}

.navbar-links li {
  margin-right: 1rem;
}

.navbar-links a, .navbar-links .white-text {
  text-decoration: none;
  color: white;
}

.navbar-links a.red-text {
  color: red;
}

.navbar-links a.green-text {
    color: green;
}

</style>
