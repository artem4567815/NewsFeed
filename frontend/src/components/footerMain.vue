<template>
  <footer class="bg-white border-t border-gray-100">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
        <!-- О проекте -->
        <div class="space-y-4">
          <h3 class="text-lg font-bold text-gray-900">О проекте</h3>
          <p class="text-gray-600 text-sm leading-relaxed">
            EduFeed - это платформа для публикации и обмена новостями в образовательной сфере. Мы стремимся сделать информацию доступной и полезной.
          </p>
        </div>

        <!-- Навигация -->
        <div class="space-y-4">
          <h3 class="text-lg font-bold text-gray-900">Навигация</h3>
          <ul class="space-y-2">
            <li>
              <a href="#" class="text-gray-600 hover:text-blue-600 transition-colors text-sm">Главная</a>
            </li>
            <li>
              <a href="#" class="text-gray-600 hover:text-blue-600 transition-colors text-sm">Новости</a>
            </li>
            <li>
              <a href="#" class="text-gray-600 hover:text-blue-600 transition-colors text-sm">Стенгазеты</a>
            </li>
            <li>
              <a href="#" class="text-gray-600 hover:text-blue-600 transition-colors text-sm">Поиск команды</a>
            </li>
          </ul>
        </div>

        <!-- Категории -->
        <div class="space-y-4">
          <h3 class="text-lg font-bold text-gray-900">Категории</h3>
          <ul class="space-y-2">
            <li>
              <a href="#" class="text-gray-600 hover:text-blue-600 transition-colors text-sm">Технологии</a>
            </li>
            <li>
              <a href="#" class="text-gray-600 hover:text-blue-600 transition-colors text-sm">Наука</a>
            </li>
            <li>
              <a href="#" class="text-gray-600 hover:text-blue-600 transition-colors text-sm">Культура</a>
            </li>
            <li>
              <a href="#" class="text-gray-600 hover:text-blue-600 transition-colors text-sm">Спорт</a>
            </li>
          </ul>
        </div>

        <!-- Контакты -->
        <div class="space-y-4">
          <h3 class="text-lg font-bold text-gray-900">Контакты</h3>
          <ul class="space-y-2">
            <li class="flex items-center text-gray-600 text-sm">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              support@edufeed.com
            </li>
            <li class="flex items-center text-gray-600 text-sm">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
              </svg>
              +7 (999) 123-45-67
            </li>
          </ul>
          <!-- Социальные сети -->
          <div class="flex space-x-4 pt-2">
            <a href="#" class="text-gray-400 hover:text-blue-600 transition-colors">
              <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
              </svg>
            </a>
            <a href="#" class="text-gray-400 hover:text-blue-600 transition-colors">
              <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
              </svg>
            </a>
            <a href="#" class="text-gray-400 hover:text-blue-600 transition-colors">
              <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm4.995 17.176c-.42.116-.863.18-1.323.18-1.79 0-3.23-.68-4.32-2.043-.81 1.41-2.061 2.043-3.75 2.043-2.22 0-3.87-1.37-3.87-3.71 0-3.51 2.7-5.42 7.41-5.42h1.14v-.67c0-1.34-.87-2.07-2.55-2.07-1.44 0-2.46.6-3.06 1.8l-2.46-.96c.87-1.8 2.91-2.88 5.52-2.88 3.21 0 5.09 1.59 5.09 4.35v5.85c0 .99.39 1.44 1.17 1.44.36 0 .69-.09.99-.27v1.8zm-5.43-3.63v-1.8h-.99c-2.52 0-3.75.78-3.75 2.31 0 1.08.81 1.62 2.01 1.62 1.47 0 2.73-.84 2.73-2.13z"/>
              </svg>
            </a>
          </div>
        </div>
      </div>

      <!-- Копирайт -->
      <div class="pt-8 mt-8 border-t border-gray-100 text-center">
        <p class="text-sm text-gray-500">© 2024 EduFeed. Все права защищены.</p>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'footer-main'
}
</script>