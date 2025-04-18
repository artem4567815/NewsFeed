<template>
  <div class="flex max-w-[2000px] h-screen bg-gray-50 transition-all ml-auto mr-auto duration-300 ease-in-out flex-col md:flex-row">
    <!-- Sidebar -->
    <aside :class="['md:w-64 w-full md:block', sidebarOpen ? 'block' : 'hidden', 'bg-white border-r p-4 shadow-md fixed md:relative z-10 h-full md:h-auto']">
      <nav class="space-y-4">
        <SidebarItem icon="Newspaper" text="Твои новости" :active="currentPage === 'news'" @click="setPage('news')" />
        <SidebarItem icon="FileEdit" text="Черновики" :active="currentPage === 'drafts'" @click="setPage('drafts')" />
        <SidebarItem icon="ShieldCheck" text="Модерация" :active="currentPage === 'moderation'" @click="setPage('moderation')" />
        <SidebarItem icon="User" text="Профиль" :active="currentPage === 'profile'" @click="setPage('profile')" />
      </nav>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 p-4 md:p-6 overflow-auto ">
      <div class="tab-container">
        <transition name="fade-in" mode="out-in">

          <!-- PROFILE -->
          <div v-if="currentPage === 'profile'">
            <h1 class="text-2xl font-bold mb-6">Профиль</h1>
            <div class="flex flex-col lg:flex-row gap-6">
              <div class="bg-white p-6 rounded-lg shadow w-full lg:w-1/3 text-center">
<!--                <img :src="posts[0].image_url" alt="avatar" class="rounded-full w-24 h-24 mx-auto mb-4" />-->
                <h2 class="text-xl font-semibold">
                  <div class="text-nowrap">Имя - {{profilePage.name}}</div>
                  <div class="text-nowrap">Фамилия - {{profilePage.surname}}</div>
                </h2>
                <p class="text-gray-500">Логин - {{profilePage.login}}</p>
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
                      <div class="flex flex-col w-full">
                        <label class="block w-full text-sm font-medium text-gray-700">Имя</label>
                        <input class="w-full  border p-2 rounded focus:outline-none focus:ring focus:ring-blue-200" placeholder="Имя" :value="profilePage.name" />
                      </div>
                      <div class="flex flex-col w-full">
                        <label class="block w-full text-sm font-medium text-gray-700">Фамилия</label>
                        <input class="w-full  border p-2 rounded focus:outline-none focus:ring focus:ring-blue-200" placeholder="Фамилия" :value="profilePage.surname" />
                      </div>
                    </div>
                    <div class="flex flex-col">
                      <label class="block w-full text-sm font-medium text-gray-700">Логин</label>
                      <input class="w-full border p-2 rounded focus:outline-none focus:ring focus:ring-blue-200" placeholder="Login" :value="profilePage.login" />
                    </div>
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
          <div v-else-if="currentPage === 'drafts'">
            <h1 class="text-2xl font-bold mb-6">Твои черновики</h1>
            <div v-if="DraftPagePosts && DraftPagePosts.length" class="space-y-6 flex flex-col items-center space-x-2">
              <post-main v-for="post in DraftPagePosts" :key="post.post_id" :post="post"></post-main>
            </div>
            <div v-else class="text-center mt-20">
              <h1 class="text-2xl font-bold mb-2">У вас пока нет черновиков</h1>
              <p class="text-gray-500 mb-6">Здесь будут отображаться ваши сохраненные черновики.</p>
              <button @click="$router.push('/Create')" class="px-4 py-2 bg-blue-600 hover:bg-blue-700 transition text-white rounded">Создать новость</button>
            </div>
          </div>

          <!-- NEWS -->
          <div v-else-if="currentPage === 'news'">
            <h1 class="text-2xl font-bold mb-6">Твои новости</h1>
            <div v-if="homePagePosts && homePagePosts.length" class="space-y-6 flex flex-col items-center space-x-2">
              <post-main v-for="post in homePagePosts" :key="post.post_id" :post="post"></post-main>
            </div>
            <div v-else class="text-center mt-20">
              <h1 class="text-2xl font-bold mb-2">У вас пока нет опубликованных новостей</h1>
              <p class="text-gray-500 mb-6">Создайте свою первую новость и поделитесь ей с другими</p>
              <button
                  class="px-4 py-2 bg-blue-600 hover:bg-blue-700 transition text-white rounded"
                  @click="$router.push('/Create')"
              >
                Создать новость
              </button>
            </div>
          </div>

          <!-- MODERATION -->
          <div v-else-if="currentPage === 'moderation'">
            <h1 class="text-2xl font-bold mb-6">Модерация</h1>
            <div v-if="moderationPagePosts && moderationPagePosts.length" class="bg-white p-6 rounded-lg shadow space-y-4">
              <div class="border-b pb-2">
                <h2 class="text-lg font-semibold">Ожидают проверки</h2>
              </div>
              <div class="space-y-6">
                <div v-for="post in moderationPagePosts" :key="post"  class="flex flex-col items-center">
                  <post-main :post="post"></post-main>
                  <div class="mt-2 flex flex-wrap gap-2">
                    <button class="bg-green-500 hover:bg-green-600 text-white px-3 py-2 rounded-2xl transition">Одобрить</button>
                    <button class="bg-red-500 hover:bg-red-600 text-white px-3 py-2 rounded-2xl transition">Отклонить</button>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="text-center mt-20">
              <h1 class="text-2xl font-bold mb-2">Нет публикаций для модерации</h1>
              <p class="text-gray-500 mb-6">Все публикации проверены или ожидают отправки на модерацию</p>
            </div>
          </div>

        </transition>
      </div>
    </main>
  </div>
