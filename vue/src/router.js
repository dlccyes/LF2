import { createRouter, createWebHistory, createWebHashHistory } from 'vue-router'
// import App from '../App.vue'
import Data from '@/views/Data_blade.vue'
import Invalid from '@/views/Invalid_blade.vue'

const routes = [
  { path: '/', name: "home", component: Data},
  { path: '/std/:id', name: "student", component: Data },
  { path: "/:pathMatch(.*)", name: "not-found", component: Invalid },
];
const router = createRouter({
  // history: createWebHistory(import.meta.env.BASE_URL),
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;