<template>
  <form-auth v-show="showModal === 'auth'" ></form-auth>
  <form-reg v-show="showModal === 'reg'"></form-reg>
  <header-main></header-main>
  
  <div class="grid grid-flow-col xl:grid-cols-5">
    <div class="flex flex-col items-center col-span-4">
      <div class="w-10/12 h-10 flex border-b-3 border-gray-300">
        <div class="mr-12 pb-4 border-b-5 border-gray-400">Новости</div>
        <div class="mr-12 pb-4 border-b-5 border-gray-400">Стенгазеты</div>
        <div class="mr-12 pb-4 border-b-5 border-gray-400">Поиск команды</div>
      </div>

      <post-main @click="$router.push('/post/id')" class="hover:cursor-pointer justify-self-center"></post-main>
      <post-main @click="$router.push('/post/id')" class="justify-self-center"></post-main>
      <post-main @click="$router.push('/post/id')" class="justify-self-center"></post-main>
      <post-main @click="$router.push('/post/id')" class="justify-self-center"></post-main>
      <post-main @click="$router.push('/post/id')" class="justify-self-center"></post-main>

    </div>
     <div class="hidden xl:flex items-center flex-col">
      <timeline-main v-for="i in 8" :key="i" @click="$router.push('/post/id')" class="hover:cursor-pointer"></timeline-main>
    </div>
  </div>
  
</template>

<script>

import { ref, onMounted } from 'vue'
import emitter from '@/main'

export default {
  data() {
    return {
    showModal: "",
    }
  },
  methods: {
    show() {
      console.log(q)
      this.showModal = true
    }
  },
  mounted() {
    emitter.on("ShowModalAuth", () => {
      this.showModal = "auth";
    });
    emitter.on("hideModal", () => {
      this.showModal = "";
    });
    emitter.on("ShowModalReg", () => {
      this.showModal = "reg";
    });
  },
  setup() {
  
  const News = ref([]);
      onMounted(async () => {
        try {
          const NewsResponse = await fetch(`${import.meta.env.VITE_BASE_URL}/posts/news`, {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
            },
          });
          console.log(NewsResponse.value)
          console.log(import.meta.env.VITE_BASE_URL);
      
          if (!NewsResponse.ok) throw new Error('Ошибка при загрузке новостей');
          News.value = await NewsResponse.json();
        } catch (error) {
          console.error('Ошибка загрузки новостей:', error);
        }
      });
    }
  }
</script>

<style scoped>

</style>