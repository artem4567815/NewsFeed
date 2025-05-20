<template>
  <div>
    <h1 class="text-2xl font-bold mb-6">Модерация</h1>
    <div v-if="moderationPosts && moderationPosts.length" class="bg-white p-6 rounded-lg shadow space-y-4">
      <div class="border-b pb-2">
        <h2 class="text-lg font-semibold">Ожидают проверки</h2>
      </div>
      <div class="space-y-6">
        <transition-group name="post-fade">
          <div v-for="post in moderationPosts" :key="post.post_id" class="flex flex-col items-center">
            <post-main @click="$router.push(`/post/${post.post_id}`)" :post="post" />
            <div class="mt-2 flex flex-wrap gap-2">
              <button @click="showApproveModal(post)" class="bg-green-500 hover:bg-green-600 text-white px-3 py-2 rounded-2xl transition">Одобрить</button>
              <button @click="showRejectModal(post)" class="bg-red-500 hover:bg-red-600 text-white px-3 py-2 rounded-2xl transition">Отклонить</button>
            </div>
          </div>
        </transition-group>
      </div>
    </div>
    <div v-else class="text-center mt-20">
      <h1 class="text-2xl font-bold mb-2">Нет публикаций для модерации</h1>
      <p class="text-gray-500 mb-6">Все публикации проверены или ожидают отправки на модерацию</p>
    </div>

    <!-- Модальное окно одобрения -->
    <Dialog as="div" class="relative z-50" @close="closeApproveModal" :open="showApproveDialog">
      <div class="fixed inset-0 bg-black/30" aria-hidden="true" />

      <div class="fixed inset-0 flex items-center justify-center p-4">
        <DialogPanel class="mx-auto max-w-sm rounded bg-white p-6 shadow-xl">
          <DialogTitle as="h3" class="text-lg font-medium leading-6 text-gray-900 mb-4">
            Одобрить публикацию?
          </DialogTitle>
          
          <div class="mt-2">
            <p class="text-sm text-gray-500">
              Новость станет видна всем пользователям
            </p>
          </div>

          <div class="mt-6 flex justify-end gap-3">
            <button
              type="button"
              class="inline-flex justify-center rounded-md border border-transparent bg-gray-100 px-4 py-2 text-sm font-medium text-gray-900 hover:bg-gray-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-gray-500 focus-visible:ring-offset-2"
              @click="closeApproveModal"
            >
              Отмена
            </button>
            <button
              type="button"
              class="inline-flex justify-center rounded-md border border-transparent bg-green-500 px-4 py-2 text-sm font-medium text-white hover:bg-green-600 focus:outline-none focus-visible:ring-2 focus-visible:ring-green-500 focus-visible:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
              @click="confirmApprove"
              :disabled="isApproving"
            >
              <span v-if="isApproving">Одобрение...</span>
              <span v-else>Да, одобрить</span>
            </button>
          </div>
        </DialogPanel>
      </div>
    </Dialog>

    <!-- Модальное окно отклонения -->
    <Dialog as="div" class="relative z-50" @close="closeRejectModal" :open="showRejectDialog">
      <div class="fixed inset-0 bg-black/30" aria-hidden="true" />

      <div class="fixed inset-0 flex items-center justify-center p-4">
        <DialogPanel class="mx-auto max-w-lg rounded bg-white p-6 shadow-xl">
          <DialogTitle as="h3" class="text-lg font-medium leading-6 text-gray-900 mb-4">
            Причина отказа
          </DialogTitle>
          
          <div class="mt-2 space-y-3">
            <div v-for="reason in standardReasons" :key="reason.id" class="flex items-center">
              <input
                type="checkbox"
                :id="reason.id"
                v-model="selectedReasons"
                :value="reason.id"
                class="mr-2 h-5 w-5 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                @change="handleReasonChange(reason.id)"
              >
              <label :for="reason.id" class="text-gray-700">{{ reason.label }}</label>
            </div>

            <div v-if="showCustomReason" class="mt-3">
              <label class="block text-sm font-medium text-gray-700 mb-1">Укажите свою причину</label>
              <textarea
                v-model="customReason"
                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                rows="3"
                placeholder="Опишите причину..."
              ></textarea>
            </div>
          </div>

          <div class="mt-6 flex justify-end gap-3">
            <button
              type="button"
              class="inline-flex justify-center rounded-md border border-transparent bg-gray-100 px-4 py-2 text-sm font-medium text-gray-900 hover:bg-gray-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-gray-500 focus-visible:ring-offset-2"
              @click="closeRejectModal"
            >
              Отмена
            </button>
            <button
              type="button"
              class="inline-flex justify-center rounded-md border border-transparent bg-red-500 px-4 py-2 text-sm font-medium text-white hover:bg-red-600 focus:outline-none focus-visible:ring-2 focus-visible:ring-red-500 focus-visible:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
              @click="confirmReject"
              :disabled="!canReject || isRejecting"
            >
              <span v-if="isRejecting">Отклонение...</span>
              <span v-else>Подтвердить</span>
            </button>
          </div>
        </DialogPanel>
      </div>
    </Dialog>

    <!-- Модальное окно подтверждения отклонения -->
    <Dialog as="div" class="relative z-50" @close="closeRejectConfirmModal" :open="showRejectConfirmDialog">
      <div class="fixed inset-0 bg-black/30" aria-hidden="true" />

      <div class="fixed inset-0 flex items-center justify-center p-4">
        <DialogPanel class="mx-auto max-w-lg rounded bg-white p-6 shadow-xl">
          <DialogTitle as="h3" class="text-lg font-medium leading-6 text-gray-900 mb-4">
            Подтвердите отказ
          </DialogTitle>
          
          <div class="mt-2">
            <p class="text-gray-600 mb-4">Вы точно хотите отклонить новость?</p>
            <div class="p-3 bg-gray-50 rounded-md">
              <p class="font-medium mb-2">Причины:</p>
              <ul class="list-disc pl-5 space-y-1">
                <li v-for="reason in formattedReasons" :key="reason">{{ reason }}</li>
              </ul>
            </div>
          </div>

          <div class="mt-6 flex justify-end gap-3">
            <button
              type="button"
              class="inline-flex justify-center rounded-md border border-transparent bg-gray-100 px-4 py-2 text-sm font-medium text-gray-900 hover:bg-gray-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-gray-500 focus-visible:ring-offset-2"
              @click="closeRejectConfirmModal"
            >
              Отмена
            </button>
            <button
              type="button"
              class="inline-flex justify-center rounded-md border border-transparent bg-red-500 px-4 py-2 text-sm font-medium text-white hover:bg-red-600 focus:outline-none focus-visible:ring-2 focus-visible:ring-red-500 focus-visible:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
              @click="submitReject"
              :disabled="isRejecting"
            >
              <span v-if="isRejecting">Отклонение...</span>
              <span v-else>Да, отклонить</span>
            </button>
          </div>
        </DialogPanel>
      </div>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useToast } from "vue-toastification"
