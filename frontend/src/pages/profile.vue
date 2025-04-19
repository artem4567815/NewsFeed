<template>
  <div class="flex max-w-[2000px] h-screen bg-gray-50 transition-all ml-auto mr-auto duration-300 ease-in-out flex-col md:flex-row">
    <!-- Sidebar -->
    <aside :class="['md:w-64 w-full md:block', sidebarOpen ? 'block' : 'hidden', 'bg-white border-r p-4 shadow-md fixed md:relative z-10 h-full md:h-auto']">
      <nav class="space-y-4">
        <SidebarItem icon="Newspaper" text="Твои новости" :active="currentPage === 'news'" @click="setPage('news')" />
        <SidebarItem icon="FileEdit" text="Черновики" :active="currentPage === 'drafts'" @click="setPage('drafts')" />
        <SidebarItem icon="ShieldCheck" text="Модерация" v-if="isAdmin" :active="currentPage === 'moderation'" @click="setPage('moderation')" />
        <SidebarItem icon="User" text="Профиль" :active="currentPage === 'profile'" @click="setPage('profile')" />
      </nav>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 p-4 md:p-6 overflow-auto">
      <div class="tab-container">
        <transition name="fade-in" mode="out-in">
          <!-- PROFILE -->
          <div v-if="currentPage === 'profile'">
            <h1 class="text-2xl font-bold mb-6">Профиль</h1>
            <div class="flex flex-col lg:flex-row gap-6">
              <div class="bg-white p-6 rounded-lg shadow w-full lg:w-1/3 text-center">
                <div v-if="profilePage" class="flex w-full justify-center items-center mb-2">
                  <img
                      v-if="profilePage.avatar_url"
                      :src="profilePage.avatar_url"
                      class="w-16 h-16 rounded-full"
                  />
                  <div
                      v-else
                      class="w-16 h-16 rounded-full bg-gradient-to-r from-blue-500 to-blue-600 flex items-center justify-center text-white font-bold text-lg"
                  >
                    {{ profilePage.login.charAt(0) || '?' }}
                  </div>
                </div>
                <h2 class="text-xl font-semibold">
                  <div class="text-nowrap">Имя - {{profilePage.name}}</div>
                  <div class="text-nowrap">Фамилия - {{profilePage.surname}}</div>
                </h2>
                <p class="text-gray-500">Логин - {{profilePage.login}}</p>
                <div class="mt-4">
                  <input
                      type="file"
                      ref="avatarInput"
                      accept="image/*"
                      @change="handleAvatarChange"
                      class="hidden"
                  />
                  <button
                      @click="$refs.avatarInput.click()"
                      class="px-4 py-2 bg-blue-600 hover:bg-blue-700 transition text-white rounded"
                      :disabled="isUploading"
                  >
                    <span v-if="!isUploading">Изменить аватар</span>
                    <span v-else>Загрузка...</span>
                  </button>
                  <p v-if="uploadStatus" class="mt-2 text-sm" :class="uploadStatus.success ? 'text-green-600' : 'text-red-600'">
                    {{ uploadStatus.message }}
                  </p>
                </div>
              </div>

              <div class="bg-white p-6 rounded-lg shadow w-full lg:w-2/3">
                <div class="border-b mb-4 pb-2 flex gap-4 overflow-auto">
                  <button @click="profileTab = 'personal'" :class="['pb-1 whitespace-nowrap', profileTab === 'personal' ? 'text-blue-600 font-medium border-b-2 border-blue-600' : 'text-gray-500 hover:text-blue-600']">Личные данные</button>
                  <button @click="profileTab = 'security'" :class="['pb-1 whitespace-nowrap', profileTab === 'security' ? 'text-blue-600 font-medium border-b-2 border-blue-600' : 'text-gray-500 hover:text-blue-600']">Безопасность</button>
