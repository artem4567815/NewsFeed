<template>
  <div class="group cursor-pointer relative pl-6">
    <!-- Вертикальная линия -->
    <div class="absolute left-2.5 top-0 bottom-0 w-px bg-blue-100"></div>

    <!-- Точка времени -->
    <div class="absolute left-0 top-2">
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
        {{ title }}
      </h3>

      <!-- Дата -->
      <div class="flex items-center text-sm text-gray-500">
        <CalendarDays  class="w-4 h-4 mr-1.5 mb-1"/>
        <span>{{ startDate }}</span>
      </div>
    </div>

    <div class=" ml-4 mt-2 flex items-center">
        <span class="text-sm font-medium text-gray-500 bg-white/80  px-2 py-0.5 rounded-full shadow-sm">
          {{ timePassed }}
        </span>
    </div>
    <!-- Отступ между элементами -->
    <div class="h-2"></div>
  </div>
</template>

<script setup>
import { CalendarDays } from 'lucide-vue-next';
</script>

<script>



export default {

  name: 'timeline-main',
  props: {
    title: String,
    startDate: String,
    endDate: String,
    timePassed: String
  }
}
</script>

<style scoped>
.group:last-child .h-8 {
  display: none;
}
</style>