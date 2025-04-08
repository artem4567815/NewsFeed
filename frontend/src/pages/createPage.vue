<template>
  <div class="min-h-screen bg-pattern">
    <div class="bg-blue-100/40 w-89/100 justify-self-center mt-5 backdrop-blur-sm rounded-2xl p-0 sm:p-3 text-center flex flex-col justify-center items-center shadow-sm  ">
      <div class="text-2xl my-3  text-center font-semibold">Edu<span class="text-blue-500">Feed</span></div>

      <h2 class="lg:text-[2.5rem]  text-[1.5rem] font-bold text-[#1F2937] mb-4 leading-tight">Создание новости</h2>
      <p class="text-lg sm:text-xl mb-5 text-gray-600">Расскажи всем о своём уникальном событии!</p>
    </div>

    <form @submit.prevent="submitForm" class="flex flex-col items-center  py-8">
      <!-- Основной контейнер -->
      <div class="bg-white rounded-2xl shadow-lg overflow-hidden w-90/100 max-w-450 transition-transform duration-300 ease-out">
        <div class="flex flex-col lg:flex-row  h-full">
          <!-- Блок загрузки изображения -->
          <div
              class="aspect-video w-full lg:max-w-180 relative overflow-hidden bg-gray-100 hover:bg-gray-200 transition-colors duration-200 flex items-center justify-center cursor-pointer "
              @click.stop="triggerFileInput"
          >
            <input ref="imageInput" type="file" accept="image/*" class="hidden" @change="handleImageUpload" />

            <div class="text-center p-6">
              <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-blue-100 mb-4">
                <Upload class="h-6 w-6 text-blue-600" />
              </div>
              <p class="text-lg font-medium text-gray-700 mb-1">Загрузите изображение</p>
              <p class="text-gray-500 mb-4">или</p>
              <blue-button
                  type="button"
                  @click.stop="$router.push('/Create/Cover')"
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
                  {{ new Date().toLocaleDateString() }}
                </span>
              </div>
            </div>

            <!-- Заголовок -->
            <div class="mb-6">
              <label for="NewsName" class="block text-sm font-medium text-gray-700 mb-1">Название новости</label>
              <input
                  v-model="postNew.title"
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
                  v-model="postNew.short_content"
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
                    :class="{
                    'bg-blue-100 text-blue-800': index % 4 === 0,
                    'bg-green-100 text-green-800': index % 4 === 1,
                    'bg-yellow-100 text-yellow-800': index % 4 === 2,
                    'bg-purple-100 text-purple-800': index % 4 === 3
                  }"
                >
                  {{ tag }}
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
                v-model="postNew.content"
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
                v-model="postNew.end_date"
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
          >
            Опубликовать новость
          </blue-button>
        </div>
      </div>
    </form>
  </div>
</template>

<script setup>
import { onBeforeMount } from 'vue'
import { useRouter } from 'vue-router'
import { CalendarDays, Upload } from 'lucide-vue-next'
import { ref } from 'vue'
import {jwtDecode} from 'jwt-decode'
import BlueButton from "@/components/UI/blueButton.vue";

const router = useRouter()

const imageInput = ref(null)
const newTag = ref('')
const tags = ref(['Технологии', 'Образование', 'Школа'])

const postNew = ref({
  title: "",
  type: "news",
  content: "",
  short_content: "",
  start_date: "",
  end_date: "",
  post_img: null,
  post_img_detail: ""
})

const addTag = () => {
  if (newTag.value.trim() && !tags.value.includes(newTag.value.trim())) {
    tags.value.push(newTag.value.trim())
    newTag.value = ''
  }
}

const triggerFileInput = () => {
  if (imageInput.value) {
    imageInput.value.click()
  }
}

const handleImageUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    const reader = new FileReader()
    reader.readAsDataURL(file)
    reader.onload = () => {
      postNew.value.post_img = reader.result
    }
  }
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
  const response = await fetch('http://localhost:5000/auth/refresh', {
    method: 'POST',
    credentials: 'include'
  })
  if (response.status === 401) {
    return "Not Auth"
  }
  const data = await response.json()
  localStorage.setItem('access', data.access)
}

const submitForm = async () => {
  try {
    postNew.value.start_date = 795683520000
    postNew.value.end_date = convertToTimestamp(postNew.value.end_date)

    const response = await fetch('http://127.0.0.1:8080/admin/create/post', {
      method: 'POST',
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${localStorage.getItem("authToken")}`,
      },
      body: JSON.stringify(postNew.value)
    })

    if (response.status === 401) {
      let ans = await refreshToken()
      if (ans === "Not Auth") {
        return "User not auth"
      }
      return submitForm()
    }

    const data = await response.json()
    console.log('Post created:', data)
    router.push('/Create')
  } catch (error) {
    console.error('Error creating post:', error)
  }
}

// Аналог beforeMount
onBeforeMount(() => {
  const token = localStorage.getItem('authToken')
  if (!token) {
    router.push('/auth')
    return
  }

  try {
    const decoded = jwtDecode(token)
    if (!decoded['is_admin']) {
      router.push('/auth')
    }
  } catch (e) {
    console.error("Token decoding failed", e)
    router.push('/auth')
  }
})
</script>


<style>
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