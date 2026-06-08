<template>
  <div class="home">
    <h2>Bienvenue</h2>
    <p>Sélectionnez une option dans le menu pour explorer la musique.</p>
    <div class="links">
      <RouterLink to="/songs">📀 Voir les chansons</RouterLink>
      <RouterLink to="/playlists">📋 Voir les playlists</RouterLink>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>

<style scoped>
.home {
  text-align: center;
  padding: 2rem;
}

.links {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 1.5rem;
  flex-wrap: wrap;
}

a {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  background: #f7f8ff;
  border: 1px solid #6671a1;
  border-radius: 0.75rem;
  color: #111;
  text-decoration: none;
  transition: background 0.2s ease;
}

a:hover {
  background: #e5e7ff;
}
</style>
