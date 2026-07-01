<template>
  <section>
    <div v-if="songs.length">
      <ul>
        <li v-for="song in songs" :key="song.video_id" @click="playSong(song)">
          <div class="song-item">
            <div class="song-item-left">
              <i class="fa-solid fa-play song-card-play-icon"></i>
              <p class="song-nb">
                {{ songs.indexOf(song) + 1 }}
              </p>
            </div>
            <SongCard class="song-item-center" :song="song" />
            <div class="song-item-right">
              <span class="song-uploaded-date">{{ formatDateFr(song.metadata_created_at) }}</span>
              <span class="song-duration">{{ formatDuration(song.duration) }}</span>
            </div>
            <span class="song-more-options">
                <i class="fa-solid fa-ellipsis"></i>
            </span>
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

function formatDuration(seconds) {
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = String(seconds % 60).padStart(2, '0')

  return `${minutes}:${remainingSeconds}`
}

function formatDate(uploadDate) {
  const str = String(uploadDate)

  return `${str.slice(6, 8)}/${str.slice(4, 6)}/${str.slice(0, 4)}`
}

function formatDateFr(dateString) {
  const date = new Date(dateString)

  return new Intl.DateTimeFormat('fr-FR', {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  })
  .format(date)
  .replace('.', '') // enlève le point final parfois ajouté
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
  position: relative;
  display: flex;
  align-items: center;
  gap: 5px;
  cursor: pointer;
  border-radius: 0.25rem;
  padding: 5px;
}

  .song-item:hover {
    background-color: rgba(255, 255, 255, 0.16);
    cursor: default;
  }

.song-item-left {
  display: flex;
  align-items: center;
  padding-inline: 10px;
}

.song-nb {
  font-size: 0.875rem;
  color: var(--secondary-text);
  width: 2ch;
  text-align: center;
  font-variant-numeric: tabular-nums;
}

.song-card-play-icon {
  opacity: 0;
  font-size: 0.875rem;
  color: var(--primary-text);
  position: absolute;
  transform: all 0.2s ease;
}

.song-item:hover .song-nb {
  opacity: 0;
}

.song-item:hover .song-card-play-icon {
  opacity: 1;
}

.song-more-options {
  opacity: 0;
  transition: opacity 0.2s ease;
  font-size: 0.875rem;
  color: var(--secondary-text);
  margin-right: 10px;
}
  .song-more-options:hover {
    color: var(--primary-text);
    cursor: pointer;
  }

.song-item:hover .song-more-options {
  opacity: 1;
}

.song-item-center {
  flex: 1;
  min-width: 0;
  max-width: 100%;
}

.song-item-right {
  overflow: hidden;
  min-width: 0px;
  max-width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-inline: 10px;
  font-size: 0.875rem;
  color: var(--secondary-text);
  flex-shrink: 0;
  flex-basis: 20%;
}

.song-item-right .song-uploaded-date {
  text-decoration: none;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>