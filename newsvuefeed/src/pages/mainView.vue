<template>

  <header-main></header-main>

  <div class="grid grid-flow-col xl:grid-cols-5">
    <div class="flex flex-col items-center col-span-4">
      <div class="w-10/12 h-10 flex border-b-3 border-gray-300">
        <div class="mr-12 pb-4 border-b-5 border-gray-400">Новости</div>
        <div class="mr-12 pb-4 border-b-5 border-gray-400">Стенгазеты</div>
        <div class="mr-12 pb-4 border-b-5 border-gray-400">Поиск команды</div>
      </div>
      <div v-for="post in posts" :key="post.news_id">
        <post-main :post="post" @click="$router.push('/post/id')" class="justify-self-center"></post-main>
      </div>
    </div>
<!--     <div class="hidden xl:flex items-center flex-col">-->
<!--      <timeline-main v-for="timeline in posts" :key="post.news_id" @click="$router.push('/post/id')" class="hover:cursor-pointer"></timeline-main>-->
<!--    </div>-->
  </div>

</template>

<script>

import { ref, onMounted } from 'vue'
import emitter from '@/main'



export default {

  setup() {
    const posts = ref([]);

    onMounted(async () => {
      try {
        const NewsResponse = await fetch(`${import.meta.env.VITE_BASE_URL}/posts?type=news`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        });
        console.log(import.meta.env.VITE_BASE_URL);

        if (!NewsResponse.ok) throw new Error('Ошибка при загрузке новостей');
        posts.value = await NewsResponse.json();
        console.log(posts)
      } catch (error) {
        console.error('Ошибка загрузки новостей:', error);
      }
    });
    return {
      posts
    }
    },
  }
</script>

<style scoped>

</style>