import jwtApi from "@/api/jwtApi.js"
import PostMain from "@/components/postMain.vue"
import router from "@/router/router.js"
import { Dialog, DialogPanel, DialogTitle } from '@headlessui/vue'

const toast = useToast()
const moderationPosts = ref([])

// Состояния для модалок
const showApproveDialog = ref(false)
const showRejectDialog = ref(false)
const showRejectConfirmDialog = ref(false)
const isApproving = ref(false)
const isRejecting = ref(false)
const postToModerate = ref(null)

// Состояния для формы отклонения
const standardReasons = [
  { id: 'spam', label: 'Спам' },
  { id: 'offensive', label: 'Оскорбительный контент' },
  { id: 'false_info', label: 'Ложная информация' },
  { id: 'copyright', label: 'Нецензурная лексика' },
  { id: 'tags', label: 'Некорректные теги' },
  { id: 'login', label: 'Нецензурный логин' },
  { id: 'building', label: 'Несуществуящая школа или корпус' },
  { id: 'other', label: 'Другая причина' }
]
const selectedReasons = ref([])
const customReason = ref('')
const showCustomReason = ref(false)

// Вычисляемые свойства
const canReject = computed(() => {
  if (selectedReasons.value.length === 0) return false
  if (selectedReasons.value.includes('other') && !customReason.value.trim()) return false
  return true
})

const formattedReasons = computed(() => {
  return selectedReasons.value.map(reasonId => {
    if (reasonId === 'other') return customReason.value
    return standardReasons.find(r => r.id === reasonId)?.label
  }).filter(Boolean)
})

const loadModerationPosts = async () => {
  try {
    const response = await jwtApi.get(`${import.meta.env.VITE_BASE_URL}/admin/moderation`)
    moderationPosts.value = response.data.wall_newspapers
  } catch (error) {
    console.error('Ошибка при загрузке постов для модерации:', error)
    toast.error('Не удалось загрузить посты для модерации')
  }
}

onMounted(loadModerationPosts)

// Методы для модалки одобрения
const showApproveModal = (post) => {
  postToModerate.value = post
  showApproveDialog.value = true
}

const closeApproveModal = () => {
  showApproveDialog.value = false
  postToModerate.value = null
}

const confirmApprove = async () => {
  if (!postToModerate.value) return
  
  isApproving.value = true
  try {
    await jwtApi.post(`${import.meta.env.VITE_BASE_URL}/admin/moderation/${postToModerate.value.post_id}/apply`, postToModerate.value.post_id)
    moderationPosts.value = moderationPosts.value.filter(post => post.post_id !== postToModerate.value.post_id)
    toast.success('Новость одобрена!')
    closeApproveModal()
  } catch (error) {
    toast.error('Ошибка при одобрении')
  } finally {
    isApproving.value = false
  }
}

// Методы для модалки отклонения
const showRejectModal = (post) => {
  postToModerate.value = post
  showRejectDialog.value = true
  selectedReasons.value = []
  customReason.value = ''
  showCustomReason.value = false
}

const closeRejectModal = () => {
  showRejectDialog.value = false
  postToModerate.value = null
  selectedReasons.value = []
  customReason.value = ''
  showCustomReason.value = false
}

const handleReasonChange = (reasonId) => {
  if (reasonId === 'other') {
    showCustomReason.value = selectedReasons.value.includes('other')
  }
}

const confirmReject = () => {
  if (!canReject.value) return
  showRejectDialog.value = false
  showRejectConfirmDialog.value = true
}

const closeRejectConfirmModal = () => {
  showRejectConfirmDialog.value = false
  postToModerate.value = null
  selectedReasons.value = []
  customReason.value = ''
  showCustomReason.value = false
}

const submitReject = async () => {
  if (!postToModerate.value || !canReject.value) return
  
  isRejecting.value = true
  try {
    await jwtApi.post(
      `${import.meta.env.VITE_BASE_URL}/admin/moderation/${postToModerate.value.post_id}/reject`,
      { reason: formattedReasons.value },
      { headers: { 'Content-Type': 'application/json' } }
    )
    moderationPosts.value = moderationPosts.value.filter(post => post.post_id !== postToModerate.value.post_id)
    toast.success('Новость отклонена!')
    closeRejectConfirmModal()
  } catch (error) {
    toast.error('Ошибка при отклонении')
  } finally {
    isRejecting.value = false
  }
}

defineExpose({
  moderationPosts,
  loadModerationPosts
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