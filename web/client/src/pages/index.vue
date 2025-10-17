<!-- vibe coded -->
<template>
  <v-app>
    <v-app-bar elevation="1">
      <v-toolbar-title>FlySearch Analytics</v-toolbar-title>
      <div class="toolbar-center">
        <div class="d-flex align-center">
          <v-select
            v-model="selectedRun"
            :items="runs"
            label="Run"
            variant="underlined"
            class="mt-5 mr-6"
            density="compact"
            :loading="loadingRuns"
            :disabled="loadingRuns || runs.length === 0"
            @update:model-value="onRunChange"
            width="240"
          />
          <v-select
            v-model="selectedEpisode"
            :items="episodes"
            label="Episode"
            variant="underlined"
            class="mt-5"
            density="compact"
            :loading="loadingEpisodes"
            :disabled="loadingEpisodes || episodes.length === 0"
            @update:model-value="onEpisodeChange"
            width="240"
          />
        </div>
      </div>
    </v-app-bar>
    <v-main>
      <v-container>

        <v-alert
          v-if="!selectedRun || !selectedEpisode"
          type="info"
          variant="tonal"
          class="mt-4"
        >
          Please select a Run and an Episode to view details.
        </v-alert>

        <v-card v-if="scenarioParams.length > 0" variant="outlined" class="mt-4">
          <v-card-title>Scenario params</v-card-title>
          <v-card-text>
            <div v-if="scenarioParams.length === 0" class="text-medium-emphasis">No parameters to display.</div>
            <div v-else>
              <div>
                <span class="text-medium-emphasis">Object name:</span>
                <span class="ml-2">{{ passedObjectName }}</span>
              </div>
              <v-expansion-panels class="mt-3" density="compact">
                <v-expansion-panel class="more-params" density="compact">
                  <template #title>
                    <span class="text-caption text-medium-emphasis">More parameters</span>
                  </template>
                  <v-expansion-panel-text>
                    <v-table density="compact">
                      <thead>
                        <tr>
                          <th class="text-left">Key</th>
                          <th class="text-left">Value</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="([k, v], idx) in otherScenarioParams" :key="k + '_' + idx">
                          <td>{{ k }}</td>
                          <td>{{ v }}</td>
                        </tr>
                      </tbody>
                    </v-table>
                    <div v-if="otherScenarioParams.length === 0" class="text-medium-emphasis mt-2">No additional parameters.</div>
                  </v-expansion-panel-text>
                </v-expansion-panel>
              </v-expansion-panels>
            </div>
          </v-card-text>
        </v-card>

        <v-card v-if="conversation.length > 0" variant="outlined" class="mt-4">
          <v-card-title>Conversation</v-card-title>
          <v-card-text>
            <div
              v-for="(msg, i) in conversation"
              :key="i"
              class="d-flex mb-3 align-center"
              :class="msg.role === 'assistant' ? 'justify-start' : 'justify-end'"
            >
              <div v-if="msg.role === 'assistant'" class="d-flex flex-column align-center mr-3">
                <v-avatar size="48">
                  <v-icon icon="mdi-robot" size="32" />
                </v-avatar>
                <div class="text-caption mt-n1">Agent</div>
              </div>
              <div v-if="!msg.isImage" class="bubble" :class="msg.role">
                <div v-if="msg.isLong && !msg.expanded">
                  {{ msg.preview }}
                  <v-btn
                    variant="text"
                    size="x-small"
                    class="ml-2"
                    @click="msg.expanded = true"
                  >Show more</v-btn>
                </div>
                <div v-else>
                  {{ msg.text }}
                  <v-btn
                    v-if="msg.isLong"
                    variant="text"
                    size="x-small"
                    class="ml-2"
                    @click="msg.expanded = false"
                  >Show less</v-btn>
                </div>
              </div>
              <div v-else>
                <v-img
                  :src="imageUrl(selectedRun, selectedEpisode, msg.imageIndex)"
                  width="500"
                  height="500"
                  class="rounded"
                  cover
                >
                  <template #placeholder>
                    <div class="d-flex align-center justify-center fill-height">
                      <v-progress-circular color="grey" indeterminate />
                    </div>
                  </template>
                </v-img>
              </div>
              <div v-if="msg.role === 'user'" class="d-flex flex-column align-center ml-3">
                <v-avatar size="48">
                  <v-icon icon="mdi-quadcopter" size="32" />
                </v-avatar>
                <div class="text-caption mt-n1">Benchmark</div>
              </div>
            </div>
            <div v-if="conversation.length === 0" class="text-medium-emphasis mt-2">No conversation to display.</div>
          </v-card-text>
        </v-card>

        <v-card v-if="successState !== null" variant="outlined" class="mt-4">
          <v-card-title>Result</v-card-title>
          <v-card-text>
            <v-alert
              :type="successState ? 'success' : 'error'"
              variant="tonal"
            >
              {{ successState ? 'Target located' : 'Mission failed' }}
            </v-alert>
          </v-card-text>
        </v-card>

        <v-card v-if="selectedRun && selectedEpisode" variant="outlined" class="mt-4">
          <v-card-title>Trajectory preview</v-card-title>
          <v-card-text>
            <v-img
              :src="previewUrl(selectedRun, selectedEpisode)"
              max-width="1000"
              max-height="700"
              class="rounded preview-img"
              contain
            >
              <template #placeholder>
                <div class="d-flex align-center justify-center fill-height">
                  <v-progress-circular color="grey" indeterminate />
                </div>
              </template>
            </v-img>
          </v-card-text>
        </v-card>
      </v-container>
    </v-main>
    <v-footer app elevation="1" class="justify-center">
      <div class="text-caption">© {{ currentYear }} — FlySearch authors</div>
    </v-footer>
  </v-app>
