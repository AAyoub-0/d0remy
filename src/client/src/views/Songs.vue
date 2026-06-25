<template>
  <div class="songs-view">
    <div class="song-list-header">
        <div class="header-left">
          <span>#</span>
        </div>

        <div class="header-center">
          <span class="sortBy-text" :class="{ active: sortBy === 'title' }" @click="setSort('title')">
            Titre
          </span>
          <div class="small-search-box">
            <i class="fas fa-search" aria-hidden="true"></i>
            <input
                v-model="search"
                type="text"
                placeholder="Rechercher une musique"
              />
          </div>
        </div>

        <div class="header-right">
          <span class="sortBy-text" :class="{ active: sortBy === 'added_at' }" @click="setSort('added_at')">
            Date d'ajout
          </span>
          <span class="sortBy-text" :class="{ active: sortBy === 'duration' }" @click="setSort('duration')">
            Durée
          </span>
        </div>
        <div class="header-empty-cell"></div>
    </div>

    <SongList
      :songs="filteredSongs"
      :loading-songs="loadingSongs"
      @load-songs="loadSongs"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { fetchSongs } from '../api'
import SongList from '../components/SongList.vue'

const songs = ref([])
const loadingSongs = ref(false)
const error = ref(null)

const search = ref('')
const sortBy = ref('title')
const sortOrder = ref('desc')

function setSort(sortField) {
  if (sortBy.value === sortField) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortBy.value = sortField
    sortOrder.value = 'asc'
  }
}

const filteredSongs = computed(() => {
  let result = [...songs.value]

  // Recherche
  if (search.value.trim()) {
    const query = search.value.toLowerCase()

    result = result.filter(song =>
      song.title?.toLowerCase().includes(query) ||
      song.artist?.toLowerCase().includes(query)
    )
  }

  // Tri
  result.sort((a, b) => {
    switch (sortBy.value) {
      case 'title':
        return (a.title || '').localeCompare(b.title || '')

      case 'duration':
        return (a.duration || 0) - (b.duration || 0)

      case 'added_at':
        return (
          new Date(a.metadata_created_at || a.metadata_created_at || 0) -
          new Date(b.metadata_created_at || b.metadata_created_at || 0)
        )

      default:
        return 0
    }
  })

  if (sortOrder.value === 'desc') {
    result.reverse()
  }

  return result
})

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

<style scoped>
.song-list-header {
  display: flex;
  align-items: center;
  gap: 5px;
  width: 100%;
  padding: 5px;

  position: sticky;
  top: 0;
  background-color: var(--primary-bg);
  z-index: 10;
  border-bottom: 2px solid rgba(255, 255, 255, 0.3);
}

.small-search-box {
  display: flex;
  align-items: center;
  background: #000;
  /* border: 1px solid var(--secondary-bg); */
  border-radius: 0.25rem;
  padding: 0.45rem 0.45rem;
  gap: 0.55rem;
  width: 100%;
  max-width: 200px;
  transition: all 0.2s ease;
  color: var(--secondary-text);
  overflow: hidden;
}

.small-search-box:hover {
  color: var(--primary-text);
  border-color: var(--accent);
  background-color: rgba(255, 255, 255, 0.15);
}

.small-search-box i {
  color: inherit;
  font-size: 0.9rem;
}

.small-search-box input {
  color: inherit;
  background: transparent;
  border: none;
  outline: none;
  font-size: 0.9rem;
  width: 100%;
}

.sortBy-text {
  z-index: 50;
  position: relative;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
  color: var(--secondary-text);
  font-size: 0.85rem;
}
  .sortBy-text:hover {
    color: var(--primary-text);
  }
  .sortBy-text.active {
    color: var(--primary-text);
  }

.header-left {
  display: flex;
  align-items: center;
  padding-inline: 10px;
  color: var(--secondary-text);
}

.header-center {
  display: flex;
  align-items: center;
  /* justify-content: space-between; */
  gap: 2rem;
  flex: 1;
}

.header-right {
  overflow: hidden;
  min-width: 0px;
  max-width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-inline: 10px;
  flex-basis: 20%;
  flex-shrink: 0;
}
  .header-right .sortBy-text {
    text-decoration: none;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

.header-empty-cell {
  margin-right: 10px;
  width: 14px;
}
</style>