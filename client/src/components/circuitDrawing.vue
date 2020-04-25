<template>
  <div class="circuitDrawing">
    <img
      :src="defaultqasmCircuitRoute"
      alt="circuitDrawing"
      id="circuitDrawing"
      class="circutDrawing-image responsive"
    />
  </div>
</template>
<!-- ========================================================== -->
<script>
import {defaultqasmCircuitRoute} from './../data/routes'
export default {
  data() {
    return {
      defaultqasmCircuitRoute:defaultqasmCircuitRoute
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
