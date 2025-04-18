<template>
  <div class="min-h-screen bg-pattern">
    <div class="relative flex justify-center">
      <div class="flex max-w-[2000px] flex-col 2xl:flex-row w-full max-w-screen-3xl mx-auto">
        <!-- Основной контейнер -->
        <div class="flex-1 w-full max-w-screen-2xl px-2 sm:px-8 mx-auto">
          <!-- Заголовок -->
          <div class="bg-blue-100/40 mt-8 backdrop-blur-sm rounded-2xl p-3 text-center flex flex-col justify-center items-center shadow-sm mb-12">
            <div class="text-2xl my-3 font-semibold">Edu<span class="text-blue-500">Feed</span></div>
            <h2 class="text-2xl sm:text-[2rem] font-bold text-[#1F2937] mb-4 leading-tight">
              Добро пожаловать в мир школьных новостей
            </h2>
            <p class="text-base sm:text-lg mb-5 text-gray-600">
              Будьте в курсе последних событий и обновлений из школьной жизни
            </p>
          </div>

          <!-- Основной контент -->
          <div class="space-y-10 w-full lg:w-95/100 justify-self-center flex flex-col items-center">
            <post-main
                v-for="post in posts"
                :key="post.id"
                :post="post"
                @click="$router.push(`/post/${post.post_id}`); View(post.post_id)"
                class="transform hover:scale-[1.02] transition-transform duration-300 w-full"
            />
          </div>

          <!-- Пагинация -->
          <div class="flex justify-center my-8">
            <nav class="inline-flex items-center bg-white/80 backdrop-blur-sm rounded-lg shadow-sm divide-x divide-gray-200">
              <button
                  class="p-3 text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-l-lg"
                  :disabled="currentPage === 1"
                  @click="currentPage--"
              >
                <ChevronLeft />
              </button>

              <button
                  v-for="page in visiblePages"
                  :key="page"
                  @click="currentPage = page"
                  class="px-6 py-3 text-base font-medium"
                  :class="{
    'bg-blue-600 text-white': page === currentPage,
    'text-gray-600 hover:bg-blue-50': page !== currentPage
  }"
              >
                {{ page }}
              </button>

              <button
                  class="p-3 text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-r-lg"
                  :disabled="currentPage === totalPages"
                  @click="currentPage++"
              >
                <ChevronRight />
              </button>
            </nav>
          </div>
        </div>

        <!-- Таймлайн (правая колонка) -->
        <div class="hidden 2xl:block backdrop-blur-[2px] min-h-screen w-[400px]   py-8 px-4">
          <div class="top-8">
            <filter-panel class="mb-6" @update:filters="onFilterUpdate" />
            <div class="bg-white rounded-2xl p-4 border border-gray-200 shadow-sm">
              <div class="flex items-center justify-between mb-8">
                <div>
                  <h2 class="text-lg font-bold text-gray-900 mb-1">История событий</h2>
                  <p class="text-sm text-gray-500">Хронология новостей</p>
                </div>
              </div>
              <div class="max-h-[2305px] overflow-y-auto pr-4 timeline-scroll">
                <timeline-main
                    v-for="timelineBlock in timeline"
                    :key="timelineBlock.post_id"
                    :timeline="timelineBlock"
                    @click="$router.push('/post/id')"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <footer-main></footer-main>
  </div>
</template>


<script setup>
import { ChevronLeft, ChevronRight } from 'lucide-vue-next'
import { ref, watch, onMounted, computed } from 'vue'
import FilterPanel from "@/components/filterPanel.vue"
import TimelineMain from "@/components/timelineMain.vue";
import postMain from "@/components/postMain.vue";
import axios from "axios";

const timeline = ref([])
const posts = ref([])
const filters = ref({
  query: '',
  school: '',
  period: null,
  categories: []
})
const filteredPosts = ref([])

const currentPage = ref(1)
const postsPerPage = 7
const totalPosts = ref(0) // получим из ответа

const totalPages = computed(() => Math.ceil(totalPosts.value / postsPerPage))

const visiblePages = computed(() => {
  const total = totalPages.value
  const current = currentPage.value
  const delta = 2
  const pages = []

  const start = Math.max(1, current - delta)
  const end = Math.min(total, current + delta)

  for (let i = start; i <= end; i++) {
    pages.push(i)
  }

  return pages
})

