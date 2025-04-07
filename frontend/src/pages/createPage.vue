<template>
  <header-main></header-main>

  <p class="text-3xl my-0 font-bold w-full text-center h-15 bg-black/10">Создание поста</p>
  <form @submit.prevent="submitForm" class="flex flex-col justify-center items-center text-nowrap">
    <div class="transition-transform bg-white duration-300 ease-out flex-col md:flex-row p-5 shadow-xl mt-11 flex w-90/100 justify-between rounded-2xl items-center">
      <div class="flex flex-col items-center text-pretty mb-5 md:mb-0">
        <p class="text-xl text-gray-600">Тут будет ник автора</p>
        <div class="text-2xl my-3 font-bold flex sm:flex-row flex-col">
          <div>
            <label for="NewsName" class="block text-sm font-medium text-gray-900">Название новости</label>
            <div class="mt-2">
              <input v-model="postNew.title" type="text" name="NewsName" id="NewsName" required class="block w-full text-2xl rounded-md bg-white px-3 py-1.5 text-gray-900 outline-1 outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:outline-offset-2 focus:outline-indigo-600">
            </div>
          </div>
          <p class="sm:mt-8.5 mt-3 ml-5 mr-5 text-nowrap">Дата выкладывания</p>
        </div>
        <div>
          <label for="shortDesc" class="block text-sm font-medium text-gray-900">Краткое описание</label>
          <div class="mt-2">
            <input v-model="postNew.short_content" type="text" name="shortDesc" id="shortDesc" required class="block w-full text-2xl rounded-md bg-white px-3 py-1.5 text-gray-900 outline-1 outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:outline-offset-2 focus:outline-indigo-600">
          </div>
        </div>
      </div>

      <div class="aspect-video aspect-16/9 max-h-120 md:max-w-6/12 w-full max-w-full bg-gray-200 hover:bg-gray-300 border-2 border-black rounded-lg flex justify-center items-center cursor-pointer" @click.stop="triggerFileInput">
        <input ref="imageInput" type="file" accept="image/*" class="hidden" @change="handleImageUpload" />
        <div class="flex flex-col items-center text-nowrap">
          <p class="text-center text-gray-600">Загрузите изображение</p>
          или
          <button @click.stop @click="$router.push('/Profile/Create/Cover')" class="bg hover:cursor-pointer bg-blue-500 ring-4 ring-transparent mt-1 hover:ring-blue-700/30 hover:bg-blue-600 transition ease-in-out rounded-2xl text-white px-3 py-1">Создайте свое</button>
        </div>
      </div>
    </div>

    <div class="w-full max-w-90/100">
      <label for="Desc" class="block text-sm font-medium text-gray-900">Описание</label>
      <div class="mt-2">
        <input v-model="postNew.content" type="text" name="Desc" id="Desc" required class="block w-full text-2xl rounded-md bg-white px-3 py-1.5 text-gray-900 outline-1 outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:outline-offset-2 focus:outline-indigo-600">
      </div>
    </div>

    <div class="w-full max-w-90/100 mt-4">
      <label for="time" class="block text-sm font-medium text-gray-900">Дата окончания</label>
      <div class="mt-2">
        <input v-model="postNew.end_date" type="date" name="time" id="time" required class="block w-full text-2xl rounded-md bg-white px-3 py-1.5 text-gray-900 outline-1 outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:outline-offset-2 focus:outline-indigo-600">
      </div>
    </div>

    <button type="submit" class="hover:cursor-pointer bg-blue-500 ring-4 hover:ring-blue-700/30 hover:bg-blue-600 transition ring-transparent ease-in-out rounded-2xl mt-3 text-white px-7 py-3">Принять и создать описание</button>
  </form>
</template>

<script>
import { ref, onMounted } from "vue";
import VanillaTilt from "vanilla-tilt";
import { jwtDecode } from "jwt-decode";

export default {
  data() {
    return {
      postNew: {
        title: "",
        type: "news",
        content: "",
        short_content: "",
        start_date: "",
        end_date: "",
        post_img: null,
        post_img_detail: ""
      }
    }
  },
  beforeMount() {
    let token = localStorage.getItem('authToken');
    const decoded = jwtDecode(token);
    if (!token || !decoded['is_admin']) {
      this.$router.push('/auth');
    }
  },
  methods: {
    convertToTimestamp(dateString, time = "00:00:00") {
      if (!dateString) return null;
      const [year, month, day] = dateString.split('-');
      const [hours, minutes, seconds] = time.split(':');

      const date = new Date(
          Date.UTC(
              parseInt(year),
              parseInt(month) - 1, // Месяцы в JS начинаются с 0
              parseInt(day),
              parseInt(hours),
              parseInt(minutes),
              parseInt(seconds)
          ));

      return date.getTime();
    },
    async refreshToken() {
      const response = await fetch('http://localhost:5000/auth/refresh', {
          method: 'POST',
          credentials: 'include'
      });
      if (response.status === 401) {
        return "Not Auth"
      }
      const data = await response.json();
      localStorage.setItem('access', data.access);
    },

    async submitForm() {
      try {
        this.postNew.start_date = 795683520000;
        this.postNew.end_date = this.convertToTimestamp(this.postNew.end_date);
        console.log(this.postNew.post_img)
        const response = await fetch('http://127.0.0.1:8080/admin/create/post', {
          method: 'POST',
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem("authToken")}`,
          },
          body: JSON.stringify(this.postNew)
        });

        if (response.status === 401) {
            let ans = await refreshToken();
            if (ans === "Not Auth"){
              return "User not auth"
            }
            return submitForm();
        }

        const data = await response.json();
        console.log('Post created:', data);
        this.$router.push('/Profile/Create');
      } catch (error) {
        console.error('Error creating post:', error);
      }
    },


    handleImageUpload(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => {
          this.postNew.post_img = reader.result;
        };
      }
    }
  },
  setup() {
    const card = ref(null);
    const imageInput = ref(null);

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

    const triggerFileInput = () => {
      if (imageInput.value) {
        imageInput.value.click();
      }
    };

    return {
      card,
      imageInput,
      triggerFileInput
    };
  }
}
</script>

<style lang="scss" scoped>
</style>