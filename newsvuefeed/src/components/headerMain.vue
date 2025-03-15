<template class="">
  <header class="py-2 px-7 border-b-2 border-gray-200 flex items-center justify-between gap-3 mb-10">
    <div class="flex items-center whitespace-nowrap">
      <div class="text-2xl mr-15 font-semibold">EduFeed</div>
      <div class="flex gap-3 mr-5">
        <div class="mr-5">Выбор школы</div>
        <div>Поиск по дате</div>
      </div>
    </div>

    <div class="flex justify-center items-center">
      <div class="bg-blue-500 rounded-2xl text-white px-3 py-2 mr-5 ">Вход</div>
      <div class="mb-0 flex items-center ">
        <div class="bg-gray-200 rounded-2xl p-3 mr-12">
          <Settings/>
        </div>

        <div class="relative w-full max-w-sm bg-gray-200 rounded-lg">
          <input type="text" placeholder="Найти новость..." class="w-full pl-10 pr-4 py-2 text-lg rounded-lg border border-gray-300 "/>
          <span class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500">
            <Search/>
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
  name: 'header-main',
}
</script>

<style lang="scss" scoped>

</style>