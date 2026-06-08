<template>
  <section>
    <button @click="$emit('load-songs')" :disabled="loadingSongs">
      Charger les chansons
    </button>

    <div v-if="songs.length">
      <h2>Chansons</h2>
      <ul>
        <li v-for="song in songs" :key="song.video_id">
          {{ song.title }} — {{ song.artist || song.uploader }}
        </li>
      </ul>
    </div>
  </section>
</template>

<script setup>
const props = defineProps({
  songs: { type: Array, default: () => [] },
  loadingSongs: { type: Boolean, default: false },
})
</script>
