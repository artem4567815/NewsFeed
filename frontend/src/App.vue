<template>
  <div class="app"></div>
  <header-main class="z-100"/>
  <Transition
      name="fade-slide"
      mode="out-in"
  >
    <router-view />
  </Transition>

</template>

<script>
export default {

}
</script>

<style>
.fade-slide-leave-active {
  position: absolute;
  width: 100%;
  transition: all 0.4s ease;
}
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
.fade-slide-enter-active {
  transition: all 0.4s ease;
}
.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(10px);
}
</style>