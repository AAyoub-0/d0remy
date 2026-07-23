<template>
  <div class="song-card">
    <img :src="song.thumbnail" alt="Thumbnail" class="thumbnail" />
    <div class="song-info">
      <a href="#" class="song-title" :class="{ 'is-current-track': isCurrentTrack }">{{ song.title }}</a>
      <a href="#" class="song-artist">{{ song.artist }}</a>
    </div>
  </div>
</template>

<script setup> 
import { computed, inject } from 'vue'
import '../styles/root.css'

const props = defineProps({
  song: {
    type: Object,
    required: true,
  },
})

const currentTrack = inject('currentTrack', null)

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

const isCurrentTrack = computed(() => isSameSong(props.song, currentTrack?.value))
</script>

<style scoped>
.song-card {
  overflow: hidden;
  display: flex;
  align-items: center;
  gap: 10px;
  border-radius: 0.25rem;
}

.thumbnail {
  width: 40px;
  height: 40px;
  object-fit: cover;
  border-radius: 0.25rem;
}

.song-info {
  display: flex;
  flex-direction: column;
  min-width: 0;
  max-width: 100%;
}

.song-info a {
  text-decoration: none;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.song-info a:hover {
  text-decoration: underline;
}

.song-info .song-title {
  color: var(--primary-text);
  font-size: 0.875rem;
  font-weight: 600;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.song-info .song-title.is-current-track {
  color: var(--violet-primary);
}

.song-info .song-artist {
  color: var(--secondary-text);
  font-size: 0.775rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>