<template>
  <div class="playlists-view">
    <PlaylistList
      :playlists="playlists"
      :loading-playlists="loadingPlaylists"
      @load-playlists="loadPlaylists"
      @select-playlist="selectPlaylist"
    />

    <PlaylistSongs
      :selected-playlist-id="selectedPlaylistId"
      :playlist-songs="playlistSongs"
      :loading-playlist-songs="loadingPlaylistSongs"
      @load-playlist-songs="loadPlaylistSongs"
    />

    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { fetchPlaylists, fetchPlaylistSongs } from '../api'
import PlaylistList from '../components/PlaylistList.vue'
import PlaylistSongs from '../components/PlaylistSongs.vue'

const playlists = ref([])
const playlistSongs = ref([])
const selectedPlaylistId = ref(null)
const loadingPlaylists = ref(false)
const loadingPlaylistSongs = ref(false)
const error = ref(null)

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

onMounted(() => {
  loadPlaylists()
})
</script>
