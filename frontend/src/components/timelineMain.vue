<template>
  <div class="group cursor-pointer  relative pl-6">
    <!-- Вертикальная линия -->
    <div class="absolute left-2.5 top-0 bottom-0 w-px bg-blue-100"></div>

    <!-- Точка времени -->
    <div class="absolute left-0 top-12">
      <div class="relative">
        <!-- Внешний круг -->
        <div class="w-5 h-5 rounded-full bg-white border-2 border-blue-200 group-hover:border-blue-400 transition-colors duration-300"></div>
        <!-- Внутренний круг -->
        <div class="absolute inset-1.5 rounded-full bg-blue-400 group-hover:bg-blue-500 transition-colors duration-300"></div>
      </div>
    </div>

    <!-- Контент -->
    <div class="relative shadow-sm bg-white/60 hover:bg-white/90 backdrop-blur-sm rounded-xl p-4 transition-all duration-300 ml-4">
      <!-- Время -->


      <!-- Заголовок -->
      <h3 class="text-base font-medium text-gray-900 group-hover:text-blue-600 transition-colors duration-300 mb-2">
        {{ timeline.title }}
      </h3>

      <!-- Дата -->
      <div class="flex items-center text-sm text-gray-500">
        <CalendarDays  class="w-4 h-4 mr-1.5 mb-1"/>
        <span>{{ timestampToDate(timeline.start_date) }} - {{ timestampToDate(timeline.end_date) }}</span>
      </div>
      <span class="text-sm font-medium text-gray-500 bg-white/80  rounded-full ">
           ТУТ НАДО РАСЧИТАТЬ СКОЛЬКО ВРЕМЕНИ ПРОШЛО
        </span>
    </div>


    <!-- Отступ между элементами -->
    <div class="h-2"></div>
  </div>
</template>

<script setup>
import { CalendarDays } from 'lucide-vue-next';
import { defineProps } from 'vue';

const props = defineProps({
  timeline: Object
});
function timestampToDate(ts) {
  const date = new Date(ts * 1000); // если timestamp в секундах
  const day = String(date.getDate()).padStart(2, '0');
  const month = String(date.getMonth() + 1).padStart(2, '0'); // месяцы с 0
  const year = date.getFullYear();
  return `${day}.${month}.${year}`;
}
</script>



<style scoped>
.group:last-child .h-8 {
  display: none;
}
</style>