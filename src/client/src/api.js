const API_BASE_URL = ''

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
    },
    ...options,
  })

  if (!response.ok) {
    const text = await response.text()
    throw new Error(`API error ${response.status}: ${text}`)
  }

  return response.json()
}

export async function fetchSongs() {
  return request('/songs')
}

export async function fetchPlaylists() {
  return request('/playlists')
}

export async function fetchPlaylistSongs(playlistId) {
  return request(`/playlists/${playlistId}/songs`)
}
