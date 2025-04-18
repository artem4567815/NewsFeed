<template>
  <span
      class="text-sm font-medium px-3 py-1 rounded-full border-transparent"
      :style="tagStyle"
  >
    {{ tag }}
  </span>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  tag: {
    type: String,
    required: true
  }
});

const tagColor = (tag) => {
  const hash = Array.from(tag).reduce((acc, char) => {
    return (acc << 5) - acc + char.charCodeAt(0);
  }, 0);
  const hue = Math.abs(hash) % 360;  // 0-359

  // Tailwind-подобные пастельные тона (S=20-30%, L=90-95%)
  const background = `hsl(${hue}, 100%, 84%)`;
  const color = `hsl(${hue}, 60%, 35%)`;

  return {
    backgroundColor: background,
    color: color
  };
};

const tagStyle = computed(() => tagColor(props.tag));
</script>