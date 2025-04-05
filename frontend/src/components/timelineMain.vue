<template>
    <div class="flex justify-self-start">
        <div class="flex flex-col items-center mr-4">
            <div class="w-6 h-6 border-3 border-black rounded-xs"></div>
            <div class="my-1 mx-0 w-0.5 h-11 bg-gray-400"></div>
            <div class="w-0.5 h-3 bg-gray-400"></div>
        </div>
        <div class="time-text text">
            <p class="time-name text">
                <b>Название новости</b>
            </p>
            <p class="time-valid text">
                от 12.12.2024 до 12.01.2025
            </p>
            <p class="time-passed" id="time-passed" >
                4 дня назад
            </p>
        </div>
    </div>
</template>

<script>
export default {
      name: 'timeline-main'
    }
</script>

<style lang="scss" scoped>

</style>