const tabs = [
  { id: 'all', name: 'Все' },
  { id: 'news', name: 'Новости' },
  { id: 'newspapers', name: 'Стенгазеты' },
  { id: 'team', name: 'Поиск команды' },
  { id: 'tech', name: 'Технологии' },
  { id: 'science', name: 'Наука' },
  { id: 'culture', name: 'Культура' },
  { id: 'sport', name: 'Спорт' }
]
const activeTab = ref('all')

function View(id) {
  console.log(id)
  const ViewPost = async () => {
    try {
      await axios.post(`${import.meta.env.VITE_BASE_URL}/posts/${id}/view`, id) // axios сам вставит заголовки и токен
    } catch (error) {
      console.error('Ошибка лайка:', error)
      // можно добавить уведомление или сообщение пользователю
    }
  }

  ViewPost()
}

function filterPosts(posts, filters) {
  return posts.filter((post) => {
    const matchesQuery =
        !filters.query || post.title.toLowerCase().includes(filters.query.toLowerCase())

    const matchesSchool =
        !filters.school || post.school === filters.school

    const matchesPeriod =
        !filters.period ||
        new Date(post.date) >=
        new Date(Date.now() - filters.period * 24 * 60 * 60 * 1000)

    const matchesCategory =
        !filters.categories.length ||
        filters.categories.includes(post.category)

    return matchesQuery && matchesSchool && matchesPeriod && matchesCategory
  })
}

function onFilterUpdate(newFilters) {
  filters.value = { ...filters.value, ...newFilters }
}

watch(filters, () => {
  filteredPosts.value = filterPosts(posts.value, filters.value)
}, { deep: true, immediate: true })

async function loadPosts() {
  const offset = (currentPage.value - 1) * postsPerPage;

  try {
    const response = await axios.get(`${import.meta.env.VITE_BASE_URL}/posts`, {
      params: {
        limit: postsPerPage,
        offset: offset
      }
    });

    posts.value = response.data.posts;
    console.log(posts.value);
    totalPosts.value = response.data.posts_count;
    console.log(response.data.posts_count); // зависит от API
  } catch (error) {
    console.error('Ошибка загрузки постов:', error);
    if (error.response) {
      // Ошибка с ответом от сервера
      console.error('Статус ошибки:', error.response.status);
      console.error('Данные ошибки:', error.response.data);
    } else if (error.request) {
      // Запрос был сделан, но ответ не получен
      console.error('Ответ не получен:', error.request);
    } else {
      // Ошибка при настройке запроса
      console.error('Ошибка:', error.message);
    }
  }
}
async function loadTimeline() {
  console.log(totalPosts.value);
  try {
    const response = await axios.get(`${import.meta.env.VITE_BASE_URL}/posts`, {
      params: {
        limit: totalPosts.value,
        offset: 0
      }
    });
    timeline.value = response.data.posts;
    console.log(timeline.value);
  } catch (error) {
    console.error('Ошибка загрузки постов:', error);
    if (error.response) {
      console.error('Статус ошибки:', error.response.status);
      console.error('Данные ошибки:', error.response.data);
    } else if (error.request) {
      console.error('Ответ не получен:', error.request);
    } else {
      console.error('Ошибка:', error.message);
    }
  }
}
onMounted(async () => {
  await loadPosts()
  await loadTimeline()
})
watch(currentPage, () => {
  loadPosts()
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  })
})
</script>

<style>
/* Плавная прокрутка */
html {
  scroll-behavior: smooth;
}

/* Фоновый паттерн */
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

/* Стилизация скроллбара */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}

/* Сброс стилей */
button {
  -webkit-tap-highlight-color: transparent;
}

/* Стилизация скроллбара таймлайна */
.timeline-scroll::-webkit-scrollbar {
  width: 4px;
}

.timeline-scroll::-webkit-scrollbar-track {
  background: transparent;
}

.timeline-scroll::-webkit-scrollbar-thumb {
  background: #e5e7eb;
  border-radius: 4px;
}

.timeline-scroll::-webkit-scrollbar-thumb:hover {
  background: #d1d5db;
}

/* Стилизация скроллбара таймлайна в зеленой теме */
.timeline-scroll::-webkit-scrollbar-thumb {
  background: #a7f3d0;
}

.timeline-scroll::-webkit-scrollbar-thumb:hover {
  background: #6ee7b7;
}

.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
