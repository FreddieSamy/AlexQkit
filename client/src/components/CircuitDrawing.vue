<template>
  <div class="circuitDrawing">
    <img :src="defaultQasmCircuitRoute" alt="circuitDrawing" id="circuitDrawing" />
  </div>
</template>
<!-- ========================================================== -->
<script>
import { defaultQasmCircuitRoute } from "./../data/routes";
export default {
  data() {
    return {
      defaultQasmCircuitRoute: defaultQasmCircuitRoute
    };
  }
};
</script>
<!-- ========================================================== -->
<style scoped>
#circuitDrawing {
  width: 100%;
}
</style>
