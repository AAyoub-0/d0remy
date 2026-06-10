import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Song from '../views/Song.vue'
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
    path: '/songs/:id',
    name: 'Song',
    component: Song,
  },
  {
    path: '/playlists',
    name: 'Playlists',
    component: Playlists,
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
