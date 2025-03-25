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
      tempShape: null
    }
  },
  computed: {
    isTextTool() {
      return this.currentTool === 'text';
    }
  },
  mounted() {
    this.initCanvas();
    window.addEventListener('resize', this.handleResize);

    // Test image load after initialization
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
        selection: true,
        preserveObjectStacking: true
      });

      // Убираем backstoreOnly, так как размеры уже установлены
      this.canvas.setDimensions({ width, height });
      this.setupEventListeners();
    },

    handleResize() {
      const container = this.$refs.canvas.parentElement;
      const canvasEl = this.$refs.canvas;

      // Пересчитываем размеры
      const width = container.clientWidth;
      const height = Math.floor(width * 9 / 16);

      // Обновляем физические размеры
      canvasEl.width = width;
      canvasEl.height = height;

      // Обновляем размеры в Fabric
      this.canvas.setDimensions({ width, height });
      this.canvas.requestRenderAll();
    },

    setupEventListeners() {
      this.canvas.on('mouse:down', (options) => {
        if (this.currentTool === 'select') return;
        if (this.currentTool === 'text') {
          const pointer = this.canvas.getPointer(options.e);
          this.addTextAtPosition(pointer.x, pointer.y);
          return;
        }

        this.isDrawing = true;
        const pointer = this.canvas.getPointer(options.e);
        this.startPos = {x: pointer.x, y: pointer.y};

        if (['pencil', 'brush', 'eraser'].includes(this.currentTool)) {
          this.startFreehand(pointer.x, pointer.y);
        }
      });

      this.canvas.on('mouse:move', (options) => {
        if (!this.isDrawing || this.currentTool === 'select') return;

        const pointer = this.canvas.getPointer(options.e);

        switch (this.currentTool) {
          case 'pencil':
          case 'brush':
          case 'eraser':
            this.continueFreehand(pointer.x, pointer.y);
            break;
          case 'line':
            this.drawTempLine(pointer.x, pointer.y);
            break;
          case 'rectangle':
            this.drawTempRect(pointer.x, pointer.y);
            break;
          case 'circle':
            this.drawTempCircle(pointer.x, pointer.y);
            break;
        }
      });

      this.canvas.on('mouse:up', () => {
        if (!this.isDrawing) return;
        this.finalizeDrawing();
      });
    },

    startFreehand(x, y) {
      this.freehandPath = new fabric.Path(`M ${x} ${y}`, {
        stroke: this.currentTool === 'eraser' ? 'white' : this.currentColor,
        strokeWidth: this.brushSize,
        fill: null,
        selectable: false
      });
      this.canvas.add(this.freehandPath);
    },

    continueFreehand(x, y) {
      if (!this.freehandPath) return;
      this.freehandPath.path.push(['L', x, y]);
      this.freehandPath.set({dirty: true});
      this.canvas.requestRenderAll();
    },

    drawTempLine(x, y) {
      if (this.tempShape) this.canvas.remove(this.tempShape);

      this.tempShape = new fabric.Line([
        this.startPos.x, this.startPos.y,
        x, y
      ], {
        stroke: this.currentColor,
        strokeWidth: this.brushSize,
        selectable: false
      });

      this.canvas.add(this.tempShape);
    },

    drawTempRect(x, y) {
      if (this.tempShape) this.canvas.remove(this.tempShape);

      const width = x - this.startPos.x;
      const height = y - this.startPos.y;

      this.tempShape = new fabric.Rect({
        left: this.startPos.x,
        top: this.startPos.y,
        width: width,
        height: height,
        stroke: this.currentColor,
        strokeWidth: this.brushSize,
        fill: 'transparent',
        selectable: false
      });

      this.canvas.add(this.tempShape);
    },

    drawTempCircle(x, y) {
      if (this.tempShape) this.canvas.remove(this.tempShape);

      const radius = Math.sqrt(
          Math.pow(x - this.startPos.x, 2) +
          Math.pow(y - this.startPos.y, 2)
      );

      this.tempShape = new fabric.Circle({
        left: this.startPos.x,
        top: this.startPos.y,
        radius: radius,
        stroke: this.currentColor,
        strokeWidth: this.brushSize,
        fill: 'transparent',
        selectable: false
      });

      this.canvas.add(this.tempShape);
    },

    finalizeDrawing() {
      if (!this.isDrawing) return;
      this.isDrawing = false;

      switch (this.currentTool) {
        case 'pencil':
        case 'brush':
        case 'eraser':
          if (this.freehandPath) {
            this.freehandPath.set({selectable: true});
            this.freehandPath = null;
          }
          break;
        case 'line':
        case 'rectangle':
        case 'circle':
          if (this.tempShape) {
            this.tempShape.set({selectable: true});
            this.tempShape = null;
          }
          break;
      }

      this.canvas.requestRenderAll();
    },

    addText() {
      this.addTextAtPosition(100, 100);
    },

    addTextAtPosition(x, y) {
      const text = new fabric.Textbox('Click to edit', {
        left: x,
        top: y,
        fontSize: 20,
        fill: this.currentColor,
        width: 200,
        editable: true,
        hasControls: true
      });

      this.canvas.add(text);
      this.canvas.setActiveObject(text);
      text.enterEditing();
    },

    triggerFileInput() {
      this.$refs.fileInput.click();
    },


    readFileAsDataURL(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => {
          if (!reader.result.startsWith('data:image')) {
            reject(new Error('Invalid image format'));
            return;
          }
          resolve(reader.result);
        };
        reader.onerror = () => reject(new Error('File reading failed'));
        reader.readAsDataURL(file);
      });
    },

    async addImageToCanvas(imageData) {
      try {
        const img = await fabric.Image.fromURL(imageData, {
          crossOrigin: 'Anonymous',
          enableRetinaScaling: false
        });

        // Настройки изображения
        img.set({
          left: this.canvas.width / 2,
          top: this.canvas.height / 2,
          originX: 'center',
          originY: 'center',
          selectable: true,
          editable: true,
          hasControls: true,
          cornerSize: 20,
          borderColor: 'red'
        });

        // Автомасштабирование
        const scale = Math.min(
            this.canvas.width * 0.8 / img.width,
            this.canvas.height * 0.8 / img.height,
            1
        );

        img.scale(scale);

        this.canvas.add(img);
        this.canvas.setActiveObject(img);
        this.canvas.requestRenderAll();

        return img;
      } catch (error) {
        console.error('Ошибка загрузки изображения:', error);
        throw error;
      }
    },

    async handleImageUpload(e) {
      try {
        const file = e.target.files[0];
        if (!file) return;

        const url = URL.createObjectURL(file);
        await this.addImageToCanvas(url);
        URL.revokeObjectURL(url);
        this.$refs.fileInput.value = '';

        // Переключаем инструмент обратно на выбор
        this.currentTool = 'select';
      } catch (error) {
        console.error('Ошибка загрузки:', error);
        alert('Не удалось загрузить изображение');
      }
    },


    clearCanvas() {
      if (!this.canvas) return;
      this.canvas.clear();
      this.canvas.backgroundColor = 'white';
      this.canvas.renderAll();
    },

    downloadImage() {
      if (!this.canvas) return;
      const link = document.createElement('a');
      link.download = 'vue-paint.png';
      link.href = this.canvas.toDataURL({
        format: 'png',
        quality: 1
      });
      link.click();
    }
  },
  watch: {
    currentTool(newVal) {
      if (!this.canvas) return;
      this.canvas.selection = newVal === 'select';
      this.canvas.forEachObject(obj => {
        obj.selectable = newVal === 'select';
      });
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