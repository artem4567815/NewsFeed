<template>
  <div>
    <h1 class="text-2xl font-bold mb-6">Все новости</h1>
    <div v-if="allPosts && allPosts.length" class="space-y-6 flex flex-col items-center space-x-2">
      <transition-group name="post-fade">
        <div v-for="post in allPosts" :key="post.post_id" class="w-full flex flex-col items-center">
          <post-main @click="$router.push(`/post/${post.post_id}`)" :post="post" />
          <button 
            class="mt-2 hover:cursor-pointer bg-red-500 ring-4 ring-transparent hover:ring-red-700/30 hover:bg-red-600 transition ease-in rounded-2xl text-white px-3 py-2" 
            :value="post.post_id" 
            @click="showDeleteModal(post)"
          >
            Удалить новость
          </button>
        </div>
      </transition-group>
    </div>
    <div v-else class="text-center mt-20">
      <h1 class="text-2xl font-bold mb-2">Пока что нет новостей на сайте</h1>
      <p class="text-gray-500 mb-6">Создайте первую новость!</p>
      <button @click="$router.push('/Create')" class="px-4 py-2 bg-blue-600 hover:bg-blue-700 transition text-white rounded">Создать новость</button>
    </div>

    <!-- Модальное окно удаления -->
    <Dialog as="div" class="relative z-50" @close="closeModal" :open="showModal">
      <div class="fixed inset-0 bg-black/30" aria-hidden="true" />

      <div class="fixed inset-0 flex items-center justify-center p-4">
        <DialogPanel class="mx-auto max-w-sm rounded bg-white p-6 shadow-xl">
          <DialogTitle as="h3" class="text-lg font-medium leading-6 text-gray-900 mb-4">
            Удалить пост?
          </DialogTitle>
          
          <div class="mt-2">
            <p class="text-sm text-gray-500">
              Это действие нельзя отменить! Пост будет удалён навсегда.
            </p>
          </div>

          <div class="mt-6 flex justify-end gap-3">
            <button
              type="button"
              class="inline-flex justify-center rounded-md border border-transparent bg-gray-100 px-4 py-2 text-sm font-medium text-gray-900 hover:bg-gray-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-gray-500 focus-visible:ring-offset-2"
              @click="closeModal"
            >
              Отмена
            </button>
            <button
              type="button"
              class="inline-flex justify-center rounded-md border border-transparent bg-red-500 px-4 py-2 text-sm font-medium text-white hover:bg-red-600 focus:outline-none focus-visible:ring-2 focus-visible:ring-red-500 focus-visible:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
              @click="confirmDelete"
              :disabled="isDeleting"
            >
              <span v-if="isDeleting">Удаление...</span>
              <span v-else>Удалить</span>
            </button>
          </div>
        </DialogPanel>
      </div>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useToast } from "vue-toastification"
import jwtApi from "@/api/jwtApi.js"
import PostMain from "@/components/postMain.vue"
import router from "@/router/router.js"
import axios from "axios"
import { Dialog, DialogPanel, DialogTitle } from '@headlessui/vue'

const toast = useToast()
const allPosts = ref([])
const showModal = ref(false)
const postToDelete = ref(null)
const isDeleting = ref(false)

const loadAllPosts = async () => {
  try {
    const response = await axios.get(`${import.meta.env.VITE_BASE_URL}/posts`)
    allPosts.value = response.data.posts
  } catch (error) {
    console.error('Ошибка при загрузке всех постов:', error)
    toast.error('Не удалось загрузить список постов')
  }
}

onMounted(loadAllPosts)

const showDeleteModal = (post) => {
  postToDelete.value = post
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  postToDelete.value = null
}

const confirmDelete = async () => {
  if (!postToDelete.value) return
  
  isDeleting.value = true
  try {
    await jwtApi.delete(`${import.meta.env.VITE_BASE_URL}/posts/${postToDelete.value.post_id}`)
    allPosts.value = allPosts.value.filter(post => post.post_id !== postToDelete.value.post_id)
    toast.success('Пост удалён!')
    closeModal()
  } catch (error) {
    toast.error('Не удалось удалить пост')
  } finally {
    isDeleting.value = false
  }
}

defineExpose({
  allPosts,
  loadAllPosts
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

/* Анимации для модального окна */
.fixed {
  animation: fadeIn 0.2s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.bg-white {
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    transform: translateY(-20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}
</style> 