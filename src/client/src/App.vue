<template>
  <main>
    <h1>YT Music Client</h1>

    <section>
      <button @click="loadSongs" :disabled="loadingSongs">Charger les chansons</button>
      <div v-if="songs.length">
        <h2>Chansons</h2>
        <ul>
          <li v-for="song in songs" :key="song.video_id">
            {{ song.title }} — {{ song.artist || song.uploader }}
          </li>
        </ul>
      </div>
    </section>

    <section>
      <button @click="loadPlaylists" :disabled="loadingPlaylists">Charger les playlists</button>
      <div v-if="playlists.length">
        <h2>Playlists</h2>
        <ul>
          <li v-for="playlist in playlists" :key="playlist.playlist_id">
            <button @click="selectPlaylist(playlist.playlist_id)">
              {{ playlist.title || playlist.playlist_id }}
            </button>
          </li>
        </ul>
      </div>
    </section>

    <section v-if="selectedPlaylistId">
      <h2>Chansons de la playlist {{ selectedPlaylistId }}</h2>
      <button @click="loadPlaylistSongs(selectedPlaylistId)" :disabled="loadingPlaylistSongs">
        Charger les chansons de playlist
      </button>
      <ul v-if="playlistSongs.length">
        <li v-for="song in playlistSongs" :key="`${song.playlist_id}-${song.video_id}`">
          {{ song.video_id }} – position {{ song.position }}
        </li>
      </ul>
    </section>

    <div v-if="error" class="error">Erreur : {{ error }}</div>
  </main>
</template>

<script setup>
import { ref } from 'vue'
import { fetchSongs, fetchPlaylists, fetchPlaylistSongs } from './api'

const songs = ref([])
const playlists = ref([])
const playlistSongs = ref([])
const selectedPlaylistId = ref(null)
const loadingSongs = ref(false)
const loadingPlaylists = ref(false)
const loadingPlaylistSongs = ref(false)
const error = ref(null)

async function loadSongs() {
  error.value = null
  loadingSongs.value = true
  try {
    songs.value = await fetchSongs()
  } catch (err) {
    error.value = err.message
  } finally {
    loadingSongs.value = false
  }
}

async function loadPlaylists() {
  error.value = null
  loadingPlaylists.value = true
  try {
    playlists.value = await fetchPlaylists()
  } catch (err) {
    error.value = err.message
  } finally {
    loadingPlaylists.value = false
  }
}

function selectPlaylist(playlistId) {
  selectedPlaylistId.value = playlistId
  playlistSongs.value = []
}

async function loadPlaylistSongs(playlistId) {
  error.value = null
  loadingPlaylistSongs.value = true
  try {
    playlistSongs.value = await fetchPlaylistSongs(playlistId)
  } catch (err) {
    error.value = err.message
  } finally {
    loadingPlaylistSongs.value = false
  }
}
</script>

<style>
main {
  max-width: 800px;
  margin: 2rem auto;
  font-family: Arial, sans-serif;
  padding: 0 1rem;
}
button {
  margin: 0.5rem 0;
  padding: 0.5rem 1rem;
}
.error {
  margin-top: 1rem;
  color: #a00;
}
</style>
