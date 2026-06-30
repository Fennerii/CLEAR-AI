<script setup>
defineProps({
  imageUrl: String,
  detections: Array,
  instructions: String
})

const emit = defineEmits(['uploadAnother'])

const colors = ["#1b75bc", "#39b54a", "#fbb03b", "#ff1d25", "#4d4d4d", "#754c24", "#ffffff"];
const dots = Array.from({ length: 60 }, () => ({
  top: Math.random() * 100,
  left: Math.random() * 100,
  size: 10 + Math.random() * 6,
  color: colors[Math.floor(Math.random() * colors.length)],
  duration: 8 + Math.random() * 12,
  delay: Math.random() * -20
}))
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
            <div class="glass-card chat-box">

              <div class="top-bar">
                <span class="chat-title">Talking with CLEAR-AI</span>
                <button class="upload-btn" @click="emit('uploadAnother')">
                  <span style="color: black;">Upload Another</span>
                  <i class="fa-solid fa-upload is-size-4"></i>
                </button>
              </div>

              <div class="chat-body">

                <img v-if="imageUrl" :src="imageUrl" class="uploaded-photo" />

                <div v-if="detections && detections.length" class="detected-list">
                  <h3 class="section-heading">Detected Items</h3>
                  <div v-for="(item, i) in detections" :key="i" class="detected-item">
                    <span>{{ item.label }}</span>
                    <span class="confidence">{{ Math.round(item.confidence * 100) }}%</span>
                  </div>
                </div>

                <div v-if="instructions" class="instructions-text">
                  <h3 class="section-heading">Disposal Instructions</h3>
                  <p>{{ instructions }}</p>
                </div>

              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
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

.glass-card {
  backdrop-filter: blur(20px);
  background: rgba(255, 255, 255, 0.35);
  border: 2px solid #9daecc;
  border-radius: 24px;
  box-shadow: 0 4px 12px #01050b;
}

.chat-box {
  width: 910px;
  box-sizing: border-box;
  padding: 0;
  height: 900px;
}

.top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #9daecc;
  padding: 16px 24px;
}

.chat-title {
  font-weight: 600;
  color: #1a1a1a;
}

.upload-btn {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  box-sizing: border-box;
  border-radius: 999px;
  border: 1px solid grey;
  padding: 10px 18px;
  white-space: nowrap;
  background-color: lightgray;
  cursor: pointer;
}

.chat-body {
  padding: 24px;
  min-height: 400px;
  max-height: 600px;
  overflow-y: auto;
}

.uploaded-photo {
  max-width: 250px;
  border-radius: 16px;
  margin-bottom: 16px;
  display: block;
  margin-left: auto;
  margin-right: auto;
}

.section-heading {
  font-size: 14px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 8px;
  margin-top: 16px;
}

.detected-item {
  display: flex;
  justify-content: space-between;
  padding: 6px 0;
  border-bottom: 1px solid #ddd;
  color: #333;
}

.confidence {
  color: #777;
}

.instructions-text p {
  color: #333;
  line-height: 1.6;
  white-space: pre-line;
}
</style>