</template>

<script setup>
import {inject, onMounted, ref, watch, computed} from 'vue'

const axios = inject('axios')

// const isStatic = import.meta.env.VITE_STATIC_MODE === 'true'
const isStatic = true
const base = isStatic ? 'https://io.pardyl.com/flysearchlogs' : '/api'

const runs = ref([])
const episodes = ref([])
const selectedRun = ref('')
const selectedEpisode = ref('')
const loadingRuns = ref(false)
const loadingEpisodes = ref(false)
const scenarioParams = ref([])
const conversation = ref([])
const successState = ref(null)

const currentYear = new Date().getFullYear()

const passedObjectName = computed(() => {
  const found = scenarioParams.value.find(([k]) => k === 'passed_object_name')
  return found ? found[1] : '—'
})

const otherScenarioParams = computed(() => {
  return scenarioParams.value.filter(([k]) => k !== 'passed_object_name')
})

function fetchRuns() {
  loadingRuns.value = true
  if (isStatic) {
    fetch(base + '/index.json')
      .then(r => r.json())
      .then((idx) => {
        runs.value = (idx.runs || []).map(r => r.name)
      })
      .catch(console.error)
      .finally(() => loadingRuns.value = false)
    return
  }
  axios.get(base + '/runs')
    .then((res) => {
      runs.value = res.data || []
    })
    .catch((err) => {
      console.error(err)
    })
    .finally(() => {
      loadingRuns.value = false
    })
}

function fetchEpisodes(run) {
  if (!run) {
    episodes.value = []
    selectedEpisode.value = ''
    return
  }
  loadingEpisodes.value = true
  if (isStatic) {
    fetch(base + '/index.json')
      .then(r => r.json())
      .then((idx) => {
        const r = (idx.runs || []).find(x => x.name === run)
        episodes.value = r ? r.episodes : []
        if (selectedEpisode.value) {
          fetchScenarioParams(run, selectedEpisode.value)
          fetchConversation(run, selectedEpisode.value)
          fetchSuccess(run, selectedEpisode.value)
        }
      })
      .catch(console.error)
      .finally(() => loadingEpisodes.value = false)
    return
  }
  axios.get(base + `/runs/${encodeURIComponent(run)}/episodes`)
    .then((res) => {
      episodes.value = res.data || []
      if (selectedEpisode.value) {
        fetchScenarioParams(run, selectedEpisode.value)
        fetchConversation(run, selectedEpisode.value)
        fetchSuccess(run, selectedEpisode.value)
      }
    })
    .catch((err) => {
      console.error(err)
    })
    .finally(() => {
      loadingEpisodes.value = false
    })
}

function fetchScenarioParams(run, episode) {
  scenarioParams.value = []
  if (!run || !episode) {
    return
  }
  const url = isStatic
    ? base + `/${encodeURIComponent(run)}/${encodeURIComponent(episode)}/scenario_params.json`
    : base + `/runs/${encodeURIComponent(run)}/file/${encodeURIComponent(episode)}/scenario_params.json`
  fetch(url)
    .then(r => r.json())
    .then((data) => {
      const entries = Object.entries(data || {})
      entries.sort((a, b) => a[0].localeCompare(b[0]))
      scenarioParams.value = entries
    })
    .catch((err) => {
      console.error(err)
      scenarioParams.value = []
    })
}

