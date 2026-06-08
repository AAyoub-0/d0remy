<template>
  <section>
    <button @click="$emit('load-playlists')" :disabled="loadingPlaylists">
      Charger les playlists
    </button>

    <div v-if="playlists.length">
      <h2>Playlists</h2>
      <ul>
        <li v-for="playlist in playlists" :key="playlist.playlist_id">
          <button @click="$emit('select-playlist', playlist.playlist_id)">
            {{ playlist.title || playlist.playlist_id }}
          </button>
        </li>
      </ul>
    </div>
  </section>
</template>

<script setup>
const props = defineProps({
  playlists: { type: Array, default: () => [] },
  loadingPlaylists: { type: Boolean, default: false },
})
</script>
