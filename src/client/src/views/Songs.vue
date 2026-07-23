<template>
  <div class="songs-view">

    <div class="songs-view-header">
      <div class="visualizer-card" :style="visualizerCardStyle" v-if="visualizerBars.length">

        <div class="visualizer-left">
          <div class="visualizer-thumbnail" v-if="activeVisualizerSong?.thumbnail">
            <img :src="activeVisualizerSong.thumbnail" alt="Album cover" />
          </div>
        </div>

        <div class="visualizer-right">
          <div class="visualizer-header">
            <div class="visualizer-label">
              <span v-if="activeVisualizerSong" class="visualizer-song">{{ activeVisualizerSong.title }}</span>
              <span v-if="activeVisualizerSong" class="visualizer-artist">{{ activeVisualizerSong.artist }}</span>
            </div>

            <div class="visualizer-actions">
              <button
                class="visualizer-actions-button"
                v-if="activeVisualizerSong"
                @click="$emit('like-song', activeVisualizerSong)"
                aria-label="Aimer"
              >
                <i class="fa-regular fa-heart" aria-hidden="true"></i>
                <span class="visualizer-tooltip" aria-hidden="true">Aimer</span>
              </button>
              <button
                class="visualizer-actions-button"
                v-if="activeVisualizerSong"
                @click="$emit('add-to-playlist', activeVisualizerSong)"
                aria-label="Ajouter à la playlist"
              >
                <i class="fa-solid fa-plus" aria-hidden="true"></i>
                <span class="visualizer-tooltip" aria-hidden="true">Ajouter à une playlist</span>
              </button>
              <button
                class="visualizer-actions-button"
                v-if="activeVisualizerSong"
                @click="$emit('download-song', activeVisualizerSong)"
                aria-label="Télécharger"
              >
                <i class="fa-solid fa-download" aria-hidden="true"></i>
                <span class="visualizer-tooltip" aria-hidden="true">Télécharger</span>
              </button>
              <button
                class="visualizer-actions-button"
                v-if="activeVisualizerSong"
                @click="$emit('share-song', activeVisualizerSong)"
                aria-label="Partager"
              >
                <i class="fa-solid fa-share-nodes" aria-hidden="true"></i>
                <span class="visualizer-tooltip" aria-hidden="true">Partager</span>
              </button>
              <button
                class="visualizer-actions-button"
                v-if="activeVisualizerSong"
                @click="$emit('more-options', activeVisualizerSong)"
                aria-label="Plus d'options"
              >
                <i class="fa-solid fa-ellipsis" aria-hidden="true"></i>
                <span class="visualizer-tooltip" aria-hidden="true">Plus d'options</span>
              </button>
            </div>
          </div>

          <div ref="visualizerContainer" class="visualizer-shell">
            <canvas ref="visualizerCanvas" class="visualizer-bars" @click="handleVisualizerClick"></canvas>
            <div class="visualizer-timer visualizer-timer-left">{{ currentTimeText }}</div>
            <div class="visualizer-timer visualizer-timer-right">{{ durationText }}</div>
          </div>
        </div>
      </div>

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
    </div>
    

    <SongList
      :songs="filteredSongs"
      :loading-songs="loadingSongs"
      @load-songs="loadSongs"
      class="song-list"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, inject } from 'vue'
import { fetchSongs } from '../api'
import SongList from '../components/SongList.vue'
import { Vibrant } from 'node-vibrant/browser'

const songs = ref([])
const loadingSongs = ref(false)
const error = ref(null)
const currentTrack = inject('currentTrack', null)
const currentTimeRef = inject('currentTime', ref(0))
const currentDurationRef = inject('currentDuration', ref(0))
const seekTo = inject('seekTo', null)
const visualizerContainer = ref(null)
const visualizerCanvas = ref(null)
const visualizerWidth = ref(0)
const visualizerBackgroundStyle = ref('')
let resizeObserver = null

function colorToRgb(cssColor) {
  if (Array.isArray(cssColor)) {
    return `rgb(${cssColor[0]}, ${cssColor[1]}, ${cssColor[2]})`
  }
  return String(cssColor).trim()
}

function getGradientFromPalette(palette) {
  if (!palette) {
    return ''
  }

  const swatches = [
    palette.Vibrant,
    palette.DarkVibrant,
    palette.Muted,
    palette.LightVibrant,
    palette.DarkMuted,
  ].filter(Boolean)

  if (!swatches.length) {
    return ''
  }

  const colors = swatches.map(swatch => colorToRgb(swatch.rgb))

  if (colors.length === 1) {
    return `linear-gradient(135deg, ${colors[0]} 0%, ${colors[0]} 100%)`
  }

  if (colors.length === 2) {
    return `linear-gradient(135deg, ${colors[0]} 0%, ${colors[1]} 75%)`
  }

  return `linear-gradient(135deg, ${colors[1]} 0%, ${colors[1]} 100%)`
}

