<template>
  <div
      :class="['flex items-center px-3 py-2 rounded cursor-pointer', active ? 'bg-blue-100 text-blue-600' : 'hover:bg-gray-100']"
      @click="$emit('click')">
    <component :is="iconComponent" class="w-5 h-5 mr-3"/>
    <span>{{ text }}</span>
  </div>
</template>

<script setup>
import {computed} from 'vue'
import * as icons from 'lucide-vue-next'

const props = defineProps({
  icon: String,
  text: String,
  active: Boolean
})

const iconComponent = computed(() => icons[props.icon])
</script>