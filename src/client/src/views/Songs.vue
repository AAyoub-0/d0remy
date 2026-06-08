<template>
  <div class="songs-view">
    <SongList
      :songs="songs"
      :loading-songs="loadingSongs"
      @load-songs="loadSongs"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { fetchSongs } from '../api'
import SongList from '../components/SongList.vue'

const songs = ref([])
const loadingSongs = ref(false)
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

onMounted(() => {
  loadSongs()
})
</script>
