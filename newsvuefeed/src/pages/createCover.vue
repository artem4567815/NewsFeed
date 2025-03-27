<template>
  <div class="max-w-6xl mx-auto">
    <h1 class="text-3xl font-bold text-center mb-6">Vue Paint</h1>

    <!-- Toolbar -->
    <div class="bg-white rounded-lg shadow-md p-4 mb-4 flex flex-wrap gap-4 items-center">
      <div class="flex items-center gap-2">
        <label class="font-medium">Tool:</label>
        <select v-model="currentTool" class="border rounded px-2 py-1">
          <option value="select">Select/Move</option>
          <option value="pencil">Pencil</option>
          <option value="brush">Brush</option>
          <option value="eraser">Eraser</option>
          <option value="line">Line</option>
          <option value="rectangle">Rectangle</option>
          <option value="circle">Circle</option>
          <option value="text">Text</option>
        </select>
      </div>

      <div class="flex items-center gap-2">
        <label class="font-medium">Color:</label>
        <input type="color" v-model="currentColor" class="w-8 h-8 cursor-pointer">
      </div>

      <div class="flex items-center gap-2" v-if="!isTextTool">
        <label class="font-medium">Size:</label>
        <input type="range" v-model="brushSize" min="1" max="50" class="w-24">
        <span>{{ brushSize }}px</span>
      </div>

      <button @click="clearCanvas" class="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600">
        Clear
      </button>

      <button @click="downloadImage" class="bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600">
        Save
      </button>

      <button @click="addText" class="bg-green-500 text-white px-3 py-1 rounded hover:bg-green-600">
        Add Text
      </button>

      <button @click="triggerFileInput" class="bg-purple-500 text-white px-3 py-1 rounded hover:bg-purple-600">
        Add Image
      </button>
      <input
          type="file"
          ref="fileInput"
          accept="image/*"
          style="display: none;"
          @change="handleImageUpload"
      >
    </div>

    <!-- Canvas Container -->
    <div class="bg-white rounded-lg shadow-md p-4 relative">
      <canvas
          ref="canvas"
          class="border border-gray-300 w-full touch-none"
      ></canvas>
    </div>
  </div>
</template>

<script>
import * as fabric from 'fabric';
import { jwtDecode } from "jwt-decode";

export default {
  data() {
    return {
      currentTool: 'select',
      currentColor: '#000000',
      brushSize: 5,
      canvas: null,
      isDrawing: false,
      startPos: { x: 0, y: 0 },
      freehandPath: null,
      tempShape: null,
      drawingOptions: {
        color: '#000000', // Цвет карандаша
        lineWidth: 5,     // Толщина линии
        shadowColor: '#888888', // Цвет тени
        shadowWidth: 0,   // Ширина тени
        shadowOffset: 0,  // Смещение тени
      },
    }
  },
  computed: {
    isTextTool() {
      return this.currentTool === 'text';
    }
  },
  beforeMount() {
    let token = localStorage.getItem('authToken');
    const decoded = jwtDecode(token);
    if (!token || !decoded['is_admin']) {
      this.$router.push('/auth');
    }
  },
  mounted() {
    this.initCanvas();
    window.addEventListener('resize', this.handleResize);

  },
  beforeDestroy() {
    window.removeEventListener('resize', this.handleResize);
    if (this.canvas) {
      this.canvas.dispose();
    }
  },
  methods: {
    initCanvas() {
      const container = this.$refs.canvas.parentElement;
      const canvasEl = this.$refs.canvas;

      // Получаем реальные размеры контейнера
      const width = container.clientWidth;
      const height = Math.floor(width * 9 / 16);

      // Устанавливаем физические размеры canvas
      canvasEl.width = width;
      canvasEl.height = height;

      this.canvas = new fabric.Canvas(canvasEl, {
        backgroundColor: 'white',
        selection: true
      });

      // Убираем backstoreOnly, так как размеры уже установлены
      this.canvas.setDimensions({ width, height });
      this.setupEventListeners();
    },
    setupDrawingOptions() {
      const brush = this.canvas.freeDrawingBrush;
      console.log(this.drawingOptions.color)
      brush.color = "#000000";
      brush.width = this.drawingOptions.lineWidth;
      brush.shadow = new fabric.Shadow({
        blur: this.drawingOptions.shadowWidth,
        offsetX: this.drawingOptions.shadowOffset,
        offsetY: this.drawingOptions.shadowOffset,
        affectStroke: true,
        color: this.drawingOptions.shadowColor,
      });
    },

    // Слушатели для изменения параметров рисования
    changeDrawingColor(color) {
      this.drawingOptions.color = color;
      this.canvas.freeDrawingBrush.color = color;
    },

    changeDrawingLineWidth(width) {
      this.drawingOptions.lineWidth = width;
      this.canvas.freeDrawingBrush.width = width;
    },

    changeDrawingShadowColor(color) {
      this.drawingOptions.shadowColor = color;
      this.canvas.freeDrawingBrush.shadow.color = color;
    },

    changeDrawingShadowWidth(width) {
      this.drawingOptions.shadowWidth = width;
      this.canvas.freeDrawingBrush.shadow.blur = width;
    },

    changeDrawingShadowOffset(offset) {
      this.drawingOptions.shadowOffset = offset;
      this.canvas.freeDrawingBrush.shadow.offsetX = offset;
      this.canvas.freeDrawingBrush.shadow.offsetY = offset;
    },

    toggleDrawingMode() {
      this.canvas.isDrawingMode = !this.canvas.isDrawingMode;
      // Выводим актуальный текст для кнопки
      if (this.canvas.isDrawingMode) {
        console.log('Включен режим рисования');
      } else {
        console.log('Выключен режим рисования');
      }
    },
  },
  watch: {
    currentTool(newVal) {
      if (!this.canvas) return;
      this.canvas.selection = newVal === 'select';
      this.canvas.requestRenderAll();
    }
  }
}
</script>

<style scoped>
canvas {
  width: 100% !important;
  height: auto !important;
  aspect-ratio: 16/9;
}
</style>