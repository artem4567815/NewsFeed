<template>
  <div class="flex max-w-[2000px] h-screen bg-gray-50 transition-all ml-auto mr-auto duration-300 ease-in-out flex-col md:flex-row">
    <!-- Sidebar -->
    <aside :class="['md:w-64 w-full md:block', sidebarOpen ? 'block' : 'hidden', 'bg-white border-r p-4 shadow-md fixed md:relative z-10 h-full md:h-auto']">
      <nav class="space-y-4">
        <SidebarItem icon="Newspaper" text="Твои новости" :active="currentPage === 'news'" @click="setPage('news')" />
        <SidebarItem icon="FileEdit" text="Черновики" :active="currentPage === 'drafts'" @click="setPage('drafts')" />
        <SidebarItem icon="ShieldCheck" text="Модерация" v-if="isAdmin" :active="currentPage === 'moderation'" @click="setPage('moderation')" />
        <SidebarItem icon="ScrollText" text="Все новости" v-if="isAdmin" :active="currentPage === 'moderation_list'" @click="setPage('moderation_list')" />
        <SidebarItem icon="User" text="Профиль" :active="currentPage === 'profile'" @click="setPage('profile')" />
      </nav>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 p-4 md:p-6 overflow-auto">
      <div class="tab-container">
        <transition name="fade-in" mode="out-in">
          <component 
            :is="currentComponent" 
            v-if="currentComponent"
            ref="currentTabRef"
          />
        </transition>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import * as icons from 'lucide-vue-next'
import SidebarItem from "@/components/SidebarItem.vue"
import ProfileTab from "@/components/profile/ProfileTab.vue"
import DraftsTab from "@/components/profile/DraftsTab.vue"
import NewsTab from "@/components/profile/NewsTab.vue"
import ModerationTab from "@/components/profile/ModerationTab.vue"
import ModerationListTab from "@/components/profile/ModerationListTab.vue"
import emitter from '@/main.js'
import { jwtDecode } from "jwt-decode"
import router from "@/router/router.js"

const { Menu } = icons

const currentPage = ref('news')
const sidebarOpen = ref(false)
const isAdmin = ref(false)
const currentTabRef = ref(null)

// Вычисляемое свойство для определения текущего компонента
const currentComponent = computed(() => {
  switch (currentPage.value) {
    case 'profile':
      return ProfileTab
    case 'drafts':
      return DraftsTab
    case 'news':
      return NewsTab
    case 'moderation':
      return ModerationTab
    case 'moderation_list':
      return ModerationListTab
    default:
      return null
  }
})

emitter.on('toggle-sidebar', () => {
  sidebarOpen.value = !sidebarOpen.value
})

const setPage = (page) => {
  currentPage.value = page
  sidebarOpen.value = false
}

// Проверка прав администратора при монтировании
onMounted(() => {
  const token = localStorage.getItem('authToken')
  if (!token) {
    router.push('/auth')
    return
  }
  try {
    const decoded = jwtDecode(token)
    if (decoded['is_admin']) {
      isAdmin.value = true
    }
  } catch (e) {
    console.error("Token decoding failed", e)
    router.push('/auth')
  }
})

// Следим за изменением текущей страницы и загружаем соответствующие данные

</script>

<style>
html {
  scroll-behavior: smooth;
}
.tab-container {
  position: relative;
  overflow: hidden;
  min-height: 100%;
}

.fade-in-enter-active, .fade-in-leave-active {
  transition: all 0.35s ease;
  position: absolute;
  width: 100%;
}

.fade-in-enter-from, .fade-in-leave-to {
  opacity: 0;
  transform: translateY(15px);
}

.fade-in-enter-to, .fade-in-leave-from {
  opacity: 1;
  transform: translateY(0);
}
</style>