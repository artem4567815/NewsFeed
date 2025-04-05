<template class="">
  <header class="py-2 px-7 border-b-2 bg-white border-gray-200 flex items-center justify-between gap-3">
    <div class="flex items-center whitespace-nowrap">
      <div @click="$router.push('/')" class="text-2xl mr-15 hover:cursor-pointer font-semibold">EduFeed</div>
      <div class="hidden md:flex gap-3 mr-5">
        <div class="mr-5">Выбор школы</div>
        <div>Поиск по дате</div>
      </div>
    </div>

    <div class="flex justify-center items-center">
      <button v-show="!token || token === 'undefined' " @click="$router.push('/auth')" class="bg hover:cursor-pointer bg-blue-500 ring-4 hover:ring-blue-700/30 hover:bg-blue-600 transition ease-in-out rounded-2xl text-white px-3 py-2 mr-5"  >Вход</button>
      <button v-show="$route.path !== '/profile' && token && token !== 'undefined'" @click="$router.push('/profile')" class="hover:cursor-pointer bg-blue-500 ring-4 hover:ring-blue-700/30 hover:bg-blue-600 transition ease-in-out rounded-2xl text-white px-3 py-2 mr-5" >Профиль</button>
      <button @click="$router.push('/Profile/Create')" v-show="$route.path === '/profile'" class="hover:cursor-pointer bg-blue-500 ring-4 hover:ring-blue-700/30 hover:bg-blue-600 transition ease-in-out rounded-2xl text-white px-3 py-2 mr-5" >Создать пост</button>


      <div class="mb-0 flex items-center ">
        <div class="hover:cursor-pointer bg-gray-200 ring-4 ring-black/0 hover:bg-gray-300 hover:ring-gray-200  transition ease-in-out rounded-2xl p-3 mr-12">
          <Settings/>
        </div>

        <div class="hidden md-4 sm:flex w-full max-w-sm bg-gray-200 rounded-lg relative">
          <input type="text" placeholder="Найти новость..." class="w-full pl-10 pr-4 py-2 text-lg rounded-lg border border-gray-300"/>
          <span class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500">
            <Search />
          </span>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { Settings, Search } from 'lucide-vue-next';
</script>

<script>

export default {
  data() {
    return {
      authed: false,
      showModal: "",
      token: localStorage.getItem('authToken'),
    }
  },
  name: 'header-main'
}
</script>

<style lang="scss" scoped>

</style>