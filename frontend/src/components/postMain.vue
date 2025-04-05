<template> 
    <div ref="card" class="transition-transform bg-white duration-300 ease-out flex-col md:flex-row  p-5 shadow-xl mt-11 flex w-90/100 justify-between rounded-2xl items-center">
        <div class="flex flex-col items-center text-pretty mb-5 md:mb-0">
            <p class="text-xl text-gray-600">{{ post.author.name }}</p>
            <p class="text-2xl my-3 font-bold">{{ post.title }} · 13.10.28</p>
            <p class="text-xl text-gray-600">{{ post.short_content }}</p>
        </div>
        <img src="https://avatars.mds.yandex.net/get-mpic/5234525/img_id5188673678753414396.jpeg/orig" alt="картинка" class="aspect-16/9 max-h-120 md:max-w-6/12 rounded-lg"/>
    </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from "vue";
import VanillaTilt from "vanilla-tilt";

export default {
  name: "post-main",
  props: {
    post: Object
  },
  setup() {
    const card = ref(null);

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


    // onUnmounted(() => {
    //   if (card.value) {
    //     card.value.vanillaTilt.destroy();
    //   }
    // });

    return { card };
  },
};
</script>

<style lang="scss" scoped>
</style>
