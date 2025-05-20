<template>
  <div>
    <h1 class="text-2xl font-bold mb-6">Твои новости</h1>
    <div v-if="news && news.length" class="space-y-6 flex flex-col items-center space-x-2">
      <transition-group name="post-fade">
        <post-main 
          v-for="post in news" 
          :key="post.post_id" 
          :post="post" 
          @click="$router.push(`/post/${post.post_id}`)"
        />
      </transition-group>
    </div>
    <div v-else class="text-center mt-20">
      <h1 class="text-2xl font-bold mb-2">У вас пока нет опубликованных новостей</h1>
      <p class="text-gray-500 mb-6">Создайте свою первую новость и поделитесь ей с другими</p>
      <button
          class="px-4 py-2 bg-blue-600 hover:bg-blue-700 transition text-white rounded"
          @click="$router.push('/Create')"
      >
        Создать новость
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useToast } from "vue-toastification"
import jwtApi from "@/api/jwtApi.js"
import PostMain from "@/components/postMain.vue"
import router from "@/router/router.js"

const news = ref([])
const toast = useToast()

const loadNews = async () => {
  try {
    const response = await jwtApi.get(`${import.meta.env.VITE_BASE_URL}/user/HomePage`)
    news.value = response.data.user_posts.filter(post => post.status === "published")
  } catch (error) {
    console.error('Ошибка при загрузке новостей:', error)
    toast.error('Не удалось загрузить новости')
  }
}

onMounted(loadNews)

defineExpose({
  news,
  loadNews
})
</script>

<style scoped>
.post-fade-move,
.post-fade-enter-active,
.post-fade-leave-active {
  transition: all 0.5s ease;
}

.post-fade-enter-from,
.post-fade-leave-to {
  opacity: 0;
  transform: translateY(30px);
}

.post-fade-leave-active {
  position: absolute;
  width: 100%;
}
</style> 