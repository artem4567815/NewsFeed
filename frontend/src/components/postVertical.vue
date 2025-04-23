<template>
  <div
      ref="card"
      class=" bg-white rounded-2xl max-w-150 shadow-lg overflow-hidden w-95/100 transition-transform duration-300 ease-out cursor-pointer"
  >
    <div class="flex flex-col  h-full">
      <!-- Изображение -->
      <div class=" relative overflow-hidden">
        <img
            src="https://loremflickr.com/800/450"
            alt="Изображение новости"
            class="w-full aspect-16/9 lg:h-full object-cover"
        />
      </div>

      <!-- Контент -->
      <div class="flex-1 p-2 md:p-4 flex flex-col min-h-[350px] relative">
        <!-- Категория -->
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
        <div class="flex items-center space-x-4 timeline-scroll overflow-x-auto mb-4">
          <div class="bg-blue-600/20 text-blue-600  border-blue-600/40  border-1 px-3 py-1 rounded-full text-sm font-medium ">
            Технологии
          </div>
          <div class="bg-green-600/20 text-green-600  border-green-600/40  border-1 px-3 py-1 rounded-full text-sm font-medium ">
            автобусы
          </div>
          <div class="bg-orange-600/20 text-orange-600 border-orange-600/40  border-1 px-3 py-1 rounded-full text-sm font-medium ">
            Технологии
          </div>
          <div class="bg-violet-600/20 text-violet-600 border-violet-600/40  ring-1 px-3 py-1 rounded-full text-sm font-medium ">
            dbedbe
          </div>

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



<style lang="scss" scoped>
.timeline-scroll::-webkit-scrollbar {
  margin-top: 4px;
  width: 4px;
}

.timeline-scroll::-webkit-scrollbar-track {
  background: transparent;
}

.timeline-scroll::-webkit-scrollbar-thumb {
  background: #e5e7eb;
  border-radius: 4px;
}

.timeline-scroll::-webkit-scrollbar-thumb:hover {
  background: #d1d5db;
}

/* Стилизация скроллбара таймлайна в зеленой теме */
.timeline-scroll::-webkit-scrollbar-thumb {
  background: #a7d6f3;
}

.timeline-scroll::-webkit-scrollbar-thumb:hover {
  background: #6ee7b7;
}
</style>
