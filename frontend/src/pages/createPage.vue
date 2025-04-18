<template>
  <div class="min-h-screen bg-pattern">
    <div class="bg-blue-100/40 w-89/100 justify-self-center mt-5 backdrop-blur-sm rounded-2xl p-0 sm:p-3 text-center flex flex-col justify-center items-center shadow-sm">
      <div class="text-2xl my-3 text-center font-semibold">Edu<span class="text-blue-500">Feed</span></div>
      <h2 class="lg:text-[2.5rem] text-[1.5rem] font-bold text-[#1F2937] mb-4 leading-tight">Создание новости</h2>
      <p class="text-lg sm:text-xl mb-5 text-gray-600">Расскажи всем о своём уникальном событии!</p>
    </div>

    <form @submit.prevent="submitForm" class="flex flex-col items-center py-8">
      <div class="bg-white rounded-2xl shadow-lg overflow-hidden w-90/100 max-w-450 transition-transform duration-300 ease-out">
        <div class="flex flex-col lg:flex-row h-full">
          <!-- Блок загрузки изображения -->
          <div
              class="aspect-video w-full lg:max-w-180 relative overflow-hidden bg-gray-100 hover:bg-gray-200 transition-colors duration-200 flex items-center justify-center cursor-pointer"
              @click.stop="triggerFileInput"
          >
            <input ref="imageInput" type="file" accept="image/*" class="hidden" @change="handleImageUpload" />

            <!-- Отображение превью или дефолтного контента -->
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

          <!-- Форма ввода -->
          <div class="flex-1 p-6 lg:min-w-120 flex flex-col">
            <!-- Метаданные -->
            <div class="mb-6">
              <div class="flex items-center space-x-4 mb-4">
                <span class="flex items-center text-sm font-medium text-gray-600">
                  <CalendarDays class="w-4 h-4 mr-1.5" />
                  {{ currentDate }}
                </span>
              </div>
            </div>

            <!-- Заголовок -->
            <div class="mb-6">
              <label for="NewsName" class="block text-sm font-medium text-gray-700 mb-1">Название новости</label>
              <input
                  v-model="postData.title"
                  type="text"
                  id="NewsName"
                  required
                  class="block w-full px-4 py-3 text-xl font-bold text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="Введите заголовок новости"
              >
            </div>

            <!-- Краткое описание -->
            <div class="mb-6">
              <label for="shortDesc" class="block text-sm font-medium text-gray-700 mb-1">Краткое описание</label>
              <textarea
                  v-model="postData.short_content"
                  id="shortDesc"
                  required
                  rows="3"
                  class="block w-full px-4 py-3 text-base text-gray-700 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="Краткое описание новости"
              ></textarea>
            </div>

            <!-- Теги -->
            <div class="mb-6">
              <label class="block text-sm font-medium text-gray-700 mb-2">Теги</label>
              <div class="flex flex-wrap gap-2">
                <span
                    v-for="(tag, index) in tags"
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
                <input
                    type="text"
                    v-model="newTag"
                    @keydown.enter.prevent="addTag"
                    class="flex-1 min-w-[100px] px-3 py-1 text-sm border-0 focus:ring-0"
                    placeholder="Добавить тег"
                >
              </div>
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
                id="Desc"
                required
                rows="5"
                class="block w-full px-4 py-3 text-base text-gray-700 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500"
                placeholder="Полное описание новости"
            ></textarea>
          </div>

          <!-- Дата окончания -->
          <div class="mb-6">
            <label for="time" class="block text-sm font-medium text-gray-700 mb-1">Дата окончания</label>
            <input
                v-model="postData.end_date"
                type="date"
                id="time"
                required
                class="block w-full px-4 py-3 text-base text-gray-700 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500"
            >
          </div>
        </div>

        <!-- Кнопка отправки -->
        <div class="p-6 border-t border-gray-200 flex justify-center lg:justify-end">
          <blue-button
              type="submit"
              :disabled="isSubmitting"
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
import BlueButton from "@/components/UI/blueButton.vue"

const router = useRouter()

// Refs
const imageInput = ref(null)
const newTag = ref('')
const tags = ref(['Технологии', 'Образование', 'Школа'])
const imagePreview = ref(null)
const isSubmitting = ref(false)

// Post data
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

// Methods
const addTag = () => {
  if (newTag.value.trim() && !tags.value.includes(newTag.value.trim())) {
    tags.value.push(newTag.value.trim())
    newTag.value = ''
  }
}

const removeTag = (index) => {
  tags.value.splice(index, 1)
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

const triggerFileInput = () => {
  imageInput.value?.click()
}

const handleImageUpload = (event) => {
  const file = event.target.files[0]
  if (!file) return

  // Проверка типа файла
  if (!file.type.match('image.*')) {
    alert('Пожалуйста, выберите изображение')
    return
  }

  // Создание превью
  const reader = new FileReader()
  reader.onload = (e) => {
    imagePreview.value = e.target.result
    postData.value.post_img = e.target.result
  }
  reader.readAsDataURL(file)
}

const convertToTimestamp = (dateString, time = "00:00:00") => {
  if (!dateString) return null
  const [year, month, day] = dateString.split('-')
  const [hours, minutes, seconds] = time.split(':')

  const date = new Date(Date.UTC(
      parseInt(year),
      parseInt(month) - 1,
      parseInt(day),
      parseInt(hours),
      parseInt(minutes),
      parseInt(seconds)
  ))

  return date.getTime()
}

const refreshToken = async () => {
  try {
    const response = await fetch('http://localhost:5000/auth/refresh', {
      method: 'POST',
      credentials: 'include'
    })

    if (response.status === 401) {
      return "Not Auth"
    }

    const data = await response.json()
    localStorage.setItem('access', data.access)
    return data
  } catch (error) {
    console.error('Error refreshing token:', error)
    throw error
  }
}

const submitForm = async () => {
  try {
    isSubmitting.value = true

    // Подготовка данных
    const formData = {
      ...postData.value,
      start_date: 795683520000, // Фиксированная дата начала
      end_date: convertToTimestamp(postData.value.end_date),
      tags: tags.value
    }

    const response = await fetch(`${import.meta.env.VITE_BASE_URL}/posts/create/post`, {
      method: 'POST',
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${localStorage.getItem("authToken")}`,
      },
      body: JSON.stringify(formData)
    })

    if (response.status === 401) {
      const refreshResult = await refreshToken()
      if (refreshResult === "Not Auth") {
        router.push('/auth')
        return
      }
      return await submitForm() // Повторная попытка после обновления токена
    }

    if (!response.ok) {
      throw new Error(`Ошибка HTTP: ${response.status}`)
    }

    const data = await response.json()
    console.log('Post created:', data)
    router.push('/')
  } catch (error) {
    console.error('Error creating post:', error)
    alert('Произошла ошибка при создании новости')
  } finally {
    isSubmitting.value = false
  }
}

// Хук жизненного цикла
onBeforeMount(() => {
  const token = localStorage.getItem('authToken')
  if (!token) {
    router.push('/auth')
  }
})
</script>

<style>
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