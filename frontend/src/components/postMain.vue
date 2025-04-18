<template>
  <div
      ref="card"
      class=" bg-white rounded-2xl shadow-lg overflow-hidden w-95/100 transition-transform duration-300 ease-out cursor-pointer"
  >
    <div class="flex flex-col lg:flex-row h-full">
      <!-- Изображение -->
      <div class="lg:w-[500px] relative overflow-hidden">
        <img
            :src="post.image_url"
            alt="Превью картинки"
            class="w-full aspect-16/9 lg:h-full object-cover"
        />
      </div>

      <!-- Контент -->
      <div class="flex-1 p-2 md:p-4 flex flex-col min-h-[350px] relative">
        <!-- Категория -->
        <div class="flex-1 mt-8 md:mt-6">
          <!-- Метаданные -->
          <div class="flex items-center space-y-1 space-x-4 mb-4">
            <div class="flex flex-col sm:flex-row space-x-3 sm:items-center">
            <span class="flex items-center text-sm font-medium text-gray-600">
              <CalendarDays class="w-4 h-4 mr-1.5 mb-1" />
              {{ timestampToDate(post.start_date) }} - {{ timestampToDate(post.end_date) }}
            </span>
            <span class="flex items-center text-sm font-medium text-gray-600">
              <Clock class="w-4  h-4 mr-1.5 mb-1" />
              {{ dateAgo }}
            </span>
            </div>
            <span class="px-3 py-1 h-fit ml-auto sm:ml-0 text-sm font-medium rounded-full bg-blue-100 text-blue-800">{{post.type}}</span>

          </div>


          <!-- Заголовок -->
          <h2 class="text-2xl font-bold text-gray-900 mb-4 leading-tight hover:text-blue-600 transition-colors duration-200">
            {{post.title}}
          </h2>

          <!-- Описание -->
          <p class="text-base text- text-gray-700 mb-6 leading-relaxed line-clamp-3">
            {{post.short_content}}
          </p>
        </div>
          <div class="flex items-center space-x-4 timeline-scroll overflow-x-auto mb-4">
            <tag-pill v-for="tag in post.tags" :key="tag" :tag="tag" class="bg-blue-600/20 text-blue-600  border-blue-600/40  border-1 px-3 py-1 rounded-full text-sm font-medium ">
              {{tag}}
            </tag-pill>
          </div>



        <!-- Нижняя часть -->
        <div class="flex items-center justify-between pt-4 border-t border-gray-100">
          <!-- Автор -->
          <div class="flex items-center">
            <img
                :src="post.author.avatar_url"
                class="w-12 h-12 rounded-full bg-gradient-to-r from-blue-500 to-blue-600 flex items-center justify-center text-white font-bold text-lg"
            />
            <div class="ml-3">
              <p class="text-base font-medium text-gray-900">{{post.author.login}}</p>
              <p class="text-sm text-gray-600">ТУТ БУДЕТ ШКОЛА И КОРПУС</p>
            </div>
          </div>

          <!-- Статистика -->
          <div class="flex items-center space-x-6">
            <button
                @click.stop="Like"
                class="flex items-center space-x-2 text-gray-500 hover:text-blue-600 transition-colors duration-200"
            >
              <Heart   />
              <span class="text-base font-medium">{{post.likes_count}}</span>
            </button>
            <button class="flex items-center text-base font-medium text-gray-600">
              <Eye class="mr-2.5" />
              {{post.views}}
            </button>
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
import { defineProps } from 'vue';
import {jwtDecode} from "jwt-decode";
import router from "@/router/router.js";

const props = defineProps({
  post: Object
});
const card = ref(null);

function timestampToDate(ts) {
  const date = new Date(ts * 1000); // если timestamp в секундах
  const day = String(date.getDate()).padStart(2, '0');
  const month = String(date.getMonth() + 1).padStart(2, '0'); // месяцы с 0
  const year = date.getFullYear();
  return `${day}.${month}.${year}`;
}

const timestamp = 1744576048;
const dateAgo = ref(timeAgo(timestamp));
let intervalId = null;

import api from '@/api/axios'
import { useRouter } from 'vue-router'
import axios from "axios";
import TagPill from "@/components/UI/tagPill.vue";

function Like() {
  const likePost = async () => {
    try {
      await api.post(`/posts/${props.post.post_id}/like`, {
        post_id: props.post.post_id,
        credentials: 'include' // 🔥 Критически важно для кук!
      },
    )
      props.post.likes_count++
    } catch (error) {
      console.error('Ошибка лайка:', error)
      // Можно добавить уведомление
    }
  }

  likePost()
}








setInterval(() => {
    dateAgo.value = timeAgo(timestamp);
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



onMounted(() => {
  if (card.value) {
    VanillaTilt.init(card.value, {
      max: 1, // Чуть больше, чтобы было естественно
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
