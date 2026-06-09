<template>
  <div id="app">
    <header class="navbar">
      <div class="navbar-left">
        <button class="menu-btn" @click="toggleMenu" aria-label="Menu">
          <i class="fas fa-bars"></i>
        </button>
        <span class="brand">🎵 Musart</span>
      </div>

      <div class="navbar-center">
        <div class="search-box" :class="{ expanded: searchOpen }" @click="onSearchClick">
          <i class="fas fa-search" aria-hidden="true"></i>
          <input 
            ref="searchInput"
            type="text" 
            placeholder="Que souhaitez-vous écouter ou regarder ?"
            @input="handleSearch"
          />
        </div>
      </div>

      <div class="navbar-right">
        <div class="nav-links">
          <a href="#" class="nav-link">Assistance</a>
          <a href="#" class="nav-link">Télécharger</a>
        </div>
       <div class="divider"></div>
       <div class="nav-log-btn">
          <!-- <button class="btn-secondary">Installer l'appli</button> -->
          <button id="signup-btn" class="btn-secondary">S'inscrire</button>
          <button class="btn-primary">Se connecter</button>
       </div>
      </div>
    </header>

    <div class="main-container">
      <aside v-show="sidebarVisible" class="sidebar" :class="{ collapsed: sidebarCollapsed }">
        <nav class="sidebar-nav">
          <RouterLink to="/" @click="closeSidebarOnMobile" class="sidebar-link">
            <span class="icon"><i class="fas fa-home"></i></span>
            <span class="label">Accueil</span>
          </RouterLink>
          <RouterLink to="/songs" @click="closeSidebarOnMobile" class="sidebar-link">
            <span class="icon"><i class="fas fa-music"></i></span>
            <span class="label">Chansons</span>
          </RouterLink>
          <RouterLink to="/playlists" @click="closeSidebarOnMobile" class="sidebar-link">
            <span class="icon"><i class="fas fa-list"></i></span>
            <span class="label">Playlists</span>
          </RouterLink>
        </nav>
      </aside>

      <main class="main-content">
        <RouterView />
      </main>
    </div>

    <!-- MUSIC PLAYER -->
    <footer class="music-player">
      <div class="player-track">
        <div class="player-cover">
          <img :src="currentTrack?.thumbnail || 'https://via.placeholder.com/60x60?text=Album'" alt="Album cover" />
        </div>
        <div class="player-info">
          <div class="player-title">{{ currentTrack?.title || 'No Song Selected' }}</div>
          <div class="player-artist">{{ currentTrack?.artist || currentTrack?.uploader || 'Artist' }}</div>
        </div>
      </div>

      <div class="player-controls">
        <div class="controls">
          <button class="control-btn" title="Shuffle">
            <i class="fas fa-random"></i>
          </button>
          <button class="control-btn" title="Previous">
            <i class="fas fa-step-backward"></i>
          </button>
          <button class="control-btn play-btn" @click="togglePlay" title="Play/Pause">
            <i :class="isPlaying ? 'fas fa-pause' : 'fas fa-play'"></i>
          </button>
          <button class="control-btn" title="Next">
            <i class="fas fa-step-forward"></i>
          </button>
          <button class="control-btn" title="Repeat">
            <i class="fas fa-redo"></i>
          </button>
        </div>
        <div class="progress-container">
          <span class="time">{{ currentTimeText }}</span>
          <input 
            type="range" 
            class="progress-bar" 
            min="0" 
            :max="duration || 0" 
            :value="currentTime"
            @input="onProgressChange"
          />
          <span class="duration">{{ durationText }}</span>
        </div>
      </div>

      <div class="player-volume">
        <i class="fas fa-volume-down"></i>
        <input 
          type="range" 
          class="volume-slider" 
          min="0" 
          max="100" 
          value="80"
          @input="onVolumeChange"
        />
        <i class="fas fa-volume-up"></i>
      </div>
      <audio
        ref="audioRef"
        :src="audioSrc"
        @timeupdate="onTimeUpdate"
        @loadedmetadata="onLoadedMetadata"
        @ended="onEnded"
      />
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, provide, nextTick, watch, onMounted, onUnmounted } from 'vue'
import { RouterView, RouterLink } from 'vue-router'
import './styles/app.css'

