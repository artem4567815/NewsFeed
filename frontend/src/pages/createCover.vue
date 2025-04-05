<template>
  <div class="max-w-6xl mx-auto">
    <h1 class="text-3xl font-bold text-center mb-6">Vue Paint</h1>

    <!-- Toolbar -->
    <div class="bg-white rounded-lg shadow-md p-4 mb-4 flex flex-wrap gap-4 items-center">
      <div class="flex items-center gap-2">
        <label class="font-medium">Tool:</label>
        <select v-model="currentTool" class="border rounded px-2 py-1" @change="changeTool">
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

      <div class="flex items-center gap-2">
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
      <canvas id="canvas" width="960" height="540"></canvas>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      currentTool: 'select',
      currentColor: '#000000',
      brushSize: 5,
      lastPosX: 0,
      lastPosY: 0,
      line: null,
      circle: null,
      rectangle: null,
      isDrawing: false,
      canvasConfig: {
        width: 960,
        height: 540,
        backgroundColor: 'white'
      }
    }
  },
  computed: {
    isDrawingTool() {
      return ['pencil', 'brush', 'eraser'].includes(this.currentTool);
    },
    isShapeTool() {
      return ['line', 'rectangle', 'circle'].includes(this.currentTool);
    }
  },
  mounted() {
    this.initCanvas();
    this.setupEventListeners();
  },
  methods: {
    initCanvas() {
      this.canvas = new fabric.Canvas('canvas', {
        width: this.canvasConfig.width,
        height: this.canvasConfig.height,
        fireRightClick: true, 
        fireMiddleClick: true, 
        stopContextMenu: true,
        preserveObjectStacking: true,
        isDrawingMode: false
      });

      this.canvas.setBackgroundColor(this.canvasConfig.backgroundColor, this.canvas.renderAll.bind(this.canvas));
      this.changeTool();
    },

    changeTool() {
      this.canvas.isDrawingMode = this.isDrawingTool;
      this.canvas.selection = this.currentTool === 'select';
      
      if (this.isDrawingTool) {
        if (this.currentTool === 'eraser') {
          this.canvas.freeDrawingBrush = new fabric.EraserBrush(this.canvas);
          this.canvas.freeDrawingBrush.width = this.brushSize;
        } else {
          this.canvas.freeDrawingBrush = new fabric.PencilBrush(this.canvas);
          this.canvas.freeDrawingBrush.color = this.currentColor;
          this.canvas.freeDrawingBrush.width = this.brushSize;
          
          if (this.currentTool === 'brush') {
            this.canvas.freeDrawingBrush.decimate = 2;
          }
        }
      }
    },

    setupEventListeners() {
      this.canvas.on('mouse:down', this.handleMouseDown);
      this.canvas.on('mouse:move', this.handleMouseMove);
      this.canvas.on('mouse:up', this.handleMouseUp);
    },

    handleMouseDown(e) {
      if (this.isShapeTool) {
        const pointer = this.canvas.getPointer(e.e);
        this.lastPosX = pointer.x;
        this.lastPosY = pointer.y;
        this.createShape(pointer);
      }
    },

    createShape(pointer) {
      this.isDrawing = true;
      const shapeConfig = {
        stroke: this.currentColor,
        strokeWidth: this.brushSize,
        fill: this.currentTool === 'text' ? this.currentColor : 'transparent',
        selectable: true,
        hasControls: true,
        hasBorders: true
      };

      switch (this.currentTool) {
        case 'line':
          this.line = new fabric.Line([pointer.x, pointer.y, pointer.x, pointer.y], shapeConfig);
          this.canvas.add(this.line);
          break;
        case 'rectangle':
          this.rectangle = new fabric.Rect({
            left: pointer.x,
            top: pointer.y,
            width: 0,
            height: 0,
            ...shapeConfig
          });
          this.canvas.add(this.rectangle);
          break;
        case 'circle':
          this.circle = new fabric.Circle({
            left: pointer.x,
            top: pointer.y,
            radius: 0,
            ...shapeConfig
          });
          this.canvas.add(this.circle);
          break;
      }
    },

    handleMouseMove(e) {
      if (!this.isDrawing || !this.isShapeTool) return;

      const pointer = this.canvas.getPointer(e.e);
      this.updateShape(pointer);
    },

    updateShape(pointer) {
      switch (this.currentTool) {
        case 'line':
          this.line.set({ x2: pointer.x, y2: pointer.y });
          break;
        case 'rectangle':
          this.updateRectangle(pointer);
          break;
        case 'circle':
          this.updateCircle(pointer);
          break;
      }
      this.canvas.renderAll();
    },

    updateRectangle(pointer) {
      const width = pointer.x - this.lastPosX;
      const height = pointer.y - this.lastPosY;
      this.rectangle.set({
        width: Math.abs(width),
        height: Math.abs(height),
        left: width > 0 ? this.lastPosX : pointer.x,
        top: height > 0 ? this.lastPosY : pointer.y
      });
    },

    updateCircle(pointer) {
      const radius = Math.sqrt(
        Math.pow(pointer.x - this.lastPosX, 2) + 
        Math.pow(pointer.y - this.lastPosY, 2)
      ) / 2;
      this.circle.set({ 
        radius,
        left: this.lastPosX,
        top: this.lastPosY
      });
    },

    handleMouseUp() {
      this.isDrawing = false;
    },

    addText() {
      const text = new fabric.Textbox('Введите текст', {
        left: 100,
        top: 100,
        fontSize: 20,
        fill: this.currentColor,
        borderColor: 'blue',
        editable: true,
        padding: 10,
        hasControls: true
      });

      this.canvas.add(text);
      text.enterEditing();
      text.selectAll();
    },

    clearCanvas() {
      this.canvas.clear();
      this.canvas.setBackgroundColor(this.canvasConfig.backgroundColor);
      this.canvas.renderAll();
    },

    downloadImage() {
      const dataURL = this.canvas.toDataURL({
        format: 'png',
        quality: 1
      });
      const link = document.createElement('a');
      link.download = 'canvas-image.png';
      link.href = dataURL;
      link.click();
    },

    triggerFileInput() {
      this.$refs.fileInput.click();
    },

    handleImageUpload(e) {
      const file = e.target.files[0];
      if (!file) return;

      const reader = new FileReader();
      reader.onload = (event) => {
        fabric.Image.fromURL(event.target.result, (img) => {
          const canvasWidth = this.canvas.width;
          const canvasHeight = this.canvas.height;
          const maxWidth = canvasWidth * 0.8;
          const maxHeight = canvasHeight * 0.8;
          
          const scale = Math.min(
            maxWidth / img.width,
            maxHeight / img.height
          );
          
          img.set({
            left: (canvasWidth - img.width * scale) / 2,
            top: (canvasHeight - img.height * scale) / 2,
            scaleX: scale,
            scaleY: scale,
            selectable: true,
            hasControls: true
          });
          
          this.canvas.add(img);
          this.canvas.setActiveObject(img);
        });
      };
      reader.readAsDataURL(file);
      e.target.value = '';
    }
  },
  watch: {
    currentColor() {
      this.changeTool();
    },
    brushSize() {
      if (this.isDrawingTool) {
        this.canvas.freeDrawingBrush.width = this.brushSize;
      }
    }
  }
}
</script>

<style scoped>
canvas {
  width: 100% !important;
  height: auto !important;
  aspect-ratio: 16/9;
  border: 1px solid #ddd;
}
</style>