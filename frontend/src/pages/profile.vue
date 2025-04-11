<template>
  <div class="flex max-w-[2000px] h-screen bg-gray-50 transition-all ml-auto mr-auto duration-300 ease-in-out flex-col md:flex-row">
    <!-- Sidebar -->
    <aside :class="['md:w-64 w-full md:block', sidebarOpen ? 'block' : 'hidden', 'bg-white border-r p-4 shadow-md fixed md:relative z-10 h-full md:h-auto']">
      <nav class="space-y-4">
        <SidebarItem icon="Newspaper" text="Твои новости" :active="currentPage === 'news'" @click="setPage('news')" />
        <SidebarItem icon="FileEdit" text="Черновики" :active="currentPage === 'drafts'" @click="setPage('drafts')" />
        <SidebarItem icon="ShieldCheck" text="Модерация" :active="currentPage === 'moderation'" @click="setPage('moderation')" /> <!-- ТУТ НАДО ПРОВЕРЯТЬ БУДЕТ ТОКЕН -->
        <SidebarItem icon="User" text="Профиль" :active="currentPage === 'profile'" @click="setPage('profile')" />
      </nav>
    </aside>

    <!-- Mobile Header -->


    <!-- Main Content -->
    <main class="flex-1 p-4 md:p-6 overflow-auto mt-16 md:mt-0">
      <div class="tab-container">
        <transition name="fade-in" mode="out-in">

            <!-- PROFILE -->
            <div v-if="currentPage === 'profile'">
              <h1 class="text-2xl font-bold mb-6">Профиль</h1>
              <div class="flex flex-col lg:flex-row gap-6">
                <div class="bg-white p-6 rounded-lg shadow w-full lg:w-1/3 text-center">
                  <img src="https://i.pravatar.cc/100" alt="avatar" class="rounded-full w-24 h-24 mx-auto mb-4" />
                  <h2 class="text-xl font-semibold">Иван Петров</h2>
                  <p class="text-gray-500">ivan@example.com</p>
                  <button class="mt-4 px-4 py-2 bg-blue-600 hover:bg-blue-700 transition text-white rounded">Изменить аватар</button>
                </div>
                <div class="bg-white p-6 rounded-lg shadow w-full lg:w-2/3">
                  <div class="border-b mb-4 pb-2 flex gap-4 overflow-auto">
                    <button @click="profileTab = 'personal'" :class="['pb-1 whitespace-nowrap', profileTab === 'personal' ? 'text-blue-600 font-medium border-b-2 border-blue-600' : 'text-gray-500 hover:text-blue-600']">Личные данные</button>
                    <button @click="profileTab = 'security'" :class="['pb-1 whitespace-nowrap', profileTab === 'security' ? 'text-blue-600 font-medium border-b-2 border-blue-600' : 'text-gray-500 hover:text-blue-600']">Безопасность</button>
                    <button @click="profileTab = 'notifications'" :class="['pb-1 whitespace-nowrap', profileTab === 'notifications' ? 'text-blue-600 font-medium border-b-2 border-blue-600' : 'text-gray-500 hover:text-blue-600']">Уведомления</button>
                  </div>
                    <div :key="profileTab">
                      <div v-if="profileTab === 'personal'" class="space-y-4">
                        <div class="flex flex-col sm:flex-row gap-4">
                          <input class="w-full sm:w-1/2 border p-2 rounded focus:outline-none focus:ring focus:ring-blue-200" placeholder="Имя" value="Иван" />
                          <input class="w-full sm:w-1/2 border p-2 rounded focus:outline-none focus:ring focus:ring-blue-200" placeholder="Фамилия" value="Петров" />
                        </div>
                        <input class="w-full border p-2 rounded focus:outline-none focus:ring focus:ring-blue-200" placeholder="Email" value="ivan@example.com" />
                        <textarea class="w-full border p-2 rounded focus:outline-none focus:ring focus:ring-blue-200" placeholder="О себе"></textarea>
                        <button class="px-4 py-2 bg-blue-600 hover:bg-blue-700 transition text-white rounded">Сохранить изменения</button>
                      </div>
                      <div v-else-if="profileTab === 'security'" class="space-y-4">
                        <label class="block text-sm font-medium text-gray-700">Текущий пароль</label>
                        <input type="password" class="w-full border p-2 rounded focus:outline-none focus:ring focus:ring-blue-200" placeholder="Введите текущий пароль" />
                        <label class="block text-sm font-medium text-gray-700">Новый пароль</label>
                        <input type="password" class="w-full border p-2 rounded focus:outline-none focus:ring focus:ring-blue-200" placeholder="Введите новый пароль" />
                        <button class="mt-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 transition text-white rounded">Обновить пароль</button>
                      </div>
                      <div v-else class="space-y-4">
                        <label class="flex items-center space-x-2">
                          <input type="checkbox" checked class="accent-blue-600" />
                          <span>Получать email-уведомления</span>
                        </label>
                        <label class="flex items-center space-x-2">
                          <input type="checkbox" class="accent-blue-600" />
                          <span>Push-уведомления в браузере</span>
                        </label>
                      </div>
                    </div>
                </div>
              </div>
            </div>

            <!-- DRAFTS -->
            <div v-else-if="currentPage === 'drafts'" class="text-center mt-20">
              <h1 class="text-2xl font-bold mb-2">У вас пока нет черновиков</h1>
              <p class="text-gray-500 mb-6">Здесь будут отображаться ваши сохраненные черновики.</p>
              <button class="px-4 py-2 bg-blue-600 hover:bg-blue-700 transition text-white rounded">Создать черновик</button>
            </div>

            <!-- NEWS -->
            <div v-else-if="currentPage === 'news'">
              <h1 class="text-2xl font-bold mb-6">Твои новости</h1>
              <div v-if="news.length" class="space-y-6 flex flex-col items-center space-x-2">
                <post-main v-for="i in 3"></post-main>
              </div>
              <div v-else class="text-center mt-20 text-gray-400 italic">
                Пока нет опубликованных новостей.
              </div>
            </div>

            <!-- MODERATION -->
            <div v-else-if="currentPage === 'moderation'">
              <h1 class="text-2xl font-bold mb-6">Модерация</h1>
              <div v-if="moderationList.length" class="bg-white p-6 rounded-lg shadow space-y-4">
                <div class="border-b pb-2">
                  <h2 class="text-lg font-semibold">Ожидают проверки</h2>
                </div>
                <div class="space-y-6">
                  <div v-for="i in 3" :key="i" class="flex flex-col items-center">
                    <post-main></post-main>
                    <div class="mt-2 flex flex-wrap gap-2">
                      <button class="bg-green-500 hover:bg-green-600 text-white px-3 py-2 rounded-2xl transition">Одобрить</button>
                      <button class="bg-red-500 hover:bg-red-600 text-white px-3 py-2 rounded-2xl transition">Отклонить</button>
                    </div>
                  </div>
                </div>
              </div>
              <div v-else class="text-center text-gray-400 italic mt-10">Нет публикаций для модерации.</div>
            </div>

        </transition>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import * as icons from 'lucide-vue-next'
import SidebarItem from "@/components/SidebarItem.vue";
import PostMain from "@/components/postMain.vue";


const { Menu } = icons

const currentPage = ref('news')
const sidebarOpen = ref(false)
const profileTab = ref('personal')

const setPage = (page) => {
  currentPage.value = page
  sidebarOpen.value = false
}

const news = ref([
  {
    id: 1,
    title: 'Важное событие в мире технологий и инноваций',
    description: 'Краткое описание новости, которое дает представление о содержании статьи...',
    tags: ['Технологии', 'автобусы', 'dbedbe'],
    likes: 128,
    views: 1200
  },
  {
    id: 2,
    title: 'Новый прорыв в науке',
    description: 'Учёные совершили невероятное открытие, которое может изменить наше представление о мире...',
    tags: ['Наука', 'Исследования'],
    likes: 85,
    views: 920
  }
])

const moderationList = ref([
  { id: 1, title: 'Новое исследование климата', author: 'Алексей Иванов' },
  { id: 2, title: 'Искусственный интеллект в образовании', author: 'Мария Смирнова' }
])
</script>

<style>
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
