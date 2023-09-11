import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    
    {
      path: "/view01",
      // le parametre name est a ecrire ds le App.vue
      // ds les balises RouterLink
      // (si jamais cette view doit etre accessible depuis la navbar)
      name: "view01",
      component: () => import("../views/view01.vue"),
    },

    {
      path: "/view02_subscribe",
      name: "view02_subscribe",
      component: () => import("../views/view02_subscribe.vue"),
    },

    {
      // https://stackoverflow.com/questions/71029445/handling-dot-in-vue-router-params-using-vue-3/71803786#71803786
      // pr essayer de resoudre le probleme du mail qui renvoie sur rien
      path: "/view03_check_token/:token",
      name: "view03_check_token",
      component: () => import("../views/view03_check_token.vue"),
      props: true,
    },

    {
      path: "/view04_connect",
      name: "view04_connect",
      component: () => import("../views/view04_connect.vue"),
    },

    {
      path: "/view05_secured_user_personal_panel",
      name: "view05_secured_user_personal_panel",
      component: () => import("../views/view05_secured_user_personal_panel.vue"),
    },

    {
      path: "/view06_logout",
      name: "view06_logout",
      component: () => import("../views/view06_logout.vue"),
    },

    {
      path: "/view07_approve/:token",
      name: "view07_approve",
      component: () => import("../views/view07_approve.vue"),
      props: true,
    },

    {
      path: "/view08_comment_user_post",
      name: "view08_comment_user_post",
      component: () => import("../views/view08_comment_user_post.vue"),
      props: true,
    },

    {
      path: "/view09_reply_user_post/:p_id",
      name: "view09_reply_user_post",
      component: () => import("../views/view09_reply_user_post.vue"),
      props: true,
    },

    {
        path: '/view11_adm_sommaire',
        name: 'view11_adm_sommaire',
        component: () => import("../views/view11_adm_sommaire.vue"),
    },

    {
      path: "/view12_adm_delete_comment",
      name: "view12_adm_delete_comment",
      component: () => import("../views/view12_adm_delete_comment.vue"),
    },

    {
      path: "/view13_adm_delete_user",
      name: "view13_adm_delete_user",
      component: () => import("../views/view13_adm_delete_user.vue"),
    },

    {
      path: "/view14_adm_moderate_new_comment",
      name: "view14_adm_moderate_new_comment",
      component: () => import("../views/view14_adm_moderate_new_comment.vue"),
    },

    {
      path: "/view15_adm_moderate_new_user",
      name: "view15_adm_moderate_new_user",
      component: () => import("../views/view15_adm_moderate_new_user.vue"),
    },

    {
      path: "/view16_adm_moderate_new_reply",
      name: "view16_adm_moderate_new_reply",
      component: () => import("../views/view16_adm_moderate_new_reply.vue"),
    },

      // la jumelle de la view20
    {
      path: "/view17_adm_moderate_new_specific_comment/:commentId",
      name: "view17_adm_moderate_new_specific_comment",
      component: () => import("../views/view17_adm_moderate_new_specific_comment.vue"),
    },

    {
      path: "/view18_adm_moderate_new_comments",
      name: "view18_adm_moderate_new_comments",
      component: () => import("../views/view18_adm_moderate_new_comments.vue"),
    },

    {
      path: "/view19_adm_moderate_new_users",
      name: "view19_adm_moderate_new_users",
      component: () => import("../views/view19_adm_moderate_new_users.vue"),
    },

      // la jumelle de la view17
    {
      path: "/view20_adm_moderate_new_specific_user/:userId",
      name: "view20_adm_moderate_new_specific_user",
      component: () => import("../views/view20_adm_moderate_new_specific_user.vue"),
    },

    {
      path: "/view21_contact",
      name: "view21_contact",
      component: () => import("../views/view21_contact.vue"),
    },

    {
      path: "/view22_adm_moderate_new_specific_reply/:filId",
      name: "view22_adm_moderate_new_specific_reply",
      component: () => import("../views/view22_adm_moderate_new_specific_reply.vue"),
    },

  ],
});

export default router;
