<template>
  <section>
    <button @click="$emit('load-songs')" :disabled="loadingSongs">
      Charger les chansons
    </button>

    <div v-if="songs.length">
      <h2>Chansons</h2>
      <ul>
        <li v-for="song in songs" :key="song.video_id" @click="playSong(song)">
          {{ song.title }} — {{ song.artist || song.uploader }}
        </li>
      </ul>
    </div>
  </section>
</template>

<script setup>
import { inject } from 'vue'

const props = defineProps({
  songs: { type: Array, default: () => [] },
  loadingSongs: { type: Boolean, default: false },
})

const setCurrentTrack = inject('setCurrentTrack', () => {})

function playSong(song) {
  setCurrentTrack(song)
}
</script>