async function refreshVisualizerBackground(song) {
  visualizerBackgroundStyle.value = ''
  if (!song?.thumbnail) {
    console.log('No thumbnail available for song:', song)
    return
  }

  try {
    const image = new Image()
    image.crossOrigin = 'anonymous'
    image.src = song.thumbnail

    await new Promise((resolve, reject) => {
      image.onload = resolve
      image.onerror = reject
    })

    const palette = await Vibrant.from(image).getPalette()
    const gradient = getGradientFromPalette(palette)
    visualizerBackgroundStyle.value = gradient || ''
  } catch (err) {
    console.error('Error generating visualizer background:', err)
    visualizerBackgroundStyle.value = ''
  }
}

const search = ref('')
const sortBy = ref('title')
const sortOrder = ref('desc')

const fallbackBars = [0.2, 0.35, 0.55, 0.26, 0.7, 0.38, 0.62, 0.3, 0.68, 0.24, 0.45, 0.72]

function clamp(value, min = 0, max = 1) {
  return Math.min(max, Math.max(min, value))
}

function interpolateBars(values, targetCount) {
  if (!Array.isArray(values) || !values.length) {
    return []
  }

  if (targetCount <= 1) {
    return [clamp(values[0] ?? 0)]
  }

  const result = []
  for (let index = 0; index < targetCount; index += 1) {
    const position = index / Math.max(1, targetCount - 1)
    const rawIndex = position * (values.length - 1)
    const lowerIndex = Math.floor(rawIndex)
    const upperIndex = Math.min(values.length - 1, lowerIndex + 1)
    const weight = rawIndex - lowerIndex
    const lowerValue = values[lowerIndex] ?? 0
    const upperValue = values[upperIndex] ?? lowerValue
    result.push(clamp(lowerValue + (upperValue - lowerValue) * weight))
  }

  return result
}

function getTargetBarCount() {
  if (!visualizerWidth.value) {
    return 56
  }

  // Reduce bar width by roughly 30% while keeping the same gap spacing
  // so the canvas is still filled entirely.
  return Math.max(40, Math.min(260, Math.floor(visualizerWidth.value / 3.4)))
}

function normalizeBarsToPeak(values) {
  if (!Array.isArray(values) || !values.length) {
    return []
  }

  const normalizedSource = values.map(value => clamp(Number(value) || 0))
  const peak = normalizedSource.reduce((maxValue, value) => Math.max(maxValue, value), 0)
  if (peak <= 0) {
    return normalizedSource.map(() => 0)
  }

  const normalized = normalizedSource.map(value => clamp(value / peak))

  // Adaptive gamma keeps the original waveform shape while scaling it to use
  // more canvas height when the track energy is globally low.
  const sorted = [...normalized].sort((a, b) => a - b)
  const percentile80 = sorted[Math.min(sorted.length - 1, Math.floor((sorted.length - 1) * 0.8))] || 0
  const targetPercentile80 = 0.74

  let gamma = 1
  if (percentile80 > 0 && percentile80 < 1) {
    gamma = Math.log(targetPercentile80) / Math.log(percentile80)
  }
  gamma = clamp(gamma, 0.75, 1.35)

  return normalized.map(value => clamp(Math.pow(value, gamma)))
}

function updateVisualizerWidth() {
  if (!visualizerContainer.value) {
    return
  }

  visualizerWidth.value = visualizerContainer.value.clientWidth
}

const progress = computed(() => {
  const duration = Number(currentDurationRef?.value || currentTrack?.value?.duration || 0)
  const currentTime = Number(currentTimeRef?.value || 0)
  if (!duration || duration <= 0) {
    return 0
  }
  return Math.min(1, Math.max(0, currentTime / duration))
})

