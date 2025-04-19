<template>
  <div class="-z-10 fixed inset-0 flex items-center justify-center bg-black/50">
    <div class="flex bg-white w-11/12 sm:w-9/12 md:w-7/12 lg:w-6/12 xl:w-4/12 rounded-xl flex-col justify-center px-6 py-12 lg:px-8">
      <div class="sm:mx-auto sm:w-full sm:max-w-sm">
        <div class="text-3xl justify-self-center hover:cursor-pointer font-semibold">Edu<span class="text-blue-500">Feed</span></div>
        <h2 class="mt-10 text-center text-2xl/9 font-bold tracking-tight text-gray-900">Регистрация</h2>
      </div>

      <div v-if="errorMessage" class="mt-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
        {{ errorMessage }}
      </div>

      <div class="mt-6 sm:mx-auto sm:w-full sm:max-w-sm">
        <form @submit.prevent="submitForm" class="space-y-3">
          <div>
            <label for="name" class="block text-sm/6 font-medium text-gray-900">Имя</label>
            <div class="mt-1">
              <input
                  v-model="register.name"
                  @input="validateName"
                  type="text"
                  name="name"
                  id="name"
                  required
                  class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
                  :class="{'outline-red-500': nameError}"
              >
              <div v-if="nameError" class="text-red-500 text-sm mt-1">{{ nameError }}</div>
            </div>
          </div>

          <div>
            <label for="surname" class="block text-sm/6 font-medium text-gray-900">Фамилия</label>
            <div class="mt-1">
              <input
                  v-model="register.surname"
                  @input="validateSurname"
                  type="text"
                  name="surname"
                  id="surname"
                  required
                  class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
                  :class="{'outline-red-500': surnameError}"
              >
              <div v-if="surnameError" class="text-red-500 text-sm mt-1">{{ surnameError }}</div>
            </div>
          </div>

          <div>
            <label for="school" class="block text-sm/6 font-medium text-gray-900">Школа</label>
            <div class="mt-1">
              <input
                  v-model="register.school"
                  @input="validateSchool"
                  type="text"
                  name="school"
                  id="school"
                  required
                  class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
                  :class="{'outline-red-500': schoolError}"
              >
              <div v-if="schoolError" class="text-red-500 text-sm mt-1">{{ schoolError }}</div>
            </div>
          </div>

          <div>
            <label for="building" class="block text-sm/6 font-medium text-gray-900">Корпус</label>
            <div class="mt-1">
              <input
                  v-model="register.building"
                  @input="validateBuilding"
                  type="text"
                  name="building"
                  id="building"
                  required
                  class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
                  :class="{'outline-red-500': buildingError}"
              >
              <div v-if="buildingError" class="text-red-500 text-sm mt-1">{{ buildingError }}</div>
            </div>
          </div>

          <div>
            <label for="login" class="block text-sm/6 font-medium text-gray-900">Логин</label>
            <div class="mt-1">
              <input
                  v-model="register.login"
                  @input="validateLogin"
                  type="text"
                  name="login"
                  id="login"
                  required
                  class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
                  :class="{'outline-red-500': loginError}"
              >
              <div v-if="loginError" class="text-red-500 text-sm mt-1">{{ loginError }}</div>
            </div>
          </div>

          <div>
            <label for="password" class="block text-sm/6 font-medium text-gray-900">Пароль</label>
            <div class="mt-1">
              <input
                  v-model="register.password"
                  @input="validatePassword"
                  type="password"
                  name="password"
                  id="password"
                  autocomplete="current-password"
                  required
                  class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
                  :class="{'outline-red-500': passwordError}"
              >
              <div v-if="passwordError" class="text-red-500 text-sm mt-1">{{ passwordError }}</div>
              <div class="text-gray-500 text-xs mt-1">
                Пароль должен содержать минимум 8 символов, включая цифры, буквы и специальные символы (!@#$% и т.д.)
              </div>
            </div>
          </div>

          <div>
            <button
                type="submit"
                :disabled="isLoading || hasErrors"
                class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm/6 font-semibold text-white shadow-xs hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span v-if="!isLoading">Зарегистрироваться</span>
              <span v-else>Отправка...</span>
            </button>
          </div>
        </form>

        <p class="mt-10 text-center text-sm/6 text-gray-500">
          Есть аккаунт?
          <button @click="router.push('/auth')" class="font-semibold text-indigo-600 hover:text-indigo-500">Войти</button>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const register = ref({
  name: "",
  surname: "",
  school: "",
  building: "",
  login: "",
  password: ""
})

const isLoading = ref(false)
const errorMessage = ref("")

// Ошибки валидации
const nameError = ref("")
const surnameError = ref("")
const schoolError = ref("")
const buildingError = ref("")
const loginError = ref("")
const passwordError = ref("")

const hasErrors = computed(() => {
  return !!(
      nameError.value ||
      surnameError.value ||
      schoolError.value ||
      buildingError.value ||
      loginError.value ||
      passwordError.value
  )
})

// Валидация имени
const validateName = () => {
  if (!register.value.name.trim()) {
    nameError.value = "Имя обязательно"
    return false
  }
  if (register.value.name.length < 2) {
    nameError.value = "Имя должно содержать минимум 2 символа"
    return false
  }
  if (register.value.name.length > 50) {
    nameError.value = "Имя не должно превышать 50 символов"
    return false
  }
  if (!/^[a-zA-Zа-яА-ЯёЁ\s-]+$/.test(register.value.name)) {
    nameError.value = "Имя может содержать только буквы, пробелы и дефисы"
    return false
  }
  nameError.value = ""
  return true
}

// Валидация фамилии
const validateSurname = () => {
  if (!register.value.surname.trim()) {
    surnameError.value = "Фамилия обязательна"
    return false
  }
  if (register.value.surname.length < 2) {
    surnameError.value = "Фамилия должна содержать минимум 2 символа"
    return false
  }
  if (register.value.surname.length > 50) {
    surnameError.value = "Фамилия не должна превышать 50 символов"
    return false
  }
  if (!/^[a-zA-Zа-яА-ЯёЁ\s-]+$/.test(register.value.surname)) {
    surnameError.value = "Фамилия может содержать только буквы, пробелы и дефисы"
    return false
  }
  surnameError.value = ""
  return true
}

// Валидация школы
const validateSchool = () => {
  if (!register.value.school.trim()) {
    schoolError.value = "Школа обязательна"
    return false
  }
  if (register.value.school.length < 2) {
    schoolError.value = "Название школы должно содержать минимум 2 символа"
    return false
  }
  if (register.value.school.length > 100) {
    schoolError.value = "Название школы не должно превышать 100 символов"
    return false
  }
  schoolError.value = ""
  return true
}

// Валидация корпуса
const validateBuilding = () => {
  if (!register.value.building.trim()) {
    buildingError.value = "Корпус обязателен"
    return false
  }
  if (register.value.building.length > 10) {
    buildingError.value = "Название корпуса не должно превышать 10 символов"
    return false
  }
  buildingError.value = ""
  return true
}

// Валидация логина
const validateLogin = () => {
  if (!register.value.login.trim()) {
    loginError.value = "Логин обязателен"
    return false
  }
  if (register.value.login.length < 4) {
    loginError.value = "Логин должен содержать минимум 4 символа"
    return false
  }
  if (register.value.login.length > 20) {
    loginError.value = "Логин не должен превышать 20 символов"
    return false
  }
  if (!/^[a-zA-Z0-9_]+$/.test(register.value.login)) {
    loginError.value = "Логин может содержать только буквы, цифры и подчеркивания"
    return false
  }
  loginError.value = ""
  return true
}

// Валидация пароля (с проверкой на специальные символы)
const validatePassword = () => {
  if (!register.value.password) {
    passwordError.value = "Пароль обязателен"
    return false
  }
  if (register.value.password.length < 8) {
    passwordError.value = "Пароль должен содержать минимум 8 символов"
    return false
  }
  if (!/[0-9]/.test(register.value.password)) {
    passwordError.value = "Пароль должен содержать хотя бы одну цифру"
    return false
  }
  if (!/[A-Z]/.test(register.value.password)) {
    passwordError.value = "Пароль должен содержать хотя бы одну заглавную букву"
    return false
  }
  if (!/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(register.value.password)) {
    passwordError.value = "Пароль должен содержать хотя бы один специальный символ (!@#$% и т.д.)"
    return false
  }
  passwordError.value = ""
  return true
}

// Общая валидация формы
const validateForm = () => {
  const validations = [
    validateName(),
    validateSurname(),
    validateSchool(),
    validateBuilding(),
    validateLogin(),
    validatePassword()
  ]
  return validations.every(valid => valid)
}

const submitForm = async () => {
  if (!validateForm()) return;

  isLoading.value = true;
  errorMessage.value = "";

  try {
    // 1. Регистрация
    const registerResponse = await axios.post(
        `${import.meta.env.VITE_BASE_URL}/auth/register/admin`,
        register.value,
        {
          headers: {
            'Content-Type': 'application/json',
          },
          withCredentials: true
        }
    );


    // 2. Автоматический вход после регистрации
    const loginResponse = await axios.post(
        `${import.meta.env.VITE_BASE_URL}/auth/login`,
        {
          login: register.value.login,
          password: register.value.password
        },
        {
          headers: {
            'Content-Type': 'application/json',
          },
          withCredentials: true
        }
    );


    // 3. Сохранение токена
    if (loginResponse.data.access_token) {
      localStorage.setItem('authToken', loginResponse.data.access_token);
      await router.push('/');
      window.location.reload(); // или перенаправление на страницу входа

    }

  } catch (error) {
    if (axios.isAxiosError(error)) {
      // Безопасный вывод ошибки Axios
      errorMessage.value = error.response?.data?.message ||
          error.response?.data?.error ||
          `Ошибка ${error.response?.status || 'соединения'}`;

      console.error('Ошибка запроса:', {
        url: error.config?.url,
        status: error.response?.status,
        message: error.response?.data?.message || error.response?.data?.error,
      });
    } else {
      // Обработка не-Axios ошибок
      errorMessage.value = 'Неизвестная ошибка';
      console.error('Неожиданная ошибка:', error instanceof Error ? error.message : String(error));
    }
  } finally {
    isLoading.value = false;
  }
};
</script>