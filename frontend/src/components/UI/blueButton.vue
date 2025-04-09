<template>
  <div>
    <button class="hover:cursor-pointer bg-blue-500 ring-4 ring-transparent hover:ring-blue-700/30 hover:bg-blue-600 transition ease-in rounded-2xl text-white px-3 py-2 " ><slot></slot></button>
  </div>
</template>

<script>
export default {
  name: 'blue-button'
}
</script>

<style lang="scss" scoped>

</style>