</template>

<script setup>
import {onMounted, ref} from 'vue'
import * as icons from 'lucide-vue-next'
import SidebarItem from "@/components/SidebarItem.vue";
import PostMain from "@/components/postMain.vue";
import emitter from '@/main.js'
import jwtApi from "@/api/jwtApi.js";

const { Menu } = icons

const currentPage = ref('news')
const sidebarOpen = ref(false)
const profileTab = ref('personal')


emitter.on('toggle-sidebar', () => {
  sidebarOpen.value = !sidebarOpen.value
})

const setPage = (page) => {
  currentPage.value = page
  sidebarOpen.value = false
}


const homePagePosts = ref(null);

onMounted(async () => {
  try {
    const res = await jwtApi.get(`${import.meta.env.VITE_BASE_URL}/user/HomePage`, {
    });
    homePagePosts.value = res.data.user_posts
    console.log(homePagePosts.value)
  } catch (error) {
    console.error('Ошибка при запросе:', error);
  }
});

const moderationPagePosts = ref(null);

onMounted(async () => {
  try {
    const res = await jwtApi.get(`${import.meta.env.VITE_BASE_URL}/admin/moderation`, {
    });
    moderationPagePosts.value = res.data.wall_newspapers
    console.log(moderationPagePosts.value)
  } catch (error) {
    console.error('Ошибка при запросе:', error);
  }
});

const DraftPagePosts = ref(null);
onMounted(async () => {
  try {
    const res = await jwtApi.get(`${import.meta.env.VITE_BASE_URL}/admin/moderation`, {
    });
    DraftPagePosts.value = res.data
    console.log(DraftPagePosts.value)
  } catch (error) {
    console.error('Ошибка при запросе:', error);
  }
});

const profilePage = ref(null);
onMounted(async () => {
  try {
    const res = await jwtApi.get(`${import.meta.env.VITE_BASE_URL}/user/profile`, {
    });
    profilePage.value = res.data
    console.log(profilePage.value)
  } catch (error) {
    console.error('Ошибка при запросе:', error);
  }
});
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