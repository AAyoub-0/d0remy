<template>
  <section>
    <div v-if="songs.length">
      <h2>Chansons</h2>
      <ul>
        <li v-for="song in songs" :key="song.video_id" @click="playSong(song)">
          <div class="song-item">
            <p class="song-nb">
              <i class="fa-solid fa-play song-card-play-icon"></i>
              <span class="song-number">{{ songs.indexOf(song) + 1 }}</span>
            </p>
            <SongCard :song="song" />
          </div>
        </li>
      </ul>
    </div>
  </section>
</template>

<script setup>
import { inject } from 'vue'
import SongCard from './SongCard.vue'

const props = defineProps({
  songs: { type: Array, default: () => [] },
  loadingSongs: { type: Boolean, default: false },
})

const setCurrentTrack = inject('setCurrentTrack', () => {})

function playSong(song) {
  setCurrentTrack(song)
}
</script>

<style scoped>
ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

li {
  list-style: none;
  margin: 0px;
  padding: 0px;
  border: none;
  cursor: default;
}
li:last-child {
  border-bottom: none;
}
li:hover {
  cursor: default;
}

.song-item {
  display: flex;
  align-items: center;
  gap: 5px;
  border-radius: 0.25rem;
  cursor: pointer;
  padding-block: 5px;
}

  .song-item:hover {
    background-color: rgba(255, 255, 255, 0.16);
    cursor: default;
  }

.song-nb {
  position: relative;
  font-size: 0.875rem;
  color: var(--secondary-text);
  width: 30px;
  text-align: center;
  margin-right: 10px;
}

.song-card-play-icon {
  opacity: 0;
  font-size: 0.875rem;
  color: var(--primary-text);
  position: absolute;
  transform: all 0.2s ease;
}

.song-item:hover .song-number {
  opacity: 0;
}

.song-item:hover .song-card-play-icon {
  opacity: 1;
}
</style>