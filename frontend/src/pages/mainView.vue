<template>
  <div class="min-h-screen bg-pattern">
    <div class="relative flex justify-center">
      <div class="flex flex-col 2xl:flex-row w-full max-w-screen-3xl mx-auto">
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
                v-for="post in 5"
                :key="post.id"
                :post="post"
                @click="$router.push(`/post/${post.id}`)"
                class="transform hover:scale-[1.02] transition-transform duration-300 w-full"
            />
          </div>

          <!-- Пагинация -->
          <div class="flex justify-center mt-16">
            <nav class="inline-flex items-center bg-white/80 backdrop-blur-sm rounded-lg shadow-sm divide-x divide-gray-200">
              <button class="p-3 text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-l-lg">
                <ChevronLeft />
              </button>
              <button class="px-6 py-3 text-base font-medium text-white bg-blue-600">1</button>
              <button class="px-6 py-3 text-base font-medium text-gray-600 hover:bg-blue-50">2</button>
              <button class="px-6 py-3 text-base font-medium text-gray-600 hover:bg-blue-50">3</button>
              <button class="p-3 text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-r-lg">
                <ChevronRight />
              </button>
            </nav>
          </div>
        </div>

        <!-- Таймлайн (правая колонка) -->
        <div class="hidden 2xl:block backdrop-blur-[2px] min-h-screen py-8 px-4">
          <div class="top-8">
            <filter-panel class="mb-6" @update:filters="onFilterUpdate" />
            <div class="bg-white rounded-2xl p-4 border border-gray-200 shadow-sm">
              <div class="flex items-center justify-between mb-8">
                <div>
                  <h2 class="text-lg font-bold text-gray-900 mb-1">История событий</h2>
                  <p class="text-sm text-gray-500">Хронология новостей</p>
                </div>
              </div>
              <div class="max-h-[calc(100vh-180px)] overflow-y-auto pr-4 timeline-scroll">
                <timeline-main
                    v-for="(item, index) in timelineItems"
                    :key="index"
                    :title="item.title"
                    :start-date="item.date"
                    :time-passed="item.timePassed"
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
import { ref, watch, onMounted } from 'vue'
import FilterPanel from "@/components/filterPanel.vue"

const posts = ref([])
const filters = ref({
  query: '',
  school: '',
  period: null,
  categories: []
})
const filteredPosts = ref([])

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

const timelineItems = [
  {
    title: "Важное событие в мире технологий",
    date: "15.03.2024",
    timePassed: "2 часа назад"
  },
  {
    title: "Новый прорыв в науке",
    date: "14.03.2024",
    timePassed: "1 день назад"
  },
  {
    title: "Интересные новости экономики",
    date: "13.03.2024",
    timePassed: "2 дня назад"
  },
  {
    title: "Культурное событие года",
    date: "12.03.2024",
    timePassed: "3 дня назад"
  },
  {
    title: "Спортивные достижения",
    date: "11.03.2024",
    timePassed: "4 дня назад"
  }
]

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

onMounted(async () => {
  try {
    const NewsResponse = await fetch(`${import.meta.env.VITE_BASE_URL}/posts?type=news`)
    if (!NewsResponse.ok) throw new Error('Ошибка при загрузке новостей')
    posts.value = await NewsResponse.json()
  } catch (error) {
    console.error('Ошибка загрузки новостей:', error)
  }
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
