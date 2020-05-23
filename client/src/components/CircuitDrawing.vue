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
  margin: -15px 0px 0px 0px;

  /* height:100px; */
  /* z-index: -10;
  width: 100%;
  margin: -80px 0px 0px 0px;
  padding: -10px 0px 0px 0px; */
}
</style>