<!--                  <button @click="profileTab = 'notifications'" :class="['pb-1 whitespace-nowrap', profileTab === 'notifications' ? 'text-blue-600 font-medium border-b-2 border-blue-600' : 'text-gray-500 hover:text-blue-600']">Уведомления</button>-->
                </div>

                <div :key="profileTab">
                  <div v-if="profileTab === 'personal'" class="space-y-4">
                    <div class="flex flex-col sm:flex-row gap-4">
                      <div class="flex flex-col w-full">
                        <label class="block w-full text-sm font-medium text-gray-700">Имя</label>
                        <input v-model="profilePage.name" class="w-full border p-2 rounded focus:outline-none focus:ring focus:ring-blue-200" placeholder="Имя" />
                      </div>
                      <div class="flex flex-col w-full">
                        <label class="block w-full text-sm font-medium text-gray-700">Фамилия</label>
                        <input v-model="profilePage.surname" class="w-full border p-2 rounded focus:outline-none focus:ring focus:ring-blue-200" placeholder="Фамилия" />
                      </div>
                    </div>
                    <div class="flex flex-col">
                      <label class="block w-full text-sm font-medium text-gray-700">Логин</label>
                      <input v-model="profilePage.building" class="w-full border p-2 rounded focus:outline-none focus:ring focus:ring-blue-200" placeholder="Login" />
                    </div>
                    <div class="flex w-full justify-between items-center">
                      <button
                          @click="saveProfileChanges"
                          class="px-4 py-2 bg-blue-600 hover:bg-blue-700 transition text-white rounded"
                          :disabled="isSaving"
                      >
                        <span v-if="!isSaving">Сохранить изменения</span>
                        <span v-else>Сохранение...</span>
                      </button>
                      <button
                          @click="exit"
                          class="px-4 py-2 justify-self-end  bg-red-600 hover:bg-red-700 transition text-white rounded"
                      >
                         Выйти из аккаунта
                      </button>
                    </div>
                    <p v-if="saveStatus" class="mt-2 text-sm" :class="saveStatus.success ? 'text-green-600' : 'text-red-600'">
                      {{ saveStatus.message }}
                    </p>
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
              <div class="w-full flex flex-col items-center " v-for="post in DraftPagePosts" :key="post.post_id">
                <post-main :post="post"></post-main>
                <blue-button class="mt-2" :value="post.post_id" @click="to_moderations(post.post_id)">Отправить на модерацию</blue-button>
              </div>
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
                    <button @click="aprove(post.post_id)" class="bg-green-500 hover:bg-green-600 text-white px-3 py-2 rounded-2xl transition">Одобрить</button>
                    <button @click="reject(post.post_id)" class="bg-red-500 hover:bg-red-600 text-white px-3 py-2 rounded-2xl transition">Отклонить</button>
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
import {jwtDecode} from "jwt-decode";
import router from "@/router/router.js";
const { Menu } = icons
import { useRoute } from "vue-router"
import BlueButton from "@/components/UI/blueButton.vue";

const currentPage = ref('news')
const sidebarOpen = ref(false)
const profileTab = ref('personal')

const isAdmin = ref(false) // Добавляем флаг администратора

// Данные
const homePagePosts = ref(null);
const moderationPagePosts = ref(null);
const DraftPagePosts = ref(null);
const profilePage = ref({
  name: '',
  surname: '',
  login: '',
  avatar_url: ''
});

// Состояния
const avatarInput = ref(null);
const uploadStatus = ref(null);
const isUploading = ref(false);
const isSaving = ref(false);
const saveStatus = ref(null);

emitter.on('toggle-sidebar', () => {
  sidebarOpen.value = !sidebarOpen.value
})

