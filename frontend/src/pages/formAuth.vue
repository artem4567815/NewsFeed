<template>
  <div @click.stop="hideModal" class="-z-10 fixed inset-0 flex items-center justify-center bg-black/50">
    <div @click.stop class="flex bg-white rounded-xl w-11/12 sm:w-9/12 md:w-7/12 lg:w-6/12 xl:w-4/12 flex-col justify-center px-6 py-12 lg:px-8">
      <div class="sm:mx-auto sm:w-full sm:max-w-sm">
        <div class="text-3xl justify-self-center hover:cursor-pointer font-semibold">Edu<span class="text-blue-500">Feed</span></div>
        <h2 class="mt-10 text-center text-2xl/9 font-bold tracking-tight text-gray-900">Войти в аккаунт</h2>
      </div>

      <!-- Блок для отображения ошибок -->
      <div v-if="errorMessage" class="mt-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
        {{ errorMessage }}
      </div>

      <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
        <form @submit.prevent="submitForm" class="space-y-6">
          <div>
            <label for="emailAuth" class="block text-sm/6 font-medium text-gray-900">Логин</label>
            <div class="mt-2">
              <input
                  v-model="auth.login"
                  @input="validateLogin"
                  type="text"
                  name="emailAuth"
                  id="emailAuth"
                  required
                  class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
                  :class="{'outline-red-500': loginError}"
              >
              <div v-if="loginError" class="text-red-500 text-sm mt-1">{{ loginError }}</div>
            </div>
          </div>

          <div>
            <div class="flex items-center justify-between">
              <label for="passwordAuth" class="block text-sm/6 font-medium text-gray-900">Пароль</label>
              <div class="text-sm">
                <a href="#" class="font-semibold text-indigo-600 hover:text-indigo-500">Забыли пароль?</a>
              </div>
            </div>
            <div class="mt-2">
              <input
                  v-model="auth.password"
                  @input="validatePassword"
                  type="password"
                  name="passwordAuth"
                  id="passwordAuth"
                  autocomplete="current-password"
                  required
                  class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
                  :class="{'outline-red-500': passwordError}"
              >
              <div v-if="passwordError" class="text-red-500 text-sm mt-1">{{ passwordError }}</div>
            </div>
          </div>

          <div>
            <button
                type="submit"
                :disabled="isLoading || hasErrors"
                class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm/6 font-semibold text-white shadow-xs hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span v-if="!isLoading">Войти</span>
              <span v-else>Вход...</span>
            </button>
          </div>
        </form>

        <p class="mt-10 text-center text-sm/6 text-gray-500">
          Нет аккаунта?
          <button @click="router.push('/registration')" class="font-semibold text-indigo-600 hover:text-indigo-500">Зарегистрироваться</button>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref, computed} from 'vue'
import {useRouter} from 'vue-router'
import axios from 'axios'

const router = useRouter()

const auth = ref({
  login: "",
  password: ""
})

const isLoading = ref(false)
const errorMessage = ref("")

// Ошибки валидации
const loginError = ref("")
const passwordError = ref("")

const hasErrors = computed(() => {
  return !!(
      loginError.value ||
      passwordError.value
  )
})

// Валидация логина
const validateLogin = () => {
  const login = auth.value.login.trim()
  if (!login) {
    loginError.value = "Логин обязателен"
    return false
  }
  if (login.length < 4) {
    loginError.value = "Логин должен содержать минимум 4 символа"
    return false
  }
  loginError.value = ""
  return true
}

// Валидация пароля
const validatePassword = () => {
  const password = auth.value.password
  if (!password) {
    passwordError.value = "Пароль обязателен"
    return false
  }
  if (password.length < 6) {
    passwordError.value = "Пароль должен содержать минимум 6 символов"
    return false
  }
  passwordError.value = ""
  return true
}

// Общая валидация формы
const validateForm = () => {
  validateLogin()
  validatePassword()
  return !hasErrors.value
}

const hideModal = () => {
  // Логика закрытия модального окна
}

const submitForm = async () => {
  if (!validateForm()) return

  isLoading.value = true
  errorMessage.value = ""

  try {
    const response = await axios.post(
        `${import.meta.env.VITE_BASE_URL}/auth/login`,
        {
          login: auth.value.login,
          password: auth.value.password
        },
        {
          headers: {
            'Content-Type': 'application/json',
          },
          withCredentials: true
        }
    )

    if (response.data?.access_token) {
      localStorage.setItem('authToken', response.data.access_token)
      await router.push('/')
    } else {
      throw new Error('Не получили токен авторизации')
    }

  } catch (error) {
    if (axios.isAxiosError(error)) {
      const serverMessage = error.response?.data?.message ||
          error.response?.data?.error

      if (error.response?.status === 401) {
        errorMessage.value = "Неверный логин или пароль"
      } else {
        errorMessage.value = serverMessage ||
            `Ошибка сервера (${error.response?.status || 'нет соединения'})`
      }

      console.error('Ошибка авторизации:', {
        status: error.response?.status,
        message: serverMessage,
        url: error.config?.url
      })
    } else {
      errorMessage.value = "Произошла непредвиденная ошибка"
      console.error('Неожиданная ошибка:', error instanceof Error ? error.message : String(error))
    }
  } finally {
    isLoading.value = false
  }
}
</script>