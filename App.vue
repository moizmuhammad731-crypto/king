<template>
  <!-- Scroll progress indicator -->
  <div class="pw-progress" aria-hidden="true">
    <div class="pw-progress-fill h-full"></div>
  </div>

  <!-- Animated aurora backdrop -->
  <div class="pw-aurora" aria-hidden="true">
    <span class="pw-orb-a"></span>
    <span class="pw-orb-b"></span>
    <span class="pw-orb-c"></span>
    <span class="pw-orb-d"></span>
  </div>

  <div class="relative z-10 min-h-screen flex flex-col text-ink">
    <Navbar />
    <main class="flex-1">
      <router-view />
    </main>
    <footer class="mt-12 border-t border-[#EC4899]/15 bg-white/55">
      <div class="h-px w-full bg-gradient-to-r from-transparent via-[#EC4899]/40 to-transparent"></div>
      <div
        class="max-w-7xl mx-auto px-4 py-6 flex flex-col sm:flex-row items-center justify-between gap-2 text-center sm:text-left font-mono text-[11px] text-muted"
      >
        <p>
          <strong class="pw-rainbow-text font-extrabold font-sans">Pink Wheels</strong> — Safe rides. Fair prices.
          <span class="mx-1.5 text-[#EC4899]/30">•</span> University DSA Project
        </p>
        <p class="tracking-tight">
          <span class="text-[#BE185D]">Linked List</span> |
          <span class="text-[#BE185D]">Min-Heap</span> |
          <span class="text-[#9D174D]">Stack</span>
        </p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { nextTick, onMounted, onUnmounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import Navbar from './components/common/Navbar.vue'

const route = useRoute()
let observer = null
let mutations = null
let stopRouteWatch = null

function reveal(el) {
  if (el.classList.contains('is-in')) return
  if (el.matches('.pw-reveal, .pw-reveal-fade')) observer.observe(el)
  el.querySelectorAll?.('.pw-reveal, .pw-reveal-fade').forEach((child) => observer.observe(child))
}

onMounted(() => {
  if (!('IntersectionObserver' in window)) {
    document.querySelectorAll('.pw-reveal, .pw-reveal-fade').forEach((el) => el.classList.add('is-in'))
    return
  }

  observer = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue
        entry.target.classList.add('is-in')
        observer.unobserve(entry.target)
      }
    },
    { rootMargin: '0px 0px -4% 0px', threshold: 0.01 }
  )

  document.querySelectorAll('.pw-reveal, .pw-reveal-fade').forEach((el) => observer.observe(el))

  mutations = new MutationObserver((records) => {
    for (const record of records) {
      record.addedNodes.forEach((node) => {
        if (node.nodeType === 1) reveal(node)
      })
    }
  })
  mutations.observe(document.querySelector('main') || document.body, { childList: true, subtree: true })

  stopRouteWatch = watch(
    () => route.fullPath,
    async () => {
      await nextTick()
      document
        .querySelectorAll('.pw-reveal:not(.is-in), .pw-reveal-fade:not(.is-in)')
        .forEach((el) => observer.observe(el))
      window.scrollTo(0, 0)
    },
    { flush: 'post' }
  )
})

onUnmounted(() => {
  observer?.disconnect()
  mutations?.disconnect()
  stopRouteWatch?.()
})
</script>