function formatTime(seconds) {
  const value = Number(seconds || 0)
  const safe = Number.isFinite(value) ? value : 0
  const minutes = Math.floor(safe / 60)
  const remainingSeconds = Math.floor(safe % 60)
  return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`
}

function handleVisualizerClick(event) {
  const canvas = visualizerCanvas.value
  if (!canvas || typeof seekTo !== 'function') {
    return
  }

  const rect = canvas.getBoundingClientRect()
  const clickX = event.clientX - rect.left
  const ratio = clamp(clickX / Math.max(1, rect.width))
  const duration = Number(currentDurationRef?.value || currentTrack?.value?.duration || 0)

  if (!duration || duration <= 0) {
    return
  }

  seekTo(ratio * duration)
}

const currentTimeText = computed(() => formatTime(currentTimeRef?.value || 0))
const durationText = computed(() => formatTime(currentDurationRef?.value || currentTrack?.value?.duration || 0))
const visualizerCardStyle = computed(() => ({
  background: visualizerBackgroundStyle.value || 'linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.03))',
}))

function drawVisualizer() {
  const canvas = visualizerCanvas.value
  if (!canvas) {
    return
  }

  const context = canvas.getContext('2d')
  if (!context) {
    return
  }

  const width = visualizerContainer.value?.clientWidth || canvas.clientWidth || 0
  const height = visualizerContainer.value?.clientHeight || canvas.clientHeight || 88
  const dpr = window.devicePixelRatio || 1

  canvas.width = Math.max(1, Math.round(width * dpr))
  canvas.height = Math.max(1, Math.round(height * dpr))
  context.setTransform(dpr, 0, 0, dpr, 0, 0)
  context.clearRect(0, 0, width, height)

  const bars = visualizerBars.value
  if (!bars.length) {
    return
  }

  const gap = 0.8
  const totalGap = gap * Math.max(0, bars.length - 1)
  const barWidth = Math.max(0.5, (width - totalGap) / bars.length)
  const maxHeight = height - 8
  const listenRatio = progress.value

  const unplayedColor = 'rgb(255, 255, 255)'
  const playedColorStart = 'rgb(228, 228, 232)'
  const playedColorEnd = 'var(--violet-primary)'

  const duration = Number(currentDurationRef?.value || currentTrack?.value?.duration || 0)
  const currentTime = Number(currentTimeRef?.value || 0)

  bars.forEach((bar, index) => {
    const normalized = clamp(Number(bar) || 0)
    const barHeight = Math.max(2, normalized * maxHeight)
    const x = index * (barWidth + gap)
    const y = height - barHeight

    let playedFraction = 0
    if (duration > 0) {
      const barDuration = duration / Math.max(1, bars.length)
      const barStart = index * barDuration
      playedFraction = clamp((currentTime - barStart) / barDuration)
    } else {
      const startRatio = index / Math.max(1, bars.length)
      const endRatio = (index + 1) / Math.max(1, bars.length)
      playedFraction = clamp((listenRatio - startRatio) / Math.max(1e-6, endRatio - startRatio))
    }

    const t = clamp(playedFraction)
    const rootStyle = getComputedStyle(document.documentElement)
    const playedColor = rootStyle.getPropertyValue('--violet-primary').trim() || '#8a2be2'
    const [startR, startG, startB] = [228, 228, 232]
    const [endR, endG, endB] = playedColor
      .replace('#', '')
      .match(/.{1,2}/g)
      ?.map(value => parseInt(value, 16)) || [138, 43, 226]

    const r = Math.round(startR + (endR - startR) * t)
    const g = Math.round(startG + (endG - startG) * t)
    const b = Math.round(startB + (endB - startB) * t)
    const fillColor = `rgb(${r}, ${g}, ${b})`

    context.fillStyle = fillColor
    context.fillRect(x, y, barWidth, barHeight)
  })
}

const activeVisualizerSong = computed(() => {
  if (currentTrack?.value && Array.isArray(currentTrack.value?.visualizer_data?.bars) && currentTrack.value.visualizer_data.bars.length) {
    return currentTrack.value
  }

  return null
})

watch(currentTrack, (song) => {
  refreshVisualizerBackground(song)
}, { immediate: true })

const visualizerBars = computed(() => {
  const chosenSong = activeVisualizerSong.value
  const sourceBars = chosenSong?.visualizer_data?.bars?.length
    ? chosenSong.visualizer_data.bars
    : fallbackBars

  const interpolatedBars = interpolateBars(sourceBars.map(value => clamp(Number(value) || 0)), getTargetBarCount())
  return normalizeBarsToPeak(interpolatedBars)
})

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

watch([visualizerBars, visualizerWidth, currentTimeRef, currentDurationRef], () => {
  requestAnimationFrame(drawVisualizer)
}, { flush: 'post' })

onMounted(() => {
  loadSongs()
  updateVisualizerWidth()
  requestAnimationFrame(drawVisualizer)

  if (typeof ResizeObserver !== 'undefined' && visualizerContainer.value) {
    resizeObserver = new ResizeObserver(() => {
      updateVisualizerWidth()
      requestAnimationFrame(drawVisualizer)
    })
    resizeObserver.observe(visualizerContainer.value)
  }
})

onUnmounted(() => {
  if (resizeObserver) {
    resizeObserver.disconnect()
  }
})
</script>

<style scoped>
.songs-view-header {
  border-radius: 0.75rem;
  position: sticky;
  top: 0;
  z-index: 10;
  background-color: var(--primary-bg);
}

.visualizer-card {
  display: flex;
  z-index: 20;
  border: 1px solid rgba(255, 255, 255, 0.12);
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.03));
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.08);
}

.visualizer-left {
  padding: 1.2rem 1.3rem;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 1rem;
  /* background: rgba(255, 255, 255, 0.1); */
}

.visualizer-thumbnail {
  width: 300px;
  height: 300px;
  border-radius: 0.5rem;
  overflow: hidden;
  flex-shrink: 0;
  position: relative;
}
  .visualizer-thumbnail img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

.visualizer-right {
  padding: 1.2rem 1.3rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 0.5rem;
  flex: 1;
}

.visualizer-header {
  display: flex;
  gap: 1.7rem;
}

.visualizer-actions {
  position: relative;
  display: flex;
  align-items: flex-start;
  gap: 0.05rem;
  font-size: 1.25rem;
  color: var(--secondary-text);
}

.visualizer-actions-button {
  position: relative;
  padding: 0.2rem 0.4rem;
  background: none;
  border: none;
  cursor: pointer;
  color: inherit;
  transition: all 0.2s ease;
}
.visualizer-actions-button:hover {
  color: var(--primary-text);
  background: none;
}

.visualizer-tooltip {
  --tooltip-x: -50%;
  position: absolute;
  top: calc(100% + 1rem);
  left: 50%;
  transform: translateX(var(--tooltip-x)) translateY(-0.2rem);
  opacity: 0;
  pointer-events: none;
  z-index: 6;
  padding: 0.25rem 0.45rem;
  border-radius: 0.4rem;
  background: rgba(120, 120, 120, 0.95);
  color: #fff;
  font-size: 0.72rem;
  line-height: 1;
  white-space: nowrap;
  max-width: min(12rem, calc(100vw - 2rem));
  overflow: hidden;
  text-overflow: ellipsis;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.22);
  transition: opacity 0.15s ease, transform 0.15s ease;
}

.visualizer-actions-button:first-child .visualizer-tooltip {
  --tooltip-x: 0%;
  left: 0;
}

.visualizer-actions-button:last-child .visualizer-tooltip {
  --tooltip-x: 0%;
  left: auto;
  right: 0;
}

.visualizer-actions-button:hover .visualizer-tooltip,
.visualizer-actions-button:focus-visible .visualizer-tooltip {
  opacity: 1;
  transform: translateX(var(--tooltip-x)) translateY(0);
}

.visualizer-label {
  flex: 1;
  display: flex;
  flex-direction: column;
  color: var(--primary-text);
}

.visualizer-song {
  text-align: justify;
  width: fit-content;
  padding: 0.2rem 0.5rem;
  background-color: #000;
  color: var(--primary-text);
  font-size: 1.75rem;
  font-weight: 600;
}

.visualizer-artist {
  width: fit-content;
  padding: 0.2rem 0.5rem;
  background-color: #000;
  color: var(--secondary-text);
  font-size: 1.25rem;
  font-weight: 500;
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
}

.visualizer-shell {
  position: relative;
  width: 100%;
  height: 88px;
  overflow: hidden;
  padding-bottom: 0.2rem;
  background: transparent;
}
  .visualizer-shell canvas {
    opacity: 0.9;
  }
  .visualizer-shell:hover canvas {
    opacity: 1;
  }

.visualizer-bars {
  display: block;
  width: 100%;
  height: 100%;
  background: transparent;
  cursor: pointer;
}

.visualizer-timer {
  position: absolute;
  bottom: 0.15rem;
  font-size: 0.72rem;
  font-weight: 600;
  padding: 0.1rem 0.35rem;
  border-radius: 0.25rem;
  background: #000;
  line-height: 1;
  pointer-events: none;
  z-index: 2;
}

.visualizer-timer-left {
  left: 0.25rem;
  color: var(--violet-secondary);
}

.visualizer-timer-right {
  right: 0.25rem;
  color: var(--secondary-text);
}

.song-list-header {
  display: flex;
  align-items: center;
  gap: 5px;
  width: 100%;
  padding: 5px;

  background-color: var(--primary-bg);
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