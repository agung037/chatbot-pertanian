import { createRouter, createWebHistory } from 'vue-router';

// Import views
import Dashboard from '@/views/Dashboard.vue';

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/detection',
    name: 'DiseaseDetection',
    component: () => import(/* webpackChunkName: "detection" */ '@/views/DiseaseDetection.vue')
  },
  {
    path: '/forum',
    name: 'Forum',
    component: () => import(/* webpackChunkName: "forum" */ '@/views/Forum.vue')
  },
  {
    path: '/chat',
    name: 'Chat',
    component: () => import(/* webpackChunkName: "chat" */ '@/views/Chat.vue')
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import(/* webpackChunkName: "notfound" */ '@/views/NotFound.vue')
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    // Always scroll to top
    return { top: 0 };
  },
});

export default router; 