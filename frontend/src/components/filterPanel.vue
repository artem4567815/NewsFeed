<template>
  <div class="rounded-2xl bg-white p-4 space-y-4 border border-gray-200 shadow-sm">
    <h2 class="text-lg font-semibold text-gray-900">Фильтры</h2>

    <!-- Поиск -->
    <div>
      <div class="flex items-center mb-1">
        <Search class="h-4 w-4 mr-1" />
      <label class="text-sm text-gray-600  block">Поиск</label>
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
        <option value=""> Все школы</option>
        <option v-for="school in schools" :key="school" :value="school">
          {{ school }}
        </option>
      </select>
    </div>

    <!-- Период -->
    <div>
      <div class="flex items-center mb-1">
        <Calendar class="h-4 w-4 mr-1" />
      <label class="text-sm text-gray-600  block">Период</label>
      </div>
      <select
          v-model="filters.period"
          class="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option value="">За всё время</option>
        <option value="7">Последние 7 дней</option>
        <option value="30">Последние 30 дней</option>
        <option value="365">Последний год</option>
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

    <!-- Кнопка -->
    <blue-button @click="applyFilters" class="justify-self-center">Применить фильтры</blue-button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import {Search, School, Calendar} from "lucide-vue-next";

const emit = defineEmits(['update:filters'])

const filters = ref({
  query: '',
  school: '',
  period: '',
  categories: [],
})

const schools = ['Школа №1', 'Гимназия №3', 'Лицей №7']
const categories = ['Новости', 'События', 'Объявления']

const applyFilters = () => {
  emit('update:filters', { ...filters.value })
}
</script>
