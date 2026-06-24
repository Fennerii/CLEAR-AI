<script setup>
import Disposal from './components/Disposal.vue'

const colors = ["#1b75bc", "#39b54a", "#fbb03b", "#ff1d25", "#4d4d4d", "#754c24", "#ffffff"];

const dots = Array.from({ length: 60 }, () => ({
  top: Math.random() * 100,
  left: Math.random() * 100,
  size: 10 + Math.random() * 6,
  color: colors[Math.floor(Math.random() * colors.length)],
  duration: 8 + Math.random() * 12,
  delay: Math.random() * -20
}))

import {ref} from 'vue'
// Imports Vue ref function, Ref watches for refreshes and re-renders
// Docs: https://vuejs.org/api/reactivity-core.html#ref

const fileInput = ref(null)
//Creates a const variable that is set to null, it holds a reference to input file

const hasUploaded = ref(false)
// Conontrols when Disposal.vue shows up in the template. Boolean

const uploadedImage = ref(null)
//Holds the img until we can display it with the <img> tag

const detections = ref([])
// Holds Data from Detections in the back end

const instructions = ref('')
//empty string to be filled in with ollama

const isLoading = ref(false)
//Boolean to track whether a request is loading ^add a spinny wheel or smth^

function triggerFileInput(){
    fileInput.value.click()
}
// file picker function

async function handleFileChange(event) {
  console.log("error", event.target.files[0])
  const file = event.target.files[0]
  if (!file) return

  uploadedImage.value = URL.createObjectURL(file)
  isLoading.value = true

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

              <!-- hidden file input, triggered by the visible button below -->
              <input
                type="file"
                ref="fileInput"
                accept="image/*"
                @change="handleFileChange"
                hidden
              />

              <!-- visible custom button, clicking it opens the hidden file picker -->
              <button class="button is-light browse-btn" @click="triggerFileInput">
                <i class="fa-solid fa-recycle is-size-1"></i>
                <h1>Upload Your Image</h1>
              </button>

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
  border: 2px solid  	#9daecc;
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
  height: 220px;
  padding: 32px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  text-align: center;
}

.upload-icon {
  font-size: 36px;
  color: #444;
}

.browse-btn {
  margin-top: 8px;
  background-color: lightgray;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  height: auto;
  padding: 24px 32px;
}
.upload-text {
  font-size: 14px;
  color: #444;
}


</style>