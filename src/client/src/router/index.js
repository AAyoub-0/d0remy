import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Songs from '../views/Songs.vue'
import Playlists from '../views/Playlists.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/songs',
    name: 'Songs',
    component: Songs,
  },
  {
    path: '/playlists',
    name: 'Playlists',
    component: Playlists,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
