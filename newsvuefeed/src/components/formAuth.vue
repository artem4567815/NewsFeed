<template>
<div @click.stop="hideModal()" class="z-10 fixed inset-0 flex  items-center justify-center bg-black/50">
  <div @click.stop class="flex bg-white  rounded-xl w-11/12 sm:w-9/12 md:w-7/12 lg:w-6/12 xl:w-4/12 flex-col justify-center px-6 py-12 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-sm">
      <div class="text-3xl justify-self-center font-bold">EduFeed</div>
      <h2 class="mt-10 text-center text-2xl/9 font-bold tracking-tight text-gray-900">Войти в аккаунт</h2>
    </div>

    <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
      <form class="space-y-6" action="#" method="POST">
        <div>
          <label for="emailAuth" class="block text-sm/6 font-medium text-gray-900">Почта</label>
          <div class="mt-2">
            <input type="email" name="emailAuth" id="emailAuth" autocomplete="email" required class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6">
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
            <input type="password" name="passwordAuth" id="passwordAuth" autocomplete="current-password" required class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6">
          </div>
        </div>

        <div>
          <button type="submit" class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm/6 font-semibold text-white shadow-xs hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">Войти</button>
        </div>
      </form>

      <p class="mt-10 text-center text-sm/6 text-gray-500">
        Нет аккаунта?
        <button @click="ShowModalReg()" class="font-semibold text-indigo-600 hover:text-indigo-500">Зарегестрироваться</button>
      </p>
    </div>
  </div>
</div>

</template>
<script>
  import emitter from '@/main'
    export default {
      name: 'form-auth',
      methods: {
        hideModal() {
          emitter.emit('hideModal')
        },
        ShowModalReg() {
          emitter.emit('ShowModalReg')
        }
      }
    
    }
</script>
