<template>
  <div id="app">
    <header class="navbar">
      <div class="navbar-left">
        <button class="menu-btn" @click="toggleMenu" aria-label="Menu">
          <i class="fas fa-bars"></i>
        </button>
        <span class="brand">🎵 AnBeats</span>
      </div>

      <div class="navbar-center">
        <div class="search-box" :class="{ expanded: searchOpen }" @click="onSearchClick">
          <i class="fas fa-search" aria-hidden="true"></i>
          <input 
            ref="searchInput"
            type="text" 
            placeholder="Que souhaitez-vous écouter ou regarder ?"
            @input="handleSearch"
          />
        </div>
      </div>

      <div class="navbar-right">
        <div class="nav-links">
          <a href="#" class="nav-link">Assistance</a>
          <a href="#" class="nav-link">Télécharger</a>
        </div>
       <div class="divider"></div>
       <div class="nav-log-btn">
          <!-- <button class="btn-secondary">Installer l'appli</button> -->
          <button id="signup-btn" class="btn-secondary">S'inscrire</button>
          <button class="btn-primary">Se connecter</button>
       </div>
      </div>
    </header>

    <div class="main-container">
      <aside v-if="menuOpen" class="sidebar">
        <nav class="sidebar-nav">
          <RouterLink to="/" @click="menuOpen = false">🏠 Accueil</RouterLink>
          <RouterLink to="/songs" @click="menuOpen = false">🎵 Chansons</RouterLink>
          <RouterLink to="/playlists" @click="menuOpen = false">📋 Playlists</RouterLink>
        </nav>
      </aside>

      <main class="main-content">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted, onUnmounted } from 'vue'
import { RouterView, RouterLink } from 'vue-router'
import './styles/app.css'

const menuOpen = ref(false)
const searchQuery = ref('')
const searchOpen = ref(false)
const searchInput = ref(null)

function toggleMenu() {
  menuOpen.value = !menuOpen.value
}

function handleSearch(e) {
  searchQuery.value = e.target.value
  // À intégrer avec la logique de recherche plus tard
}

function onSearchClick(e) {
  if (e.target && e.target.tagName === 'INPUT') return
  if (window.innerWidth > 768) return
  searchOpen.value = !searchOpen.value
  if (searchOpen.value) {
    nextTick(() => {
      if (searchInput.value) searchInput.value.focus()
    })
  }
}

function handleClickOutside(e) {
  const searchBox = document.querySelector('.search-box')
  if (searchOpen.value && searchBox && !searchBox.contains(e.target)) {
    searchOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>
