<template>
  <section v-if="selectedPlaylistId">
    <h2>Chansons de la playlist {{ selectedPlaylistId }}</h2>

    <button
      @click="$emit('load-playlist-songs', selectedPlaylistId)"
      :disabled="loadingPlaylistSongs"
    >
      Charger les chansons de playlist
    </button>

    <ul v-if="playlistSongs.length">
      <li
        v-for="song in playlistSongs"
        :key="`${song.playlist_id}-${song.video_id}`"
      >
        {{ song.video_id }} – position {{ song.position }}
      </li>
    </ul>
  </section>
</template>

<script setup>
const props = defineProps({
  selectedPlaylistId: { type: String, default: '' },
  playlistSongs: { type: Array, default: () => [] },
  loadingPlaylistSongs: { type: Boolean, default: false },
})
</script>
