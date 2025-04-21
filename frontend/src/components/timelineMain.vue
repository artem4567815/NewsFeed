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
      <h3 class="text-base font-medium break-all text-gray-900 group-hover:text-blue-600 transition-colors duration-300 mb-2">
        {{ timeline.title }}
      </h3>

      <!-- Дата -->
      <div class="flex items-center text-sm text-gray-500">
        <CalendarDays  class="w-4 h-4 mr-1.5 mb-1"/>
        <span>{{ timestampToDate(timeline.start_date) }} - {{ timestampToDate(timeline.end_date) }}</span>
      </div>
      <span class="text-sm font-medium text-gray-500 bg-white/80  rounded-full ">
           {{dateAgo}}
        </span>
    </div>


    <!-- Отступ между элементами -->
    <div class="h-2"></div>
  </div>
</template>

<script setup>
import { CalendarDays } from 'lucide-vue-next';
import {defineProps, ref} from 'vue';

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



setInterval(() => {
  dateAgo.value = timeAgo(props.timeline.published_at);
}, 1000); // обновляем каждую секунду

function timeAgo(timestampSec) {
  const now = Date.now();
  const timestampMs = timestampSec * 1000; // Переводим секунды в миллисекунды
  const seconds = Math.floor((now - timestampMs) / 1000);

  const intervals = [
    { label: ['секунда', 'секунды', 'секунд'], seconds: 1 },
    { label: ['минута', 'минуты', 'минут'], seconds: 60 },
    { label: ['час', 'часа', 'часов'], seconds: 3600 },
    { label: ['день', 'дня', 'дней'], seconds: 86400 },
    { label: ['неделя', 'недели', 'недель'], seconds: 604800 },
    { label: ['месяц', 'месяца', 'месяцев'], seconds: 2592000 },
    { label: ['год', 'года', 'лет'], seconds: 31536000 },
  ];

  function getPlural(n, forms) {
    const mod10 = n % 10;
    const mod100 = n % 100;
    if (mod10 === 1 && mod100 !== 11) return forms[0];
    if (mod10 >= 2 && mod10 <= 4 && (mod100 < 10 || mod100 >= 20)) return forms[1];
    return forms[2];
  }

  for (let i = intervals.length - 1; i >= 0; i--) {
    const interval = intervals[i];
    const count = Math.floor(seconds / interval.seconds);
    if (count >= 1) {
      const label = getPlural(count, interval.label);
      return `${count} ${label} назад`;
    }
  }

  return 'только что';
}

const dateAgo = ref(timeAgo(props.timeline.published_at));

</script>



<style scoped>
.group:last-child .h-8 {
  display: none;
}
</style>