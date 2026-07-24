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

      <div class="right-container">
        <div class="right-content">
          <RouterView name="right" />
        </div>
      </div>
    </div>

    <!-- MUSIC PLAYER -->
    <footer class="music-player">
      <div class="player-track">
        <div class="player-cover">
          <img :src="currentTrack?.thumbnail || 'https://via.placeholder.com/60x60?text=Album'" alt="Album cover" />
        </div>
        <div class="player-info">
          <div class="player-title" ref="playerTitleContainer">
            <span ref="playerTitle"
                  :style="{ '--titleOverflow': `${titleOverflow}px` }">
              {{ currentTrack?.title || 'No Song Selected' }}
            </span>
          </div>
          <div class="player-artist" ref="playerArtistContainer">
            <span ref="playerArtist"
                  :style="{ '--artistOverflow': `${artistOverflow}px` }">
              {{ currentTrack?.artist || currentTrack?.uploader || 'Artist' }}
            </span>
          </div>
        </div>
      </div>

      <div class="player-controls">
        <div class="controls">
          <button class="control-btn" title="Shuffle">
            <i class="fas fa-random"></i>
          </button>
          <button class="control-btn" @click="playPrevious" title="Previous">
            <i class="fas fa-step-backward"></i>
          </button>
          <button class="control-btn play-btn" @click="togglePlay" title="Play/Pause">
            <i :class="isPlaying ? 'fas fa-pause' : 'fas fa-play'"></i>
          </button>
          <button class="control-btn" @click="playNext" title="Next">
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
            @mousemove="onProgressHover"
            @mouseleave="clearProgressHover"
            :style="progressStyle"
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
          :value="volume"
          @input="onVolumeChange"
          @mousemove="onVolumeHover"
          @mouseleave="clearVolumeHover"
          :style="volumeStyle"
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
import './styles/header.css'

// css for the scrolling title
const playerTitle = ref(null)
const playerTitleContainer = ref(null)
const playerArtist = ref(null)
const playerArtistContainer = ref(null)
const titleOverflow = ref(0)
const artistOverflow = ref(0)

const windowWidth = ref(window.innerWidth)
const breakpoint = ref(getBreakpoint(window.innerWidth))
const sidebarExpanded = ref(breakpoint.value === 'desktop')
const searchQuery = ref('')
const searchOpen = ref(false)
const searchInput = ref(null)
const isPlaying = ref(false)
const currentTrack = ref(null)
const playbackQueue = ref([])
const playbackIndex = ref(-1)
const currentTime = ref(0)
const duration = ref(0)
const audioRef = ref(null)
const volume = ref(80)
const progressHoverPercent = ref(null)
const volumeHoverPercent = ref(null)

const isDesktop = computed(() => breakpoint.value === 'desktop')
const isTablet = computed(() => breakpoint.value === 'tablet')
const isMobile = computed(() => breakpoint.value === 'mobile')

const sidebarVisible = computed(() => !isMobile.value || sidebarExpanded.value)
const sidebarCollapsed = computed(() => (isDesktop.value || isTablet.value) && !sidebarExpanded.value)
const audioSrc = computed(() => {
  if (!currentTrack.value) return ''
  if (currentTrack.value.downloaded) {
    return `/media/${currentTrack.value.song_id}`
  }
  return currentTrack.value.url || ''
})

function getBreakpoint(width) {
  if (width > 1024) return 'desktop'
  if (width > 768) return 'tablet'
  return 'mobile'
}

function updatePlaybackContext(track, options = {}) {
  const queue = Array.isArray(options.queue) ? options.queue : []
  if (queue.length) {
    playbackQueue.value = queue
    const requestedIndex = Number(options.index)
    if (Number.isInteger(requestedIndex) && requestedIndex >= 0 && requestedIndex < queue.length) {
      playbackIndex.value = requestedIndex
    } else {
      playbackIndex.value = queue.findIndex(item => item?.song_id === track?.song_id)
    }
    return
  }

  if (track?.song_id) {
    const existingIndex = playbackQueue.value.findIndex(item => item?.song_id === track.song_id)
    if (existingIndex >= 0) {
      playbackIndex.value = existingIndex
      return
    }
  }

  playbackQueue.value = track ? [track] : []
  playbackIndex.value = track ? 0 : -1
}

function setCurrentTrack(track, options = {}) {
  currentTrack.value = track
  updatePlaybackContext(track, options)
  isPlaying.value = true
}

async function playTrackAt(index) {
  if (!Array.isArray(playbackQueue.value) || !playbackQueue.value.length) return
  if (index < 0 || index >= playbackQueue.value.length) return

  const nextTrack = playbackQueue.value[index]
  if (!nextTrack) return

  playbackIndex.value = index
  currentTrack.value = nextTrack
  isPlaying.value = false

  // Ensure playback starts immediately on explicit next/previous actions.
  await nextTick()
  if (!audioRef.value) return

  audioRef.value.load()
  try {
    await audioRef.value.play()
    isPlaying.value = true
  } catch {
    isPlaying.value = false
  }
}

function playNext() {
  if (!playbackQueue.value.length) return
  const nextIndex = playbackIndex.value + 1
  if (nextIndex >= playbackQueue.value.length)
    nextIndex = 0 // Loop back to the first track if at the end
  playTrackAt(nextIndex)
}

