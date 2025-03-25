<template>
  <header-main></header-main>

  <p class="text-3xl my-0 font-bold w-full text-center h-15 bg-black/10"> Создание поста</p>
  <div class="flex flex-col justify-center items-center text-nowrap">
    <div class="transition-transform bg-white duration-300 ease-out flex-col md:flex-row  p-5 shadow-xl mt-11 flex w-90/100 justify-between rounded-2xl items-center">
      <div class="flex flex-col items-center text-pretty mb-5 md:mb-0">
        <p class="text-xl text-gray-600">Тут будет ник автора</p>
        <div class="text-2xl my-3 font-bold flex sm:flex-row flex-col">
          <div>
            <label for="email" class="block text-sm font-medium text-gray-900">Название новости</label>
            <div class="mt-2">
              <input type="email" name="email" id="email" autocomplete="email" required
                     class="block w-full text-2xl rounded-md bg-white px-3 py-1.5 text-gray-900 outline-1 outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:outline-offset-2 focus:outline-indigo-600">
            </div>
          </div>
          <p class="sm:mt-8.5 mt-3 ml-5 mr-5 text-nowrap">Дата выкладывания</p>
        </div>
        <div>
          <label for="email" class="block text-sm font-medium text-gray-900">Краткое описание</label>
          <div class="mt-2">
            <input type="email" name="email" id="email" autocomplete="email" required
                   class="block w-full text-2xl rounded-md bg-white px-3 py-1.5 text-gray-900 outline-1 outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:outline-offset-2 focus:outline-indigo-600">
          </div>
        </div>
      </div>

      <div
          class="aspect-video aspect-16/9 max-h-120 md:max-w-6/12 w-full max-w-full bg-gray-200 hover:bg-gray-300 border-2 border-black rounded-lg flex justify-center items-center cursor-pointer"
          @click.stop="triggerFileInput"
      >
        <input ref="imageInput" type="file" accept="image/*" class="hidden" @change="handleImageUpload" />
        <div class="flex flex-col items-center text-nowrap">
        <p class="text-center text-gray-600">Загрузите изображение</p>
        или
          <button @click.stop @click="$router.push('/Profile/Create/Cover')" class="bg hover:cursor-pointer bg-blue-500 ring-4 ring-transparent mt-1 hover:ring-blue-700/30 hover:bg-blue-600 transition ease-in-out rounded-2xl text-white px-3 py-1"  >Создайте свое</button>

        </div>
      </div>

    </div>
    <button @click="$router.push('/Profile/Create')" class="hover:cursor-pointer bg-blue-500 ring-4 hover:ring-blue-700/30 hover:bg-blue-600 transition ring-transparent ease-in-out rounded-2xl mt-3 text-white px-7 py-3" >Принять и создать описание</button>

  </div>


</template>

<script>
import { ref, onMounted } from "vue";
import VanillaTilt from "vanilla-tilt";

export default {
  name: "post-main",
  props: {
    post: Object
  },
  setup() {
    const card = ref(null);
    const imageInput = ref(null);

    // Инициализация эффекта наклона
    onMounted(() => {
      if (card.value) {
        VanillaTilt.init(card.value, {
          max: 3,
          speed: 4000,
          perspective: 1000,
          easing: "cubic-bezier(.03,.98,.52,.99)",
          scale: 1.02,
        });
      }
    });

    // Функция для активации проводника
    const triggerFileInput = () => {
      if (imageInput.value) {
        imageInput.value.click();
      }
    };

    // Функция для обработки выбранного изображения
    const handleImageUpload = (event) => {
      const file = event.target.files[0];
      if (file) {
        // Здесь можно обработать изображение (например, показать его на странице)
        console.log("Выбранное изображение:", file);
      }
    };

    return {
      card,
      imageInput,
      triggerFileInput,
      handleImageUpload
    };
  },
};
</script>

<style lang="scss" scoped>
</style>
