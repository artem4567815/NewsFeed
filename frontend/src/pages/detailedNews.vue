<template>
  <div class="min-h-screen bg-pattern">
    <!-- Состояние загрузки -->
    <div v-if="isLoading" class="flex justify-center items-center h-screen">
      <div class="animate-pulse space-y-4 w-full max-w-2xl px-4">
        <div class="h-10 bg-gray-200 rounded w-3/4 mx-auto"></div>
        <div class="h-6 bg-gray-200 rounded w-1/2 mx-auto"></div>
        <div class="h-64 bg-gray-200 rounded-xl"></div>
        <div class="space-y-2">
          <div class="h-4 bg-gray-200 rounded w-full"></div>
          <div class="h-4 bg-gray-200 rounded w-5/6"></div>
        </div>
      </div>
    </div>

    <!-- Состояние ошибки -->
    <div v-else-if="error" class="flex justify-center items-center h-screen">
      <div class="text-center p-6 max-w-md">
        <div class="text-red-500 mb-4 text-5xl">⚠️</div>
        <h2 class="text-xl font-bold text-gray-800 mb-2">Ошибка загрузки</h2>
        <p class="text-gray-600 mb-4">{{ error }}</p>
        <button
            @click="loadPost"
            class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
        >
          Попробовать снова
        </button>
      </div>
    </div>

    <!-- Успешная загрузка -->
    <div v-else-if="post" class="relative flex justify-center">
      <div class="flex w-full justify-center max-w-[2000px]">
        <div class="flex-1 p-2 sm:p-8 2xl:max-w-[calc(100%-280px)]">
          <!-- Заголовок новости -->
          <div class="mb-8">
            <div class="flex items-center gap-2 mb-4">
              <h1 class="text-3xl font-bold break-all  text-gray-900 sm:text-4xl">{{ post.title }}</h1>
            </div>

            <div class="flex flex-wrap items-center gap-4 text-sm text-gray-500">
              <div class="flex items-center gap-2">
                <span class="font-medium text-gray-700">{{ post.author?.login || 'Неизвестный автор' }}</span>
              </div>
              <div class="flex items-center gap-2">
                <CalendarDays class="w-4 h-4" />
                <span>{{ timestampToDate(post.start_date) }} - {{ timestampToDate(post.end_date) }}</span>
              </div>
              <div class="flex items-center gap-2">
                <Eye class="w-4 h-4" />
                <span>{{ post.views }} просмотров</span>
              </div>
              <div class="flex flex-wrap gap-2 ml-auto sm:ml-0">

              <span v-if="post.type" class="px-3 py-1 text-sm font-medium rounded-full bg-blue-100 text-blue-800">
                {{ postTypeLabel(post.type) }}
              </span>
              <span v-if="fromProfile" class="px-3 py-1 text-sm font-medium rounded-full" :class="[getStatusLabel(post.status).bg, getStatusLabel(post.status).text]">
                {{ getStatusLabel(post.status).label }}
              </span>
              </div>

            </div>
          </div>

          <!-- Основное содержимое -->
          <div class="bg-white rounded-2xl shadow-sm overflow-hidden mb-8">
            <!-- Изображение новости -->
            <img
                v-if="post.image_url"
                :src="post.image_url"
                :alt="post.title"
                class="w-full aspect-16/9 lg:h-full object-cover"
            />

            <!-- Текст новости -->
            <div class="p-6 sm:p-8">
              <p class="text-lg break-all text-gray-700 mb-6">
                {{ post.short_content }}
              </p>

              <div class="prose max-w-none break-all prose break-words text-gray-700 mb-8" v-html="post.full_content"></div>

              <!-- Действия -->
              <div class="flex flex-wrap items-center justify-between gap-4 pt-6 border-t border-gray-200">
                <div class="flex items-center gap-2">
                  <button
                      @click="toggleLike"
                      class="flex items-center gap-2 px-4 py-2 text-sm font-medium rounded-lg transition-all"
                      :class="{
      'text-red-500 bg-red-50 hover:bg-red-100': isLiked,
      'text-gray-700 bg-gray-100 hover:bg-gray-200': !isLiked
    }"
                  >
                    <Heart
                        :fill="isLiked ? '#eb2525' : 'none'"
                        :stroke="isLiked ? '#eb2525' : 'currentColor'"
                        class="w-5 h-5 transition-all"
                    />
                    <span>{{ likesCount }}</span>
                  </button>
                </div>
<!--                <div class="flex items-center gap-2">-->
<!--                  <button class="flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200">-->
<!--                    <Share2 class="w-4 h-4" />-->
<!--                    <span>Поделиться</span>-->
<!--                  </button>-->
<!--                </div>-->
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <FooterMain />
  </div>
</template>

<script setup>
import { CalendarDays, Eye, Heart, Share2 } from 'lucide-vue-next'
import { ref, onMounted, computed } from 'vue'
import { useRoute } from "vue-router"
import FooterMain from "@/components/footerMain.vue"
import axios from "axios";
import api from "@/api/axios.js";

const route = useRoute()
const post = ref(null)
const isLoading = ref(true)
const error = ref(null)

import router, { previousRoute } from '@/router/router.js'
import jwtApi from "@/api/jwtApi.js"; // или откуда ты сохраняешь предыдущий путь

const fromProfile = ref(false)

onMounted(() => {

  if (previousRoute.path === '/profile') {
    fromProfile.value = true
  }
})


