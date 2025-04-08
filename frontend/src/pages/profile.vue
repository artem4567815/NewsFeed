<template>
  <div class="grid grid-flow-col xl:grid-cols-5">
    <div class="flex flex-col items-center col-span-4">
      <div class="w-10/12 h-10 flex border-b-3 border-gray-300">
        <div class="mr-12 pb-4 border-b-5 border-gray-400">Твои новости</div>
        <div class="mr-12 pb-4 border-b-5 border-gray-400">Черновик</div>
        <div class="mr-12 pb-4 border-b-5 border-gray-400">История хз</div>
      </div>
      <div v-for="post in posts" :key="post.news_id">
        <post-main :post="post" @click="$router.push('/post/id')" class="justify-self-center"></post-main>
      </div>
    </div>
  </div>
</template>

<script>
export default {

  beforeMount() {
    let token = localStorage.getItem('authToken');
    if (!token || token === 'undefined') {
      this.$router.push('/auth');
    }
  },
}
</script>

<style lang="scss" scoped>

</style>