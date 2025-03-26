<template>
  <div @click.stop="hideModal()" class="z-10 fixed inset-0 flex items-center justify-center bg-black/50">
    <div @click.stop class="flex bg-white rounded-xl w-11/12 sm:w-9/12 md:w-7/12 lg:w-6/12 xl:w-4/12 flex-col justify-center px-6 py-12 lg:px-8">
      <div class="sm:mx-auto sm:w-full sm:max-w-sm">
        <div class="text-3xl justify-self-center font-bold">EduFeed</div>
        <h2 class="mt-10 text-center text-2xl/9 font-bold tracking-tight text-gray-900">Войти в аккаунт</h2>
      </div>

      <!-- Блок для отображения ошибок -->
      <div v-if="errorMessage" class="mt-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
        {{ errorMessage }}
      </div>

      <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
        <form @submit.prevent="submitForm" class="space-y-6">
          <div>
            <label for="emailAuth" class="block text-sm/6 font-medium text-gray-900">Почта</label>
            <div class="mt-2">
              <input type="email" v-model="auth.email" name="emailAuth" id="emailAuth" autocomplete="email" required class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6">
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
              <input type="password" v-model="auth.password" name="passwordAuth" id="passwordAuth" autocomplete="current-password" required class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6">
            </div>
          </div>

          <div>
            <button type="submit" :disabled="isLoading" class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm/6 font-semibold text-white shadow-xs hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 disabled:opacity-50 disabled:cursor-not-allowed">
              <span v-if="!isLoading">Войти</span>
              <span v-else>Вход...</span>
            </button>
          </div>
        </form>

        <p class="mt-10 text-center text-sm/6 text-gray-500">
          Нет аккаунта?
          <button @click="ShowModalReg()" class="font-semibold text-indigo-600 hover:text-indigo-500">Зарегистрироваться</button>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import emitter from '@/main'

export default {
  data() {
    return {
      auth: {
        email: "",
        password: ""
      },
      isLoading: false,
      errorMessage: ""
    }
  },
  name: 'form-auth',
  methods: {
    hideModal() {
      emitter.emit('hideModal')
    },
    ShowModalReg() {
      emitter.emit('ShowModalReg')
    },
    async submitForm() {
      this.isLoading = true;
      this.errorMessage = "";

      try {
        const response = await fetch('http://127.0.0.1:8080/auth/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.auth)
        });

        const data = await response.json();

        if (!response.ok) {
          if (data.message) {
            throw new Error(data.message);
          } else {
            throw new Error(`Ошибка авторизации: ${response.status}`);
          }
        }

        console.log('Login successful:', data);

        // if (data.token) {
        //   localStorage.setItem('authToken', data.token);
        // }

        // this.hideModal();

        // this.$store.commit('setAuth', true);

        // или this.$router.push('/dashboard');

      } catch (error) {
        console.error('Login error:', error);
        this.errorMessage = error.message || 'Произошла ошибка при входе. Пожалуйста, проверьте данные и попробуйте еще раз.';
      } finally {
        this.isLoading = false;
      }
    }
  }
}
</script>