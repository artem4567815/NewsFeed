<template>
  <header class="py-2 px-2 lg:px-7 border-b-2 bg-white border-gray-200 flex items-center justify-between gap-3 relative z-50">
    <div class="flex items-center whitespace-nowrap">
      <div @click="$router.push('/')" class="text-2xl hover:cursor-pointer font-semibold">Edu<span class="text-blue-500">Feed</span></div>

    </div>

    <div class="flex justify-center items-center">
      <blue-button v-show="!token || token === 'undefined'" @click="$router.push('/auth')" class="mr-5">Вход</blue-button>
      <blue-button v-show="$route.path !== '/profile' && token && token !== 'undefined'" @click="$router.push('/profile')" class="mr-5">Профиль</blue-button>
      <blue-button @click="$router.push('/Create')" v-show="$route.path === '/profile'" class="mr-5">Создать пост</blue-button>

      <div class="mb-0 flex items-center relative" ref="menuRef">
        <!-- Бургер кнопка -->
        <div
            v-if="$route.path == '/profile'"
         @click="toggleSidebar"
            class="hover:cursor-pointer block md:hidden bg-gray-200 ring-4 mr-5 ring-black/0 hover:bg-gray-300 hover:ring-gray-200 transition ease-in-out rounded-2xl p-3 sm:mr-5"
        >
          <AlignJustify /> <!-- НУЖНО НАСТРОИТЬ ЭМИТ -->
        </div>

        <!-- Выпадающий список -->
        <transition name="fade-slide">
          <div v-if="showDropdown"  class=" absolute top-12 right-0 w-56 bg-white border border-gray-200 rounded-xl shadow-lg z-50">
            <button class="w-full flex items-center gap-3 px-4 py-3 text-sm text-gray-800 hover:bg-gray-100 transition" @click="$router.push('/news')">
              <Newspaper class="w-5 h-5 text-gray-600" /> Новости
            </button>
            <button class="w-full flex items-center gap-3 px-4 py-3 text-sm text-gray-800 hover:bg-gray-100 transition" @click="$router.push('/wallpapers')">
              <Layout class="w-5 h-5 text-gray-600" /> Стенгазеты
            </button>
            <button class="w-full flex items-center gap-3 px-4 py-3 text-sm text-gray-800 hover:bg-gray-100 transition" @click="$router.push('/team-search')">
              <BriefcaseBusiness  class="w-5 h-5 text-gray-600" /> Поиск команды
            </button>
          </div>
        </transition>

        <!-- Вторая кнопка фильтра -->
        <div v-show="$route.path == '/'" @click="toggleFilter" class="hover:cursor-pointer block 2xl:hidden bg-gray-200 ring-4 mr-5 ring-black/0 hover:bg-gray-300 hover:ring-gray-200 transition ease-in-out rounded-2xl p-3 sm:mr-5">
          <Filter />
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { Settings, Search, Filter, AlignJustify, Newspaper, Layout, BriefcaseBusiness  } from 'lucide-vue-next';
import BlueButton from "@/components/UI/blueButton.vue";
import { ref, onMounted, onBeforeUnmount } from 'vue'
import emitter from '@/main.js'
import { useRoute } from 'vue-router'

const route = useRoute()

const toggleSidebar = () => {
  emitter.emit('toggle-sidebar')
}

const toggleFilter = () => {
  emitter.emit('toggle-filter')
}

const token = localStorage.getItem('authToken')
const showDropdown = ref(false)
const menuRef = ref(null)

function toggleDropdown() {
  showDropdown.value = !showDropdown.value
}


function handleClickOutside(event) {
  if (menuRef.value && !menuRef.value.contains(event.target)) {
    showDropdown.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})
onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})

</script>

<style scoped>
.fade-slide-enter-active, .fade-slide-leave-active {
  transition: all 0.3s ease;
}
.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}
.fade-slide-enter-to {
  opacity: 1;
  transform: translateY(0);
}
.fade-slide-leave-from {
  opacity: 1;
  transform: translateY(0);
}
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