function playPrevious() {
  if (!playbackQueue.value.length) return
  const previousIndex = playbackIndex.value - 1
  if (previousIndex < 0)
    previousIndex = playbackQueue.value.length - 1 // Loop back to the last track if at the beginning
  playTrackAt(previousIndex)
}

function seekTo(time) {
  if (!audioRef.value) return

  const targetDuration = Number(duration.value || currentTrack.value?.duration || 0)
  const safeTime = Math.max(0, Math.min(targetDuration, Number(time) || 0))

  audioRef.value.currentTime = safeTime
  currentTime.value = safeTime
}

provide('currentTrack', currentTrack)
provide('currentTime', currentTime)
provide('currentDuration', duration)
provide('setCurrentTrack', setCurrentTrack)
provide('isPlaying', isPlaying)
provide('togglePlay', togglePlay)
provide('setPlaybackState', setPlaybackState)
provide('seekTo', seekTo)

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

watch(() => currentTrack.value?.title, async () => {
    await nextTick()

    if (!playerTitle.value || !playerTitleContainer.value) return

    titleOverflow.value = Math.max(
      0,
      playerTitle.value.scrollWidth - playerTitleContainer.value.clientWidth
    )
    artistOverflow.value = Math.max(
      0,
      playerArtist.value.scrollWidth - playerArtistContainer.value.clientWidth
    )
  },
  { immediate: true }
)

// Handle volume
function onVolumeChange(e) {
  if (!audioRef.value) return
  const next = Number(e.target.value)
  volume.value = Math.max(0, Math.min(100, Number.isFinite(next) ? next : 0))
  audioRef.value.volume = volume.value / 100
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

function setPlaybackState(shouldPlay) {
  if (!currentTrack.value) return
  isPlaying.value = Boolean(shouldPlay)
}

function onProgressChange(e) {
  if (!audioRef.value) return
  const nextTime = Number(e.target.value)
  audioRef.value.currentTime = nextTime
  currentTime.value = nextTime
}

function clampPercent(value) {
  return Math.min(100, Math.max(0, Number.isFinite(value) ? value : 0))
}

function getRangeHoverPercent(event, maxValue) {
  const input = event.currentTarget
  const max = Number(maxValue || 0)
  if (!input || !max || max <= 0) {
    return null
  }

  const rect = input.getBoundingClientRect()
  if (!rect.width) {
    return null
  }

  const ratio = Math.min(1, Math.max(0, (event.clientX - rect.left) / rect.width))
  return clampPercent(ratio * 100)
}

function onProgressHover(event) {
  progressHoverPercent.value = getRangeHoverPercent(event, duration.value)
}

function clearProgressHover() {
  progressHoverPercent.value = null
}

function onVolumeHover(event) {
  volumeHoverPercent.value = getRangeHoverPercent(event, 100)
}

function clearVolumeHover() {
  volumeHoverPercent.value = null
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
  const nextIndex = playbackIndex.value + 1
  if (nextIndex >= 0 && nextIndex < playbackQueue.value.length) {
    playTrackAt(nextIndex)
    return
  }
  isPlaying.value = false
}

const currentTimeText = computed(() => formatTime(currentTime.value))
const durationText = computed(() => formatTime(duration.value))

const progressPercent = computed(() => {
  const d = Number(duration.value || 0)
  const t = Number(currentTime.value || 0)
  if (!d || d <= 0) return 0
  return Math.min(100, Math.max(0, (t / d) * 100))
})

const progressStyle = computed(() => {
  const filled = progressPercent.value
  const hovered = progressHoverPercent.value

  if (hovered === null) {
    return {
      background: `linear-gradient(90deg, var(--violet-primary) ${filled}%, var(--tertiary-bg) ${filled}%)`
    }
  }

  if (hovered >= filled) {
    return {
      background: `linear-gradient(90deg, var(--violet-primary) ${filled}%, var(--secondary-text) ${filled}%, var(--secondary-text) ${hovered}%, var(--tertiary-bg) ${hovered}%)`
    }
  }

  return {
    background: `linear-gradient(90deg, var(--violet-primary) ${hovered}%, var(--secondary-text) ${hovered}%, var(--secondary-text) ${filled}%, var(--tertiary-bg) ${filled}%)`
  }
})

const volumePercent = computed(() => Math.min(100, Math.max(0, Number(volume.value || 0))))

const volumeStyle = computed(() => {
  const filled = volumePercent.value
  const hovered = volumeHoverPercent.value

  if (hovered === null) {
    return {
      background: `linear-gradient(90deg, var(--violet-primary) ${filled}%, var(--tertiary-bg) ${filled}%)`
    }
  }

  if (hovered >= filled) {
    return {
      background: `linear-gradient(90deg, var(--violet-primary) ${filled}%, var(--secondary-text) ${filled}%, var(--secondary-text) ${hovered}%, var(--tertiary-bg) ${hovered}%)`
    }
  }

  return {
    background: `linear-gradient(90deg, var(--violet-primary) ${hovered}%, var(--secondary-text) ${hovered}%, var(--secondary-text) ${filled}%, var(--tertiary-bg) ${filled}%)`
  }
})

function formatTime(seconds) {
  const floored = Math.floor(seconds || 0)
  const mins = Math.floor(floored / 60)
  const secs = floored % 60
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  window.addEventListener('resize', handleResize)
  if (audioRef.value) {
    audioRef.value.volume = Math.max(0, Math.min(1, Number(volume.value || 80) / 100))
  }
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  window.removeEventListener('resize', handleResize)
})
</script>
