<template>
  <div class="circuitDrawing">
    <img
      :src="defaultQasmCircuitRoute"
      alt="circuitDrawing"
      id="circuitDrawing"
      class="circutDrawing-image responsive"
    />
  </div>
</template>
<!-- ========================================================== -->
<script>
import {defaultQasmCircuitRoute} from './../data/routes'
export default {
  data() {
    return {
      defaultQasmCircuitRoute:defaultQasmCircuitRoute
    }
  },
};
</script>
<!-- ========================================================== -->
<style scoped>

.circuitDrawing-image {

  height: auto;
  width: auto;

}
</style>