const setPage = (page) => {
  currentPage.value = page
  sidebarOpen.value = false
}
const exit = () => {
  localStorage.clear();
  // Дополнительные действия при выходе, если нужно
  window.location.reload(); // или перенаправление на страницу входа
}
// Изменение аватара
const handleAvatarChange = async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  if (file.size > 5 * 1024 * 1024) {
    uploadStatus.value = { success: false, message: 'Файл слишком большой (максимум 5MB)' };
    return;
  }

  if (!file.type.match('image.*')) {
    uploadStatus.value = { success: false, message: 'Пожалуйста, выберите файл изображения' };
    return;
  }

  isUploading.value = true;
  uploadStatus.value = null;

  try {
    const base64DataUrl = await new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result);
      reader.onerror = error => reject(error);
      reader.readAsDataURL(file);
    });
    const response = await jwtApi.patch(
        `${import.meta.env.VITE_BASE_URL}/user/profile`,
        {
          avatar_url: base64DataUrl,
        },
        {
          headers: {
            'Content-Type': 'application/json'
          }
        }
    );

    profilePage.value.avatar_url = base64DataUrl;
    uploadStatus.value = { success: true, message: 'Аватар успешно обновлён' };

  } catch (error) {
    console.error('Ошибка при загрузке аватара:', error);
    uploadStatus.value = {
      success: false,
      message: error.response?.data?.message || 'Ошибка при загрузке аватара'
    };
  } finally {
    isUploading.value = false;
    setTimeout(() => { uploadStatus.value = null; }, 3000);
  }
};
const reason = "хцйавыв"
const to_moderations = async (post_id) => {
  const mods = await jwtApi.post(`${import.meta.env.VITE_BASE_URL}/user/${post_id}/send/to/moderation`, post_id);
  window.location.reload();
}
const aprove = async (post_id) => {
  const apr = await jwtApi.post(`${import.meta.env.VITE_BASE_URL}/admin/moderation/${post_id}/apply`, post_id);
  window.location.reload();
}
const reject = async (post_id) => {
  const rej = await jwtApi.post(`${import.meta.env.VITE_BASE_URL}/admin/moderation/${post_id}/reject`, reason,
      {headers: {'Content-Type': 'application/json'}});
  window.location.reload();
}
// Сохранение изменений профиля
const saveProfileChanges = async () => {
  if (!profilePage.value.name || !profilePage.value.surname || !profilePage.value.login) {
    saveStatus.value = { success: false, message: 'Все поля обязательны для заполнения' };
    return;
  }

  isSaving.value = true;
  saveStatus.value = null;

  try {
    const response = await jwtApi.patch(
        `${import.meta.env.VITE_BASE_URL}/user/profile`,
        {
          name: profilePage.value.name,
          surname: profilePage.value.surname,
        },
        {
          headers: {
            'Content-Type': 'application/json'
          }
        }
    );
    saveStatus.value = { success: true, message: 'Данные успешно сохранены' };

  } catch (error) {
    console.error('Ошибка при сохранении:', error);
    saveStatus.value = {
      success: false,
      message: error.response?.data?.message || 'Ошибка при сохранении данных'
    };
  } finally {
    isSaving.value = false;
    setTimeout(() => { saveStatus.value = null; }, 3000);
  }
};


// Загрузка всех данных при монтировании
onMounted(async () => {
  // Проверяем JWT на наличие прав администратора
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

  try {
    // Загрузка профиля
    const profileRes = await jwtApi.get(`${import.meta.env.VITE_BASE_URL}/user/profile`);
    profilePage.value = profileRes.data;

    // Загрузка новостей
    const allPostsRes = await jwtApi.get(`${import.meta.env.VITE_BASE_URL}/user/HomePage`);
    DraftPagePosts.value = allPostsRes.data.user_posts.filter(post => post.status === "draft");

    // Загрузка модерации (только для админов)
    if (isAdmin.value) {
      const modRes = await jwtApi.get(`${import.meta.env.VITE_BASE_URL}/admin/moderation`);
      moderationPagePosts.value = modRes.data.wall_newspapers;
    }

    // const draftsRes = await jwtApi.get(`${import.meta.env.VITE_BASE_URL}/user/drafts`);
    // homePagePosts.value = draftsRes.data;
    const homePage = await jwtApi.get(`${import.meta.env.VITE_BASE_URL}/user/HomePage`);
    homePagePosts.value = homePage.data.user_posts.filter(post => post.status === "published");

  } catch (error) {
    console.error('Ошибка при запросе данных:', error);
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