const getStatusLabel = (status) => {
  const statuses = {
    draft: { label: 'Черновик', bg: 'bg-gray-200', text: 'text-gray-700' },
    pending: { label: 'На модерации', bg: 'bg-yellow-200', text: 'text-yellow-800' },
    rejected: { label: 'Отклонено', bg: 'bg-red-200', text: 'text-red-800' },
    published: { label: 'Опубликовано', bg: 'bg-green-200', text: 'text-green-800' },

  };
  return statuses[status] || { label: status, bg: 'bg-green-100', text: 'text-green-700' };
};

const postTypeLabel = (type) => {
  const types = {
    news: 'Новость',
    event: 'Мероприятие',
    announcement: 'Объявление'
  }
  return types[type] || type
}

// Загружаем данные при монтировании
const likedPosts = ref([]) // Массив ID лайкнутых постов
const likesCount = ref(0) // Счетчик лайков для текущего поста

// Загружаем лайки пользователя
const loadLikes = async () => {
  try {
    const response = await jwtApi.get(`${import.meta.env.VITE_BASE_URL}/user/my-likes`)
    likedPosts.value = response.data.posts_liked_by_user || []
  } catch (err) {
    console.error('Ошибка загрузки лайков:', err)
  }
}

// Проверяем, лайкнул ли пользователь текущий пост
const isLiked = computed(() => {
  return post.value ? likedPosts.value.includes(post.value.post_id) : false
})

// Обработчик лайка/дизлайка
const toggleLike = async () => {
  if (!post.value) return

  // Проверка авторизации
  if (!localStorage.getItem('authToken')) {
    router.push('/auth')
    return
  }

  try {
    if (isLiked.value) {
      // Дизлайк
      await jwtApi.post(`${import.meta.env.VITE_BASE_URL}/posts/${post.value.post_id}/unlike`)
      likedPosts.value = likedPosts.value.filter(id => id !== post.value.post_id)
      likesCount.value--
    } else {
      // Лайк
      await jwtApi.post(`${import.meta.env.VITE_BASE_URL}/posts/${post.value.post_id}/like`)
      likedPosts.value.push(post.value.post_id)
      likesCount.value++
    }
  } catch (err) {
    console.error('Ошибка при лайке:', err)
    toast.error('Не удалось выполнить действие')
  }
}

// Загрузка поста
const loadPost = async () => {
  try {
    isLoading.value = true
    error.value = null

    const response = await axios.get(`${import.meta.env.VITE_BASE_URL}/posts/${route.params.id}`)
    post.value = response.data
    likesCount.value = response.data.likes_count || 0

    // Загружаем лайки после загрузки поста
    await loadLikes()
    window.scrollTo({ top: 0, behavior: 'auto' })

  } catch (err) {
    error.value = axios.isAxiosError(err)
        ? err.response?.status === 404
            ? 'Новость не найдена'
            : 'Ошибка сервера'
        : 'Неизвестная ошибка'
    console.error('Ошибка загрузки:', err)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  loadPost()
})

function timestampToDate(ts) {
  const date = new Date(ts * 1000); // если timestamp в секундах
  const day = String(date.getDate()).padStart(2, '0');
  const month = String(date.getMonth() + 1).padStart(2, '0'); // месяцы с 0
  const year = date.getFullYear();
  return `${day}.${month}.${year}`;
}

function timeAgo(timestampSec) {
  const now = Date.now();
  const timestampMs = timestampSec * 1000; // Переводим секунды в миллисекунды
  const seconds = Math.floor((now - timestampMs) / 1000);

  const intervals = [
    { label: ['секунда', 'секунды', 'секунд'], seconds: 1 },
    { label: ['минута', 'минуты', 'минут'], seconds: 60 },
    { label: ['час', 'часа', 'часов'], seconds: 3600 },
    { label: ['день', 'дня', 'дней'], seconds: 86400 },
    { label: ['неделя', 'недели', 'недель'], seconds: 604800 },
    { label: ['месяц', 'месяца', 'месяцев'], seconds: 2592000 },
    { label: ['год', 'года', 'лет'], seconds: 31536000 },
  ];

  function getPlural(n, forms) {
    const mod10 = n % 10;
    const mod100 = n % 100;
    if (mod10 === 1 && mod100 !== 11) return forms[0];
    if (mod10 >= 2 && mod10 <= 4 && (mod100 < 10 || mod100 >= 20)) return forms[1];
    return forms[2];
  }

  for (let i = intervals.length - 1; i >= 0; i--) {
    const interval = intervals[i];
    const count = Math.floor(seconds / interval.seconds);
    if (count >= 1) {
      const label = getPlural(count, interval.label);
      return `${count} ${label} назад`;
    }
  }

  return 'только что';
}
</script>

<style scoped>
/* Стили остаются без изменений */
.bg-pattern {
  background: linear-gradient(135deg, #f6f8ff 0%, #f0f4ff 100%);
  background-image:
      radial-gradient(at 20% 25%, rgba(59, 130, 246, 0.04) 0px, transparent 50%),
      radial-gradient(at 80% 75%, rgba(99, 102, 241, 0.03) 0px, transparent 50%),
      radial-gradient(at 50% 50%, rgba(139, 92, 246, 0.05) 0px, transparent 50%);
  background-attachment: fixed;
  background-size: cover;
  position: relative;
}

.bg-pattern::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%236366f1' fill-opacity='0.02'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  opacity: 0.5;
  pointer-events: none;
}
</style>