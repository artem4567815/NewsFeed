<template>
  <div class="min-h-screen bg-pattern">
    <!-- Заголовок формы -->
    <div class="bg-blue-100/40 w-89/100 justify-self-center mt-5 backdrop-blur-sm rounded-2xl p-0 sm:p-3 text-center flex flex-col justify-center items-center shadow-sm">
      <div class="text-2xl my-3 text-center font-semibold">Edu<span class="text-blue-500">Feed</span></div>
      <h2 class="lg:text-[2.5rem] text-[1.5rem] font-bold text-[#1F2937] mb-4 leading-tight">Создание новости</h2>
      <p class="text-lg sm:text-xl mb-5 text-gray-600">Расскажи всем о своём уникальном событии!</p>
    </div>

    <form @submit.prevent="submitForm" class="flex flex-col items-center py-8">
      <div class="bg-white rounded-2xl shadow-lg overflow-hidden w-90/100 max-w-450 transition-transform duration-300 ease-out">
        <div class="flex flex-col lg:flex-row h-full">
          <div class="flex flex-col w-full">
          <!-- Блок загрузки изображения -->
            <div
                class="aspect-video h-full w-full relative overflow-hidden bg-gray-100 hover:bg-gray-200 transition-colors duration-200 flex items-center justify-center cursor-pointer"
                @click.stop="triggerFileInput"
            >
              <input ref="imageInput" type="file" accept="image/*" class="hidden" @change="handleImageUpload" />

              <img
                  v-show="imagePreview"
                  :src="imagePreview"
                  class="absolute inset-0 w-full h-full object-cover"
                  alt="Превью изображения"
              />
              <div class="text-center i-100 p-6">
                <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-blue-100 mb-4">
                  <Upload class="h-6 w-6 text-blue-600" />
                </div>
                <p class="text-lg font-medium text-gray-700 mb-1">Загрузите изображение</p>
                <p class="text-gray-500 mb-4">или</p>
                <blue-button
                    type="button"
                    @click.stop="router.push('/Create/Cover')"
                >
                  Создайте свое
                </blue-button>
              </div>
            </div>
          <div v-show="imageError" class="text-red-500 text-sm mt-1 px-6">Изображение обязательно</div>
          </div>
          <!-- Форма ввода -->
          <div class="flex-1 p-6 lg:min-w-120 flex flex-col">
            <!-- Выбор типа публикации -->
            <div class="mb-6">
              <label class="block text-sm font-medium text-gray-700 mb-2">Тип публикации</label>
              <div class="flex flex-wrap gap-2">
                <button
                    v-for="type in publicationTypes"
                    :key="type.value"
                    type="button"
                    @click="postData.type = type.value"
                    class="px-3 py-1.5 rounded-md text-sm transition-colors"
                    :class="{
                      'bg-blue-500 text-white': postData.type === type.value,
                      'bg-gray-100 hover:bg-gray-200': postData.type !== type.value
                    }"
                >
                  {{ type.label }}
                </button>
              </div>
            </div>

            <!-- Заголовок -->
            <div class="mb-6">
              <label for="NewsName" class="block text-sm font-medium text-gray-700 mb-1">Название новости</label>
              <input
                  v-model="postData.title"
                  @input="validateTitle"
                  type="text"
                  id="NewsName"
                  required
                  maxlength="100"
                  class="block w-full px-4 py-3 text-xl font-bold text-gray-900 bg-gray-50 rounded-lg border"
                  :class="{'border-gray-300': !titleError, 'border-red-500': titleError}"
                  placeholder="Введите заголовок новости (макс. 100 символов)"
              >
              <div v-if="titleError" class="text-red-500 text-sm mt-1">{{ titleError }}</div>
              <div class="text-gray-500 text-xs text-right mt-1">
                {{ postData.title.length }}/100 символов
              </div>
            </div>

            <!-- Краткое описание -->
            <div class="mb-6">
              <label for="shortDesc" class="block text-sm font-medium text-gray-700 mb-1">Краткое описание</label>
              <textarea
                  v-model="postData.short_content"
                  @input="validateShortDescription"
                  id="shortDesc"
                  required
                  rows="3"
                  maxlength="200"
                  class="block w-full px-4 py-3 text-base text-gray-700 bg-gray-50 rounded-lg border"
                  :class="{'border-gray-300': !shortDescriptionError, 'border-red-500': shortDescriptionError}"
                  placeholder="Краткое описание новости (макс. 200 символов)"
              ></textarea>
              <div v-if="shortDescriptionError" class="text-red-500 text-sm mt-1">{{ shortDescriptionError }}</div>
              <div class="text-gray-500 text-xs text-right mt-1">
                {{ postData.short_content.length }}/200 символов
              </div>
            </div>

            <!-- Теги -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Теги (максимум 4)</label>

              <!-- Выбранные теги -->
              <div class="flex flex-wrap gap-2 mb-2">
                <span
                    v-for="(tag, index) in selectedTags"
                    :key="index"
                    class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium"
                    :class="tagClasses(index)"
                >
                  {{ tag }}
                  <button
                      type="button"
                      @click.stop="removeTag(index)"
                      class="ml-1 text-gray-500 hover:text-gray-700"
                  >
                    ×
                  </button>
                </span>
              </div>

              <!-- Доступные теги -->
              <div class="flex flex-wrap gap-2 mb-2">
                <span
                    v-for="(tag, index) in availableTags"
                    :key="'available-'+index"
                    @click="selectTag(tag)"
                    class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-gray-100 text-gray-800 cursor-pointer hover:bg-gray-200"
                    :class="{ 'opacity-50': selectedTags.includes(tag) }"
                >
                  {{ tag }}
                </span>
              </div>

              <!-- Поле для добавления нового тега -->
              <div class="flex md:flex-row flex-col items-start md:items-center gap-2 mt-2">
                <input
                    type="text"
                    v-model="newTag"
                    @keydown.enter.prevent="addTag"
                    class="flex-1 px-3 py-1 text-sm border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                    placeholder="Добавить свой тег"
                    maxlength="20"
                >
                <button
                    type="button"
                    @click="addTag"
                    class="px-3 py-1 bg-blue-500 text-white text-sm rounded-md hover:bg-blue-600"
                >
                  Добавить
                </button>
              </div>
              <div v-if="tagsError" class="text-red-500 text-sm mt-1">{{ tagsError }}</div>
            </div>
          </div>
        </div>

        <!-- Дополнительные поля -->
        <div class="p-6 border-t border-gray-200">
          <!-- Полное описание -->
          <div class="mb-6">
            <label for="Desc" class="block text-sm font-medium text-gray-700 mb-1">Описание</label>
            <textarea
                v-model="postData.content"
                @input="validateContent"
                id="Desc"
                required
                rows="5"
                class="block w-full px-4 py-3 text-base text-gray-700 bg-gray-50 rounded-lg border"
                :class="{'border-gray-300': !contentError, 'border-red-500': contentError}"
                placeholder="Полное описание новости"
            ></textarea>
            <div v-if="contentError" class="text-red-500 text-sm mt-1">{{ contentError }}</div>
            <div class="text-gray-500 text-xs text-right mt-1">
              {{ postData.content.length }}/5000 символов
            </div>
          </div>

          <!-- Даты -->
          <div class="mb-6 space-x-6 flex flex-col sm:flex-row items-start md:items-center gap-4 mt-2">
            <div class="w-full">
              <label for="start_date" class="block text-sm font-medium text-gray-700 mb-1">Дата начала</label>
              <input
                  v-model="postData.start_date"
                  @change="validateDates"
                  type="date"
                  id="start_date"
                  required
                  class="block w-full px-4 py-3 text-base text-gray-700 bg-gray-50 rounded-lg border"
                  :class="{'border-gray-300': !dateError, 'border-red-500': dateError}"
              >
            </div>

            <div class="w-full">
              <label for="end_date" class="block text-sm font-medium text-gray-700 mb-1">Дата окончания</label>
              <input
                  v-model="postData.end_date"
                  @change="validateDates"
                  type="date"
                  id="end_date"
                  required
                  class="block w-full px-4 py-3 text-base text-gray-700 bg-gray-50 rounded-lg border"
                  :class="{'border-gray-300': !dateError, 'border-red-500': dateError}"
              >
            </div>
          </div>
          <div v-if="dateError" class="text-red-500 text-sm mt-1">{{ dateError }}</div>
        </div>

        <!-- Кнопка отправки -->
        <div class="p-6 border-t border-gray-200 flex justify-center lg:justify-end">
          <blue-button
              type="submit"
              :disabled="isSubmitting || hasErrors"
          >
            <span v-if="isSubmitting">Публикация...</span>
            <span v-else>Опубликовать новость</span>
          </blue-button>
        </div>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, computed, onBeforeMount } from 'vue'
