<template class="z-100">
  <header class="py-2 z-100 px-2 lg:px-7 border-b-2 bg-white border-gray-200 flex items-center justify-between gap-3">
    <div class="flex items-center whitespace-nowrap">
      <div @click="$router.push('/')" class="text-2xl   hover:cursor-pointer font-semibold">Edu<span class="text-blue-500">Feed</span></div>
      <div class="hidden ml-5 md:flex gap-3 mr-5">
        <div class="mr-5">Новости</div>
        <div class="mr-5">Стенгазеты</div>
        <div class="mr-5">Поиск команды</div>
      </div>
    </div>

    <div class="flex justify-center items-center">
      <blue-button v-show="!token || token === 'undefined' " @click="$router.push('/auth')" class="mr-5" >Вход</blue-button>
      <blue-button v-show="$route.path !== '/profile' && token && token !== 'undefined'" @click="$router.push('/profile')" class="mr-5">Профиль</blue-button>
      <blue-button @click="$router.push('/Create')" v-show="$route.path === '/profile'" class="mr-5" >Создать пост</blue-button>


      <div class="mb-0 flex items-center ">
        <div class="hover:cursor-pointer block 2xl:hidden bg-gray-200 ring-4 mr-5 ring-black/0 hover:bg-gray-300 hover:ring-gray-200  transition ease-in-out rounded-2xl p-3 sm:mr-12">
          <Filter/>
        </div>
        <div class="hover:cursor-pointer bg-gray-200 ring-4 ring-black/0 hover:bg-gray-300 hover:ring-gray-200  transition ease-in-out rounded-2xl p-3 sm:mr-12">
          <Settings/>
        </div>


        <div class="hidden md-4 min-w-51 sm:flex w-full max-w-sm bg-gray-200 rounded-lg relative">
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
import { Settings, Search, Filter } from 'lucide-vue-next';
import BlueButton from "@/components/UI/blueButton.vue";
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