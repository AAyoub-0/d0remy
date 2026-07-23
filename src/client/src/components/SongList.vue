<template>
  <section>
    <div v-if="songs.length">
      <ul>
        <li v-for="(song, index) in songs" :key="song.video_id" @click="playSong(song)">
          <div class="song-item">
            <div class="song-item-left">
              <i
                class="song-card-play-icon"
                :class="getHoverIconClass(song)"
                @click.stop="onIndexIconClick(song)"
              ></i>
              <div
                v-if="isCurrentTrack(song)"
                class="song-current-cube"
                aria-hidden="true"
              >
                <div class="cube-cell cube-cell-top-left" :style="{ opacity: getCubeOpacity(song, 2) }"></div>
                <div class="cube-cell cube-cell-top-right" :style="{ opacity: getCubeOpacity(song, 3) }"></div>
                <div class="cube-cell cube-cell-bottom-left" :style="{ opacity: getCubeOpacity(song, 0) }"></div>
                <div class="cube-cell cube-cell-bottom-right" :style="{ opacity: getCubeOpacity(song, 1) }"></div>
              </div>
              <p v-else class="song-nb">
                {{ index + 1 }}
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
const currentTrack = inject('currentTrack', null)
const currentTimeRef = inject('currentTime', null)
const currentDurationRef = inject('currentDuration', null)
const isPlaying = inject('isPlaying', null)
const setPlaybackState = inject('setPlaybackState', null)
const togglePlay = inject('togglePlay', () => {})

function isSameSong(left, right) {
  if (!left || !right) return false

  if (left.video_id && right.video_id) {
    return left.video_id === right.video_id
  }

  if (left.url && right.url) {
    return left.url === right.url
  }

  return left.title === right.title && left.artist === right.artist
}

function isCurrentTrack(song) {
  return isSameSong(song, currentTrack?.value)
}

function clamp(value, min = 0, max = 1) {
  return Math.min(max, Math.max(min, Number.isFinite(value) ? value : 0))
}

function getCurrentTrackProgress(song) {
  if (!isCurrentTrack(song)) return 0

  const duration = Number(currentDurationRef?.value || song?.duration || 0)
  const currentTime = Number(currentTimeRef?.value || 0)
  if (!duration || duration <= 0) return 0

  return clamp(currentTime / duration)
}

function getSteppedOpacity(localProgress) {
  if (localProgress <= 0) return 0
  if (localProgress < (1 / 3)) return 0.3
  if (localProgress < (2 / 3)) return 0.7
  return 1
}

function getCubeOpacity(song, orderIndex) {
  const progress = getCurrentTrackProgress(song)
  const localProgress = clamp((progress * 4) - orderIndex)
  return getSteppedOpacity(localProgress)
}

function getHoverIconClass(song) {
  if (!isCurrentTrack(song)) return 'fa-solid fa-play'
  return isPlaying?.value ? 'fa-solid fa-pause' : 'fa-solid fa-play'
}

function onIndexIconClick(song) {
  if (isCurrentTrack(song)) {
    if (isPlaying?.value) {
      if (typeof setPlaybackState === 'function') {
        setPlaybackState(false)
      } else {
        togglePlay()
      }
    } else {
      if (typeof setPlaybackState === 'function') {
        setPlaybackState(true)
      } else {
        togglePlay()
      }
    }
    return
  }

  playSong(song)
}

function playSong(song) {
  const queue = Array.isArray(props.songs) ? props.songs : []
  const index = queue.findIndex(item => item?.video_id === song?.video_id)
  setCurrentTrack(song, { queue, index })
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
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
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
  z-index: 2;
  transition: opacity 0.2s ease;
}

.song-current-cube {
  width: 12px;
  height: 12px;
  display: grid;
  position: absolute;
  z-index: 2;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
  border: 1px solid rgba(255, 255, 255, 0.45);
  pointer-events: none;
}

.song-current-cube .cube-cell {
  width: 100%;
  height: 100%;
  background-color: var(--violet-primary);
  transition: opacity 0.2s ease;
  opacity: 0;
}

.song-item:hover .song-nb {
  opacity: 0;
}

.song-item:hover .song-current-cube {
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