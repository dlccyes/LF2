import { createRouter, createWebHistory, createWebHashHistory } from 'vue-router'
// import App from '../App.vue'
import Students from '@/views/Students_blade.vue'
import Student from '@/views/Student_blade.vue'
import Home from '@/views/Home_blade.vue'
import Invalid from '@/views/Invalid_blade.vue'

const routes = [
  { path: '/', component: Home},
  { path: '/students', component: Students },
  { path: '/std/:id', name: "student", component: Student },
  { path: "/:pathMatch(.*)", name: "not-found", component: Invalid },
];
const router = createRouter({
  // history: createWebHistory(import.meta.env.BASE_URL),
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;