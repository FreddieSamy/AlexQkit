<template>
  <div class="bloch-sphere-body">
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
div{
  margin:0px 100px 0px 0px;
}
.bloch-sphere {
  width: 2.5em;
  transition: transform 0.3s;
  border:0.3px solid black;
  border-radius:10px;
  margin:0px 0px -5px 0px;

}
.bloch-sphere:hover {

  position: fixed;
  z-index:20;
  transform: scale(5.5);
  
}
</style>