import { useRouter } from 'vue-router'
import { CalendarDays, Upload } from 'lucide-vue-next'
import jwtApi from "@/api/jwtApi.js";
import axios from "axios";

const router = useRouter()

// Refs
const imageInput = ref(null)
const imagePreview = ref(null)
const isSubmitting = ref(false)
const newTag = ref('')

// Ошибки валидации
const titleError = ref('')
const shortDescriptionError = ref('')
const contentError = ref('')
const dateError = ref('')
const imageError = ref('')
const tagsError = ref('')

const publicationTypes = [
  { value: 'news', label: 'Новость' },
  { value: 'wallpapers', label: 'Стенгазета' },
  // { value: 'team_search', label: 'Поиск команды' }
]

// Теги
const availableTags = ref([
  'Технологии', 'Образование', 'Школа',
  'Программирование', 'Дизайн', 'Бизнес',
  'Наука', 'Искусство', 'Маркетинг', 'Стартапы'
])
const selectedTags = ref([])

// Данные поста
const postData = ref({
  title: "",
  type: "news",
  content: "",
  short_content: "",
  start_date: "",
  end_date: "",
  post_img: null,
  post_img_detail: ""
})

// Computed
const currentDate = computed(() => new Date().toLocaleDateString())

// Проверяем есть ли ошибки
const hasErrors = computed(() => {
  return !!(
      titleError.value ||
      shortDescriptionError.value ||
      contentError.value ||
      dateError.value ||
      imageError.value ||
      tagsError.value
  )
})

