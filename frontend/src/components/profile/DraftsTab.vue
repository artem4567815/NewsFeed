<template>
  <div>
    <h1 class="text-2xl font-bold mb-6">Твои черновики</h1>
    <div v-if="drafts && drafts.length" class="space-y-6 w-full flex flex-col items-center space-x-2">
      <transition-group name="post-fade" class="w-full" tag="div">
        <div
            v-for="post in drafts"
            :key="post.post_id + '-' + post.status"
            class="mb-4 w-full"
        >
          <post-main :post="post" @click="$router.push(`/post/${post.post_id}`)" />
          <div v-if="post.status === 'draft'" class="flex justify-center gap-2 mt-2">
            <button @click="showModerationModal(post)" class="bg-blue-500 text-white px-3 py-2 rounded-xl">На модерацию</button>
          </div>
          <div v-if="post.status === 'rejected'" class="flex justify-center gap-2 mt-2">
            <button @click="showRejectionReasonModal(post)" class="bg-red-500 text-white px-3 py-2 rounded-xl">Причина отказа</button>
          </div>
        </div>
      </transition-group>
    </div>
    <div v-else class="text-center mt-20">
      <h1 class="text-2xl font-bold mb-2">У вас пока нет черновиков</h1>
      <p class="text-gray-500 mb-6">Здесь будут отображаться ваши сохраненные черновики.</p>
      <button @click="$router.push('/Create')" class="px-4 py-2 bg-blue-600 hover:bg-blue-700 transition text-white rounded">Создать новость</button>
    </div>

    <!-- Модальное окно отправки на модерацию -->
    <Dialog as="div" class="relative z-50" @close="closeModerationModal" :open="showModerationDialog">
      <div class="fixed inset-0 bg-black/30" aria-hidden="true" />

      <div class="fixed inset-0 flex items-center justify-center p-4">
        <DialogPanel class="mx-auto max-w-sm rounded bg-white p-6 shadow-xl">
          <DialogTitle as="h3" class="text-lg font-medium leading-6 text-gray-900 mb-4">
            Отправить на модерацию?
          </DialogTitle>
          
          <div class="mt-2">
            <p class="text-sm text-gray-500">
              Вы уверены, что хотите отправить этот пост на проверку?
            </p>
          </div>

          <div class="mt-6 flex justify-end gap-3">
            <button
              type="button"
              class="inline-flex justify-center rounded-md border border-transparent bg-gray-100 px-4 py-2 text-sm font-medium text-gray-900 hover:bg-gray-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-gray-500 focus-visible:ring-offset-2"
              @click="closeModerationModal"
            >
              Отмена
            </button>
            <button
              type="button"
              class="inline-flex justify-center rounded-md border border-transparent bg-blue-500 px-4 py-2 text-sm font-medium text-white hover:bg-blue-600 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
              @click="confirmModeration"
              :disabled="isSending"
            >
              <span v-if="isSending">Отправка...</span>
              <span v-else>Да, отправить</span>
            </button>
          </div>
        </DialogPanel>
      </div>
    </Dialog>

    <!-- Модальное окно причин отказа -->
    <Dialog as="div" class="relative z-50" @close="closeRejectionReasonModal" :open="showRejectionReasonDialog">
      <div class="fixed inset-0 bg-black/30" aria-hidden="true" />

      <div class="fixed inset-0 flex items-center justify-center p-4">
        <DialogPanel class="mx-auto max-w-lg rounded bg-white p-6 shadow-xl">
          <DialogTitle as="h3" class="text-lg font-medium leading-6 text-gray-900 mb-4">
            Причина отказа
          </DialogTitle>
          
          <div class="mt-2">
            <ul class="text-left space-y-1 list-disc pl-6">
              <li v-for="reason in rejectionReasons" :key="reason">{{ reason }}</li>
            </ul>
          </div>

          <div class="mt-6 flex justify-end">
            <button
              type="button"
              class="inline-flex justify-center rounded-md border border-transparent bg-gray-100 px-4 py-2 text-sm font-medium text-gray-900 hover:bg-gray-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-gray-500 focus-visible:ring-offset-2"
              @click="closeRejectionReasonModal"
            >
              Закрыть
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
import { Dialog, DialogPanel, DialogTitle } from '@headlessui/vue'

const toast = useToast()
const drafts = ref([])

// Состояния для модалок
const showModerationDialog = ref(false)
const showRejectionReasonDialog = ref(false)
const isSending = ref(false)
const postToModerate = ref(null)
const rejectionReasons = ref([])

const loadDrafts = async () => {
  try {
    const response = await jwtApi.get(`${import.meta.env.VITE_BASE_URL}/user/HomePage`)
    drafts.value = response.data.user_posts.filter(post => post.status !== "published")
  } catch (error) {
    console.error('Ошибка при загрузке черновиков:', error)
    toast.error('Не удалось загрузить черновики')
  }
}

onMounted(loadDrafts)

const showModerationModal = (post) => {
  postToModerate.value = post
  showModerationDialog.value = true
}

const closeModerationModal = () => {
  showModerationDialog.value = false
  postToModerate.value = null
}

const confirmModeration = async () => {
  if (!postToModerate.value) return
  
  isSending.value = true
  try {
    const post = drafts.value.find(p => p.post_id === postToModerate.value.post_id)
    drafts.value = drafts.value.filter(p => p.post_id !== postToModerate.value.post_id)

    await jwtApi.post(`${import.meta.env.VITE_BASE_URL}/user/${postToModerate.value.post_id}/send/to/moderation`, postToModerate.value.post_id)
    toast.success('Пост отправлен на модерацию!')

    setTimeout(() => {
      smoothScrollToTop()
    }, 300)
  } catch (error) {
    toast.error('Не удалось отправить пост')
  } finally {
    isSending.value = false
    closeModerationModal()
  }
}

const showRejectionReasonModal = (post) => {
  postToModerate.value = post
  rejectionReasons.value = post.reasons
  showRejectionReasonDialog.value = true
}

const closeRejectionReasonModal = () => {
  showRejectionReasonDialog.value = false
  postToModerate.value = null
  rejectionReasons.value = []
}

const smoothScrollToTop = () => {
  const mainContent = document.querySelector('main')
  if (!mainContent) return

  mainContent.scrollTo({
    top: 0,
    behavior: 'smooth'
  })
}

defineExpose({
  drafts,
  loadDrafts
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