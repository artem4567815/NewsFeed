<template>
  <div class="rounded-2xl bg-white p-4 space-y-4 border border-gray-200 shadow-sm">
    <h2 class="text-3xl font-semibold text-gray-900">Фильтры</h2>

    <!-- Поиск -->
    <div>
      <div class="flex items-center mb-1">
        <Search class="h-4 w-4 mr-1" />
        <label class="text-sm text-gray-600 block">Поиск</label>
      </div>
      <input
          v-model="filters.query"
          type="text"
          placeholder="Введите заголовок..."
          class="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
    </div>

    <!-- Школа -->
    <div>
      <div class="flex items-center mb-1">
        <School class="h-4 w-4 mr-1" />
        <label class="text-sm text-gray-600 block">Школа</label>
      </div>
      <select
          v-model="filters.school"
          class="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option value="">Все школы</option>
        <option v-for="school in filterInfo" :key="school" :value="school">
          {{ school }}
        </option>
      </select>
    </div>


    <!-- Категории -->
    <div>
      <label class="text-sm text-gray-600 mb-1 block">Категории</label>
      <div class="space-y-2">
        <div
            v-for="cat in categories"
            :key="cat"
            class="flex items-center gap-2"
        >
          <input
              type="checkbox"
              :value="cat"
              v-model="filters.categories"
              class="form-checkbox text-blue-600 rounded focus:ring-blue-500"
          />
          <span class="text-sm text-gray-700">{{ cat }}</span>
        </div>
      </div>
    </div>

    <!-- Теги -->
    <div>
      <label class="text-sm text-gray-600 mb-1 block">Теги</label>
      <input
          v-model="tagSearch"
          type="text"
          placeholder="Поиск тегов..."
          class="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg mb-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <div class="max-h-40 overflow-y-auto space-y-2">
        <div
            v-for="tag in displayedTags"
            :key="tag"
            class="flex items-center gap-2"
        >
          <input
              type="checkbox"
              :value="tag"
              v-model="filters.tags"
              class="form-checkbox text-blue-600 rounded focus:ring-blue-500"
          />
          <tag-pill :tag="tag" class="text-sm text-gray-700">{{ tag }}</tag-pill>
        </div>
      </div>

      <button
          v-if="!tagSearch"
          @click="showAllTags = !showAllTags"
          class="text-blue-500 text-sm mt-1 hover:underline"
      >
        {{ showAllTags ? 'Скрыть' : 'Показать все теги' }}
      </button>
    </div>

    <!-- Кнопка -->
    <blue-button @click="applyFilters" class="justify-self-center">Применить фильтры</blue-button>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Search, School, Calendar } from 'lucide-vue-next'
import jwtApi from '@/api/jwtApi.js'
import TagPill from "@/components/UI/tagPill.vue";

const emit = defineEmits(['update:filters'])

const filterInfo = ref([])

const tagSearch = ref('')
const allTags = ref([])
const showAllTags = ref(false)

const categories = ['news', 'wallpapers']

const filters = ref({
  query: '',
  school: '',
  period: '',
  categories: [],
  tags: []
})

const displayedTags = computed(() => {
  if (tagSearch.value) {
    return allTags.value.filter(tag =>
        tag.toLowerCase().includes(tagSearch.value.toLowerCase())
    )
  }
  return showAllTags.value ? allTags.value : allTags.value.slice(0, 5)
})

onMounted(async () => {
  try {
    const Info = await jwtApi.get(`${import.meta.env.VITE_BASE_URL}/posts/filter/info`)
    filterInfo.value = Info.data.schools || []
    allTags.value = [...new Set(Info.data.tags || [])]
  } catch (error) {
    console.error('Ошибка при запросе данных:', error)
  }
})

const applyFilters = () => {
  emit('update:filters', {...filters.value})
}
</script>
