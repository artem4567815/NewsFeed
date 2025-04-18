<template>
  <div class="-z-10 fixed mt-10 inset-0 flex items-center justify-center bg-black/50">
    <div class="flex bg-white w-11/12 sm:w-9/12 md:w-7/12 lg:w-6/12 xl:w-4/12 rounded-xl flex-col justify-center px-6 py-12 lg:px-8">
      <div class="sm:mx-auto sm:w-full sm:max-w-sm">


        <div class="text-3xl   justify-self-center hover:cursor-pointer font-semibold">Edu<span class="text-blue-500">Feed</span></div>
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
              <input v-model="register.name" type="text" name="name" id="name" required class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6">
            </div>
          </div>

          <div>
            <label for="surname" class="block text-sm/6 font-medium text-gray-900">Фамилия</label>
            <div class="mt-1">
              <input v-model="register.surname" type="text" name="surname" id="surname" required class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6">
            </div>
          </div>

          <div>
            <label for="school" class="block text-sm/6 font-medium text-gray-900">Школа</label>
            <div class="mt-1">
              <input v-model="register.school" type="text" name="school" id="school" required class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6">
            </div>
          </div>

          <div>
            <label for="building" class="block text-sm/6 font-medium text-gray-900">Корпус</label>
            <div class="mt-1">
              <input v-model="register.building" type="text" name="building" id="building" required class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6">
            </div>
          </div>

          <div>
            <label for="login" class="block text-sm/6 font-medium text-gray-900">Логин</label>
            <div class="mt-1">
              <input v-model="register.login" type="text" name="login" id="login" required class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6">
            </div>
          </div>

<!--          <div>-->
<!--            <label for="email" class="block text-sm/6 font-medium text-gray-900">Почта</label>-->
<!--            <div class="mt-1">-->
<!--              <input v-model="register.email" type="email" name="email" id="email" autocomplete="email" required-->
<!--                     class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6">-->
<!--            </div>-->
<!--          </div>-->

          <div>
            <label for="password" class="block text-sm/6 font-medium text-gray-900">Пароль</label>
            <div class="mt-1">
              <input v-model="register.password" type="password" name="password" id="password" autocomplete="current-password" required class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6">
            </div>
          </div>

          <div>
            <button type="submit" :disabled="isLoading" class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm/6 font-semibold text-white shadow-xs hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 disabled:opacity-50 disabled:cursor-not-allowed">
              <span v-if="!isLoading">Зарегистрироваться</span>
              <span v-else>Отправка...</span>
            </button>
          </div>
        </form>

        <p class="mt-10 text-center text-sm/6 text-gray-500">
          Есть аккаунт?
          <button @click="$router.push('/auth')" class="font-semibold text-indigo-600 hover:text-indigo-500">Войти</button>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      register: {
        name: "",
        surname: "",
        school: "",
        building: "",
        login: "",
        // email: "",
        password: ""
      },
      isLoading: false,
      errorMessage: ""
    }
  },
  name: 'form-reg',
  methods: {
    async submitForm() {
      this.isLoading = true;
      this.errorMessage = "";

      try {
        const response = await fetch(`${import.meta.env.VITE_BASE_URL}/auth/register/client`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.register)
        });

        const data = await response.json();
        console.log(data)
        if (!response.ok) {
          if (data.message) {
            throw new Error(data.message);
          } else {
            throw new Error(`Ошибка регистрации: ${response.status}`);
          }
        }

        console.log('Registration successful:', data);

        const auth = {
          login: this.register.login,
          password: this.register.password,
        }
        try {
          const response = await fetch(`${import.meta.env.VITE_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify(auth)
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

          if (data.access_token) {
            localStorage.setItem('authToken', data.access_token);
          }
          console.log(localStorage.getItem('authToken'));


          // this.hideModal();

          // this.$store.commit('setAuth', true);

          // или this.$router.push('/dashboard');

        } catch (error) {
          console.error('Login error:', error);
          this.errorMessage = error.message || 'Произошла ошибка при входе. Пожалуйста, проверьте данные и попробуйте еще раз.';
        } finally {
          this.isLoading = false;
        }
        this.$router.push('/');

      } catch (error) {
        console.error('Registration error:', error);
        this.errorMessage = error.message || 'Произошла ошибка при регистрации. Пожалуйста, попробуйте еще раз.';
      } finally {
        this.isLoading = false;
      }
    }
  }
}
</script>