// Валидация изображения
const validateImage = () => {
  if (!postData.value.post_img) {
    imageError.value = 'Изображение обязательно'
    return false
  }
  imageError.value = ''
  return true
}

// Валидация заголовка
const validateTitle = () => {
  if (postData.value.title.length > 100) {
    titleError.value = 'Заголовок не должен превышать 100 символов'
    return false
  } else if (postData.value.title.length < 5) {
    titleError.value = 'Заголовок должен содержать минимум 5 символов'
    return false
  } else {
    titleError.value = ''
    return true
  }
}

// Валидация краткого описания
const validateShortDescription = () => {
  if (postData.value.short_content.length > 200) {
    shortDescriptionError.value = 'Краткое описание не должно превышать 200 символов'
    return false
  } else if (postData.value.short_content.length < 20) {
    shortDescriptionError.value = 'Краткое описание должно содержать минимум 20 символов'
    return false
  } else {
    shortDescriptionError.value = ''
    return true
  }
}

// Валидация полного описания
const validateContent = () => {
  if (postData.value.content.length > 5000) {
    contentError.value = 'Описание не должно превышать 5000 символов'
    return false
  } else if (postData.value.content.length < 50) {
    contentError.value = 'Описание должно содержать минимум 50 символов'
    return false
  } else {
    contentError.value = ''
    return true
  }
}

// Валидация дат
const validateDates = () => {
  if (!postData.value.start_date || !postData.value.end_date) {
    dateError.value = 'Даты начала и окончания обязательны'
    return false
  }

  const startDate = new Date(postData.value.start_date)
  const endDate = new Date(postData.value.end_date)
  const today = new Date()
  today.setHours(0, 0, 0, 0)

  if (startDate < today) {
    dateError.value = 'Дата начала не может быть в прошлом'
    return false
  }

  if (endDate < startDate) {
    dateError.value = 'Дата окончания не может быть раньше даты начала'
    return false
  }

  dateError.value = ''
  return true
}

// Валидация тегов
const validateTags = () => {
  if (selectedTags.value.length === 0) {
    tagsError.value = 'Добавьте хотя бы один тег'
    return false
  } else if (selectedTags.value.length > 4) {
    tagsError.value = 'Можно добавить не более 4 тегов'
    return false
  } else {
    tagsError.value = ''
    return true
  }
}

