<template>
  <div class="song-view">
    <SongCard :song="song" />
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { ref, onMounted } from 'vue'
import { fetchSong } from '../api'
import SongCard from '../components/SongCard.vue'

const route = useRoute()
const song = ref(null)
const error = ref(null)
const loadingSong = ref(false)

async function loadSong(id) {
  error.value = null
  loadingSong.value = true
  try {
    song.value = await fetchSong(id)
  } catch (err) {
    error.value = err.message
  } finally {
    loadingSong.value = false
  }
}

onMounted(() => {
  const songId = route.query.id
  if (songId) {
    loadSong(songId)
  }
})
</script>