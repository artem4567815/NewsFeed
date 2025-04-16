<template>
  <div class="min-h-screen  bg-pattern">
    <div class="relative flex justify-center">
      <div class="flex w-full justify-center max-w-[2000px]">
        <!-- Основной контейнер -->
        <div class="flex-1 p-2 sm:p-8 2xl:max-w-[calc(100%-280px)]">

          <!-- Заголовок новости -->
          <div class="mb-8">
            <div class="flex items-center gap-2 mb-4">
              <h1 class="text-3xl font-bold text-gray-900 sm:text-4xl">{{post.title}}</h1>
            </div>

            <div class="flex flex-wrap items-center gap-4 text-sm text-gray-500">
              <div class="flex items-center gap-2">
                <span class="font-medium text-gray-700">ТУТ БУДЕТ ШКОЛА КОРПУС</span>
              </div>
              <div class="flex items-center gap-2">
                <CalendarDays class="w-4 h-4" />
                <span>12.03.2025</span>
              </div>

              <div class="flex items-center gap-2">
                <Eye class="w-4 h-4" />
                <span>{{post.views}} просмотров</span>
              </div>
              <span class="px-3 py-1 text-sm font-medium rounded-full bg-blue-100 text-blue-800">Мероприятие</span>
            </div>
          </div>

          <!-- Основное содержимое новости -->
          <div class="bg-white rounded-2xl shadow-sm overflow-hidden mb-8">
            <!-- Изображение новости (заглушка) -->
            <img
                src="https://loremflickr.com/800/450"
                alt="Изображение новости"
                class="w-full aspect-16/9 lg:h-full object-cover"
            />

            <!-- Текст новости -->
            <div class="p-6 sm:p-8">
              <p class="text-lg text-gray-700 mb-6">
                Приглашаем всех родителей и будущих учеников на день открытых дверей в нашу школу.
                Вы сможете познакомиться с преподавателями и программами обучения.
              </p>

              <div class="prose max-w-none text-gray-700 mb-8">
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent euismod, nisi eget fermentum aliquam, nisi nunc tincidunt nunc, eget tincidunt nisi nisi eget nisi. Nulla facilisi. Nulla facilisi. Nulla facilisi. Nulla facilisi.</p>

                <h2 class="text-xl font-bold mt-8 mb-4 text-gray-900">Подробности события</h2>

                <p>Curabitur auctor, nisi eget fermentum aliquam, nisi nunc tincidunt nunc, eget tincidunt nisi nisi eget nisi. Nulla facilisi. Nulla facilisi. Nulla facilisi. Nulla facilisi.</p>

                <blockquote class="border-l-4 border-blue-500 pl-4 italic my-6 text-gray-600">
                  <p>"Образование — это не подготовка к жизни; образование — это и есть жизнь."</p>
                  <footer class="mt-2 text-sm font-medium text-gray-500">— Джон Дьюи</footer>
                </blockquote>

                <p>Praesent euismod, nisl eget fermentum aliquam, nisl nunc tincidunt nunc, eget tincidunt nisl nisl eget nisl. Nulla facilisi. Nulla facilisi. Nulla facilisi. Nulla facilisi. Nulla facilisi.</p>
              </div>

              <!-- Действия с новостью -->
              <div class="flex flex-wrap items-center justify-between gap-4 pt-6 border-t border-gray-200">
                <div class="flex items-center gap-2">
                  <button class="flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200">
                    <Heart class="w-4 h-4" />
                    <span>128</span>
                  </button>
                  <button class="flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200">
                    <MessageSquare class="w-4 h-4" />
                    <span>24</span>
                  </button>
                </div>

                <div class="flex items-center gap-2">
                  <button class="flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200">
                    <Bookmark class="w-4 h-4" />
                    <span>Сохранить</span>
                  </button>
                  <button class="flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200">
                    <Share2 class="w-4 h-4" />
                    <span>Поделиться</span>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Похожие новости -->
          <div class="mb-12">
            <h2 class="text-2xl font-bold text-gray-900 mb-6">Похожие новости</h2>

            <div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
<!--              <post-vertical v-for="i in 3" @click="$router.push(`/post/${post.id}`)"></post-vertical>-->
            </div>
          </div>
        </div>
      </div>
    </div>

    <footer-main></footer-main>
  </div>
</template>

<script setup>
import { CalendarDays, Clock, Eye, Heart, MessageSquare, Bookmark, Share2 } from 'lucide-vue-next'
import {onMounted, ref} from 'vue'
import FilterPanel from "@/components/filterPanel.vue"
import PostMain from "@/components/postMain.vue";
import PostVertical from "@/components/postVertical.vue";
import {useRoute} from "vue-router";



const route = useRoute(); // Получаем объект маршрута

const post = ref(null);

onMounted(async () => {
  try {
    const NewsResponse = await fetch(`${import.meta.env.VITE_BASE_URL}/posts/${route.params.id}?from=main`);
    if (!NewsResponse.ok) throw new Error('Ошибка при загрузке новости');
    let get_data = await NewsResponse.json();
    post.value = get_data;
  } catch (error) {
    console.error('Ошибка загрузки новостей:', error);
  }
});
</script>

<style scoped>
/* Используем те же стили, что и на главной странице */
.bg-pattern {
  background: linear-gradient(135deg, #f6f8ff 0%, #f0f4ff 100%);
  background-image:
      radial-gradient(at 20% 25%, rgba(59, 130, 246, 0.04) 0px, transparent 50%),
      radial-gradient(at 80% 75%, rgba(99, 102, 241, 0.03) 0px, transparent 50%),
      radial-gradient(at 50% 50%, rgba(139, 92, 246, 0.05) 0px, transparent 50%);
  background-attachment: fixed;
  background-size: cover;
  position: relative;
}

.bg-pattern::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%236366f1' fill-opacity='0.02'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  opacity: 0.5;
  pointer-events: none;
}

.timeline-scroll::-webkit-scrollbar {
  width: 4px;
}

.timeline-scroll::-webkit-scrollbar-track {
  background: transparent;
}

.timeline-scroll::-webkit-scrollbar-thumb {
  background: #a7f3d0;
  border-radius: 4px;
}

.timeline-scroll::-webkit-scrollbar-thumb:hover {
  background: #6ee7b7;
}
</style>