// Добавление тега
const addTag = () => {
  const tag = newTag.value.trim()

  if (!tag) return

  if (tag.length > 20) {
    tagsError.value = 'Тег не должен превышать 20 символов'
    return
  }

  if (selectedTags.value.length >= 4) {
    tagsError.value = 'Можно выбрать не более 4 тегов'
    return
  }

  if (!selectedTags.value.includes(tag)) {
    selectedTags.value.push(tag)
    newTag.value = ''

    // Добавляем новый тег в общий список, если его там нет
    if (!availableTags.value.includes(tag)) {
      availableTags.value.push(tag)
    }
  }

  validateTags()
}

const removeTag = (index) => {
  selectedTags.value.splice(index, 1)
  validateTags()
}

const selectTag = (tag) => {
  if (selectedTags.value.length >= 4) {
    tagsError.value = 'Можно выбрать не более 4 тегов'
    return
  }

  if (!selectedTags.value.includes(tag)) {
    selectedTags.value.push(tag)
    validateTags()
  }
}

const tagClasses = (index) => {
  const colors = [
    'bg-blue-100 text-blue-800',
    'bg-green-100 text-green-800',
    'bg-yellow-100 text-yellow-800',
    'bg-purple-100 text-purple-800'
  ]
  return colors[index % 4]
}

// Методы работы с изображением
const triggerFileInput = () => {
  imageInput.value?.click()
}

const handleImageUpload = (event) => {
  const file = event.target.files[0]
  if (!file) return

  if (!file.type.match('image.*')) {
    imageError.value = 'Пожалуйста, выберите изображение'
    return
  }

  const reader = new FileReader()
  reader.onload = (e) => {
    imagePreview.value = e.target.result
    postData.value.post_img = e.target.result
    imageError.value = ''
  }
  toast.success("Картинка загружена!")

  reader.readAsDataURL(file)
}

// Вспомогательные методы
const convertToTimestamp = (dateString, time = "00:00:00") => {
  if (!dateString || !/^\d{4}-\d{2}-\d{2}$/.test(dateString)) return null
  if (!/^\d{2}:\d{2}:\d{2}$/.test(time)) return null

  const [year, month, day] = dateString.split('-').map(Number)
  const [hours, minutes, seconds] = time.split(':').map(Number)

  return Date.UTC(year, month - 1, day, hours, minutes, seconds)
}


// Валидация всей формы
const validateForm = () => {
  const validations = [
    validateImage(),
    validateTitle(),
    validateShortDescription(),
    validateContent(),
    validateDates(),
    validateTags()
  ]

  return validations.every(valid => valid)
}

// Отправка формы
import { useToast } from "vue-toastification"
import {jwtDecode} from "jwt-decode";

const toast = useToast()

const submitForm = async () => {
  if (!validateForm()) {
    toast.error("Пожалуйста, исправьте ошибки в форме")
    return
  }

  try {
    isSubmitting.value = true

    const formData = {
      ...postData.value,
      start_date: convertToTimestamp(postData.value.start_date) / 1000,
      end_date: convertToTimestamp(postData.value.end_date) / 1000,
      tags: selectedTags.value
    }

    const response = await jwtApi.post(
        `${import.meta.env.VITE_BASE_URL}/posts/create/post`, formData)
    const decoded = jwtDecode(localStorage.getItem('authToken')
  )
    if (decoded['is_admin']) {
      toast.success("Новость успешно опубликована!")
    } else {
      toast.success("Новость успешно добавлена в черновики!")

    }
    router.push('/')

  } catch (error) {
    if (axios.isAxiosError(error)) {
      const errorMessage = error.response?.data?.message ||
          'Произошла ошибка при создании новости'
      toast.error(errorMessage)
    } else {
      console.error('Unknown error:', error)
      toast.error('Произошла неизвестная ошибка')
    }
  } finally {
    isSubmitting.value = false
  }
}

// Проверка авторизации
onBeforeMount(() => {
  if (!localStorage.getItem('authToken')) {
    router.push('/auth')
  }
})
</script>

<style>
/* Стили остаются без изменений */
.bg-pattern {
  background: linear-gradient(135deg, #f6f8ff 0%, #f0f4ff 100%);
  background-image: radial-gradient(at 20% 25%, rgba(59, 130, 246, 0.04) 0px, transparent 50%),
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