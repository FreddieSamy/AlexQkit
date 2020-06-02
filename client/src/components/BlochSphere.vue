<template>
  <div>
    <img
      class="bloch-sphere"
      :src="defaultBlochSphereRoute"
      alt
      :id="'bloch-sphere-'+this.$parent.id"
    />
  </div>
</template>
<!-- =============================================================  -->

<script>
import { defaultBlochSphereRoute } from "./../data/routes";

export default {
  name: "BlochSphere",
  display: "BlochSphere",
  data() {
    return {
      defaultBlochSphereRoute: defaultBlochSphereRoute
    };
  },
  mounted() {}
};
</script>
<!-- =============================================================  -->

<style scoped>
.bloch-sphere {
  width: 2.5em;
  transition: transform 0.1s;
  border:0.3px solid black;
  border-radius:10px;

}
.bloch-sphere:hover {
  position: fixed;
  z-index:2;
  transform: scale(5.5);
  
}
</style>