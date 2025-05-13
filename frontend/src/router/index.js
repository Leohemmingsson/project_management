import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import About from "../views/About.vue";
import Login from "../views/Login.vue";
import NotFound from "../views/NotFound.vue"; // <-- import this

const routes = [
  { path: "/", name: "Home", component: Home },
  { path: "/about", name: "About", component: About },
  { path: "/login", name: "Login", component: Login },
  // Catch-all route for 404
  { path: "/:pathMatch(.*)*", name: "NotFound", component: NotFound },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