function normalizeRole(role) {
  if (!role) return 'user'
  if (typeof role !== 'string') return 'user'
  const r = role.toLowerCase()
  if (r.includes('assistant')) return 'assistant'
  return 'user'
}

function fetchConversation(run, episode) {
  conversation.value = []
  if (!run || !episode) return
  const url = isStatic
    ? base + `/${encodeURIComponent(run)}/${encodeURIComponent(episode)}/conversation.json`
    : base + `/runs/${encodeURIComponent(run)}/file/${encodeURIComponent(episode)}/conversation.json`
  fetch(url)
    .then(r => r.json())
    .then((data) => {
      const msgs = Array.isArray(data) ? data : []
      let imageCounter = 0
      conversation.value = msgs.reduce((acc, m) => {
        const role = normalizeRole(m[0])
        const text = m[1]
        if (text === 'image') {
          const idx = imageCounter
          imageCounter += 1
          acc.push({ role, text, isImage: true, imageIndex: idx })
          return acc
        }
        const cleaned = typeof text === 'string' ? text.replace(/^[\r\n]+|[\r\n]+$/g, '') : String(text)
        // Hide lines like "Image 12:" from conversation view
        if (/^\s*Image\s+\d+:\s*$/.test(cleaned)) {
          return acc
        }
        const isLong = cleaned.length > 500
        const preview = isLong ? cleaned.slice(0, 500) + '…' : cleaned
        acc.push({ role, text: cleaned, isImage: false, isLong, expanded: false, preview })
        return acc
      }, [])
    })
    .catch((err) => {
      console.error(err)
      conversation.value = []
    })
}

function fetchSuccess(run, episode) {
  successState.value = null
  if (!run || !episode) return
  if (isStatic) {
    // In static mode, read exported success.json (boolean). If missing, leave as null.
    const urlJson = base + `/${encodeURIComponent(run)}/${encodeURIComponent(episode)}/success.json`
    fetch(urlJson)
      .then((res) => {
        if (!res.ok) throw new Error('missing success.json')
        return res.json()
      })
      .then((data) => { successState.value = !!data })
      .catch(() => { successState.value = null })
    return
  }
  const url = base + `/runs/${encodeURIComponent(run)}/episodes/${encodeURIComponent(episode)}/success`
  fetch(url)
    .then(r => r.json())
    .then((data) => { successState.value = !!data })
    .catch((err) => {
      console.error(err)
      successState.value = null
    })
}

function previewUrl(run, episode) {
  return isStatic
    ? base + `/${encodeURIComponent(run)}/${encodeURIComponent(episode)}/preview.jpg`
    : base + `/runs/${encodeURIComponent(run)}/episodes/${encodeURIComponent(episode)}/preview.png`
}

function imageUrl(run, episode, idx) {
  if (!run || !episode) return ''
  return isStatic
    ? base + `/${encodeURIComponent(run)}/${encodeURIComponent(episode)}/${idx}.jpg`
    : base + `/runs/${encodeURIComponent(run)}/file/${encodeURIComponent(episode)}/${idx}.png`
}

function onRunChange() {
  selectedEpisode.value = ''
  scenarioParams.value = []
  conversation.value = []
  successState.value = null
  fetchEpisodes(selectedRun.value)
}

function onEpisodeChange() {
  fetchScenarioParams(selectedRun.value, selectedEpisode.value)
  fetchConversation(selectedRun.value, selectedEpisode.value)
  fetchSuccess(selectedRun.value, selectedEpisode.value)
}

onMounted(() => {
  fetchRuns()
})

watch(selectedRun, (val, old) => {
  if (val !== old) {
    onRunChange()
  }
})

watch(selectedEpisode, (val, old) => {
  if (val !== old) {
    onEpisodeChange()
  }
})
</script>

<style scoped>
.v-container {
  max-width: 1000px;
  margin-top: 1rem
}
.toolbar-center {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
}
/* Smaller expansion header */
.more-params :deep(.v-expansion-panel-title) {
  min-height: 28px;
  padding-top: 2px;
  padding-bottom: 2px;
}
.bubble {
  max-width: 65%;
  padding: 10px 12px;
  border-radius: 12px;
  white-space: pre-wrap;
  word-break: break-word;
  background-color: transparent;
}
.bubble.assistant {
  border: 1px solid rgba(var(--v-theme-on-surface), 0.38);
  color: rgb(var(--v-theme-on-surface));
}
.bubble.user {
  border: 1px solid rgb(var(--v-theme-primary));
  color: rgb(var(--v-theme-primary));
}
.preview-img :deep(img) {
  object-fit: contain !important;
}
</style>
