<template>
  <div>
    <h1 class="text-2xl font-bold mb-6">Профиль</h1>
    <div class="flex flex-col lg:flex-row gap-6">
      <div class="bg-white p-6 rounded-lg shadow w-full lg:w-1/3 text-center">
        <div v-if="profilePage" class="flex w-full justify-center items-center mb-2">
          <img
              v-if="profilePage.avatar_url"
              :src="profilePage.avatar_url"
              class="w-16 h-16 rounded-full object-cover"
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
              <input v-model="profilePage.login" class="w-full border p-2 rounded focus:outline-none focus:ring focus:ring-blue-200" placeholder="Login" />
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
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useToast } from "vue-toastification"
import jwtApi from "@/api/jwtApi.js"
import router from "@/router/router.js"

const toast = useToast()
const profileTab = ref('personal')
const profilePage = ref({
  name: '',
  surname: '',
  login: '',
  avatar_url: ''
})

const avatarInput = ref(null)
const uploadStatus = ref(null)
const isUploading = ref(false)
const isSaving = ref(false)
const saveStatus = ref(null)

onMounted(async () => {
  try {
    const response = await jwtApi.get(`${import.meta.env.VITE_BASE_URL}/user/profile`)
    profilePage.value = response.data
  } catch (error) {
    console.error('Ошибка при загрузке профиля:', error)
    toast.error('Не удалось загрузить данные профиля')
  }
})

const handleAvatarChange = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  if (file.size > 5 * 1024 * 1024) {
    uploadStatus.value = { success: false, message: 'Файл слишком большой (максимум 5MB)' }
    return
  }

  if (!file.type.match('image.*')) {
    uploadStatus.value = { success: false, message: 'Пожалуйста, выберите файл изображения' }
    return
  }

  isUploading.value = true
  uploadStatus.value = null

  try {
    const base64DataUrl = await new Promise((resolve, reject) => {
      const reader = new FileReader()
      reader.onload = () => resolve(reader.result)
      reader.onerror = error => reject(error)
      reader.readAsDataURL(file)
    })
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
    )

    profilePage.value.avatar_url = base64DataUrl
    uploadStatus.value = { success: true, message: 'Аватар успешно обновлён' }

  } catch (error) {
    console.error('Ошибка при загрузке аватара:', error)
    uploadStatus.value = {
      success: false,
      message: error.response?.data?.message || 'Ошибка при загрузке аватара'
    }
  } finally {
    isUploading.value = false
    setTimeout(() => { uploadStatus.value = null }, 3000)
  }
}

const saveProfileChanges = async () => {
  if (!profilePage.value.name || !profilePage.value.surname || !profilePage.value.login) {
    saveStatus.value = { success: false, message: 'Все поля обязательны для заполнения' }
    return
  }

  isSaving.value = true
  saveStatus.value = null

  try {
    const response = await jwtApi.patch(
        `${import.meta.env.VITE_BASE_URL}/user/profile`,
        {
          name: profilePage.value.name,
          surname: profilePage.value.surname,
          login: profilePage.value.login
        },
        {
          headers: {
            'Content-Type': 'application/json'
          }
        }
    )
    saveStatus.value = { success: true, message: 'Данные успешно сохранены' }

  } catch (error) {
    console.error('Ошибка при сохранении:', error)
    saveStatus.value = {
      success: false,
      message: error.response?.data?.message || 'Ошибка при сохранении данных'
    }
  } finally {
    isSaving.value = false
    setTimeout(() => { saveStatus.value = null }, 3000)
  }
}

const exit = () => {
  localStorage.clear()
  window.location.reload()
}

defineExpose({
  profilePage
})
</script> 