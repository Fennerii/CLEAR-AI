<script setup>
import { ref } from 'vue'
import Disposal from './components/Disposal.vue'

const colors = ["#1b75bc", "#39b54a", "#fbb03b", "#ff1d25", "#4d4d4d", "#754c24", "#ffffff"]

const dots = Array.from({ length: 60 }, () => ({
  top: Math.random() * 100,
  left: Math.random() * 100,
  size: 10 + Math.random() * 6,
  color: colors[Math.floor(Math.random() * colors.length)],
  duration: 8 + Math.random() * 12,
  delay: Math.random() * -20
}))

const fileInput = ref(null)
const cameraInput = ref(null)
const hasUploaded = ref(false)
const uploadedImage = ref(null)
const detections = ref([])
const instructions = ref('')
const isLoading = ref(false)

async function handleFileChange(event) {
  const file = event.target.files[0]
  if (!file) return

  uploadedImage.value = URL.createObjectURL(file)
  isLoading.value = true
  hasUploaded.value = false

  const formData = new FormData()
  formData.append('file', file)

  try {
    const response = await fetch('http://localhost:8000/detect', {
      method: 'POST',
      body: formData
    })
    const data = await response.json()
    detections.value = data.detections
    instructions.value = data.instructions
    hasUploaded.value = true
  } catch (error) {
    console.error('Upload failed:', error)
  } finally {
    isLoading.value = false
  }
}

function triggerFileInput() {
  fileInput.value.click()
}

function triggerCamera() {
  cameraInput.value.click()
}
</script>

<template>
  <section class="hero is-fullheight particle-bg">
    <div
      v-for="(dot, i) in dots"
      :key="i"
      class="dot"
      :style="{
        top: dot.top + '%',
        left: dot.left + '%',
        width: dot.size + 'px',
        height: dot.size + 'px',
        backgroundColor: dot.color,
        animationDuration: dot.duration + 's',
        animationDelay: dot.delay + 's'
      }"
    ></div>

    <div class="hero-body">
      <div class="container">
        <div class="columns is-vcentered is-centered cards-row">

          <div class="column is-narrow">
            <div class="glass-card name-card">
              <h1 class="title has-text-centered is-size-1 is-family-monospace" style="color: #1a1a1a;">CLEAR-AI</h1>
              <p class="subtitle" style="color: #444;">Making the World A Cleaner Place</p>
            </div>
          </div>

          <div class="column is-narrow">
            <div class="glass-card upload-card">

              <!-- File picker input -->
              <input
                type="file"
                ref="fileInput"
                accept="image/*"
                @change="handleFileChange"
                hidden
              />

              <!-- Camera input -->
              <input
                type="file"
                ref="cameraInput"
                accept="image/*"
                capture="environment"
                @change="handleFileChange"
                hidden
              />

              <!-- Loading state -->
              <div v-if="isLoading" class="loading-text">
                <i class="fa-solid fa-spinner fa-spin"></i>
                Analyzing...
              </div>

              <!-- Upload buttons -->
              <div v-else class="button-group">
                <button class="button is-light browse-btn" @click="triggerFileInput">
                  <i class="fa-solid fa-recycle is-size-1"></i>
                  <h1>Upload Image</h1>
                </button>

                <button class="button is-light browse-btn" @click="triggerCamera">
                  <i class="fa-solid fa-camera is-size-1"></i>
                  <h1>Take Photo</h1>
                </button>
              </div>

              <p class="upload-text">See How to Dispose of Your Trash</p>
            </div>
          </div>

        </div>
      </div>
    </div>
  </section>

  <Disposal
    v-if="hasUploaded"
    :imageUrl="uploadedImage"
    :detections="detections"
    :instructions="instructions"
    @uploadAnother="triggerFileInput"
  />
</template>

<style scoped>
.particle-bg {
  background-color: #ffffff;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.dot {
  position: absolute;
  border-radius: 50%;
  opacity: 0.7;
  pointer-events: none;
  animation-name: float;
  animation-timing-function: ease-in-out;
  animation-iteration-count: infinite;
}

@keyframes float {
  0%   { transform: translate(0, 0); }
  25%  { transform: translate(15px, -20px); }
  50%  { transform: translate(-10px, -35px); }
  75%  { transform: translate(-20px, -10px); }
  100% { transform: translate(0, 0); }
}

.cards-row {
  position: relative;
  z-index: 1;
}

.glass-card {
  backdrop-filter: blur(20px);
  background: rgba(255, 255, 255, 0.35);
  border: 2px solid #9daecc;
  border-radius: 24px;
  box-shadow: 0 4px 12px #01050b;
}

.name-card {
  width: 380px;
  height: 560px;
  padding: 40px 32px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.upload-card {
  width: 320px;
  height: 280px;
  padding: 32px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  text-align: center;
}

.button-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 100%;
  align-items: center;
}

.browse-btn {
  background-color: lightgray;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  height: auto;
  padding: 16px 32px;
  width: 100%;
}

.upload-text {
  font-size: 14px;
  color: #444;
}

.loading-text {
  font-size: 16px;
  color: #444;
  display: flex;
  align-items: center;
  gap: 8px;
}
</style>