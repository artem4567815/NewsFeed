<template>
  <div
      ref="card"
      class=" bg-white rounded-2xl shadow-lg overflow-hidden w-95/100 transition-transform duration-300 ease-out cursor-pointer"
  >
    <div class="flex flex-col md:flex-row h-full">
      <!-- Изображение -->
      <div class="md:w-[500px] relative overflow-hidden">
        <img
            src="https://picsum.photos/800/450"
            alt="Изображение новости"
            class="w-full aspect-16/9 md:h-full object-cover"
        />
      </div>

      <!-- Контент -->
      <div class="flex-1 p-6 md:p-8 flex flex-col min-h-[350px] relative">
        <!-- Категория -->
        <div class="absolute top-4 right-4">
          <span class="bg-blue-600 text-white px-4 py-1.5 rounded-full text-sm font-medium shadow-sm">
            Технологии
          </span>
        </div>

        <div class="flex-1 mt-8 md:mt-6">
          <!-- Метаданные -->
          <div class="flex items-center space-x-4 mb-4">
            <span class="flex items-center text-sm font-medium text-gray-600">
              <CalendarDays class="w-4 h-4 mr-1.5 mb-1" />
              13.03.2024
            </span>
            <span class="flex items-center text-sm font-medium text-gray-600">
              <Clock class="w-4 h-4 mr-1.5 mb-1" />
              2 часа назад
            </span>
          </div>

          <!-- Заголовок -->
          <h2 class="text-2xl font-bold text-gray-900 mb-4 leading-tight hover:text-blue-600 transition-colors duration-200">
            Важное событие в мире технологий и инноваций
          </h2>

          <!-- Описание -->
          <p class="text-base text-gray-700 mb-6 leading-relaxed line-clamp-3">
            Краткое описание новости, которое дает представление о содержании статьи. Здесь может быть несколько строк текста, которые будут обрезаны при необходимости. Дополнительная информация о событии и его значимости.
          </p>
        </div>

        <!-- Нижняя часть -->
        <div class="flex items-center justify-between pt-4 border-t border-gray-100">
          <!-- Автор -->
          <div class="flex items-center">
            <div
                class="w-12 h-12 rounded-full bg-gradient-to-r from-blue-500 to-blue-600 flex items-center justify-center text-white font-bold text-lg"
            >
              A
            </div>
            <div class="ml-3">
              <p class="text-base font-medium text-gray-900">Автор новости</p>
              <p class="text-sm text-gray-600">Редактор</p>
            </div>
          </div>

          <!-- Статистика -->
          <div class="flex items-center space-x-6">
            <button
                class="flex items-center space-x-2 text-gray-500 hover:text-blue-600 transition-colors duration-200"
            >
              <Heart />
              <span class="text-base font-medium">128</span>
            </button>
            <span class="flex items-center text-base font-medium text-gray-600">
              <Eye class="mr-2.5" />
              1.2K
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Eye } from 'lucide-vue-next';
import { CalendarDays } from 'lucide-vue-next';
import { Clock } from 'lucide-vue-next';
import { Heart } from 'lucide-vue-next';
import { onMounted, onUnmounted, ref } from "vue";
import VanillaTilt from "vanilla-tilt";

const card = ref(null);

onMounted(() => {
  if (card.value) {
    VanillaTilt.init(card.value, {
      max: 3, // Чуть больше, чтобы было естественно
      speed: 200, // Понизил скорость, чтобы не было рывков
      perspective: 1200, // Чуть меньше для лучшей плавности
      scale: 1.01, // Легкий эффект увеличения
      easing: "cubic-bezier(.03,.98,.52,.99)", // Плавность движения
      glare: false, // Убираем блики, они вызывают лаги
    });
  }
});

onUnmounted(() => {
  if (card.value && card.value.vanillaTilt) {
    card.value.vanillaTilt.destroy();
    card.value.vanillaTilt = null;
  }
});
</script>

<script>
export default {
  name: "post-main",
  props: {
    post: Object
  }
};
</script>

<style lang="scss" scoped>
</style>