const windowWidth = ref(window.innerWidth)
const breakpoint = ref(getBreakpoint(window.innerWidth))
const sidebarExpanded = ref(breakpoint.value === 'desktop')
const searchQuery = ref('')
const searchOpen = ref(false)
const searchInput = ref(null)
const isPlaying = ref(false)
const currentTrack = ref(null)
const currentTime = ref(0)
const duration = ref(0)
const audioRef = ref(null)

const isDesktop = computed(() => breakpoint.value === 'desktop')
const isTablet = computed(() => breakpoint.value === 'tablet')
const isMobile = computed(() => breakpoint.value === 'mobile')

const sidebarVisible = computed(() => !isMobile.value || sidebarExpanded.value)
const sidebarCollapsed = computed(() => (isDesktop.value || isTablet.value) && !sidebarExpanded.value)
const audioSrc = computed(() => {
  if (!currentTrack.value) return ''
  if (currentTrack.value.downloaded) {
    return `/media/${currentTrack.value.video_id}`
  }
  return currentTrack.value.url || ''
})

function getBreakpoint(width) {
  if (width > 1024) return 'desktop'
  if (width > 768) return 'tablet'
  return 'mobile'
}

function setCurrentTrack(track) {
  currentTrack.value = track
  isPlaying.value = true
}

provide('setCurrentTrack', setCurrentTrack)

watch(currentTrack, async () => {
  if (!audioRef.value) return
  audioRef.value.load()
  if (audioSrc.value) {
    try {
      await audioRef.value.play()
      isPlaying.value = true
    } catch {
      isPlaying.value = false
    }
  } else {
    isPlaying.value = false
  }
})

watch(isPlaying, () => {
  if (!audioRef.value) return
  if (isPlaying.value) {
    audioRef.value.play().catch(() => {
      isPlaying.value = false
    })
  } else {
    audioRef.value.pause()
  }
})

// Handle volume
function onVolumeChange(e) {
  if (!audioRef.value) return
  const volume = Number(e.target.value) / 100
  audioRef.value.volume = volume
}

function toggleMenu() {
  sidebarExpanded.value = !sidebarExpanded.value
}

function closeSidebarOnMobile() {
  if (isMobile.value) {
    sidebarExpanded.value = false
  }
}

function handleSearch(e) {
  searchQuery.value = e.target.value
}

function onSearchClick(e) {
  if (e.target && e.target.tagName === 'INPUT') return
  if (!isMobile.value) return
  searchOpen.value = !searchOpen.value
  if (searchOpen.value) {
    nextTick(() => {
      if (searchInput.value) searchInput.value.focus()
    })
  }
}

function handleClickOutside(e) {
  const searchBox = document.querySelector('.search-box')
  if (searchOpen.value && searchBox && !searchBox.contains(e.target)) {
    searchOpen.value = false
  }
}

function handleResize() {
  windowWidth.value = window.innerWidth
  const nextBreakpoint = getBreakpoint(window.innerWidth)
  if (nextBreakpoint !== breakpoint.value) {
    breakpoint.value = nextBreakpoint
    sidebarExpanded.value = nextBreakpoint === 'desktop'
  }
}

function togglePlay() {
  if (!currentTrack.value) return
  isPlaying.value = !isPlaying.value
}

function onProgressChange(e) {
  if (!audioRef.value) return
  const nextTime = Number(e.target.value)
  audioRef.value.currentTime = nextTime
  currentTime.value = nextTime
}

function onTimeUpdate() {
  if (!audioRef.value) return
  currentTime.value = audioRef.value.currentTime
}

function onLoadedMetadata() {
  if (!audioRef.value) return
  duration.value = audioRef.value.duration || 0
}

function onEnded() {
  isPlaying.value = false
}

const currentTimeText = computed(() => formatTime(currentTime.value))
const durationText = computed(() => formatTime(duration.value))

function formatTime(seconds) {
  const floored = Math.floor(seconds || 0)
  const mins = Math.floor(floored / 60)
  const secs = floored % 60
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  window.removeEventListener('resize', handleResize)
})
</script>
