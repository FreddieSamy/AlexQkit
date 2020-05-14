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
}

.bloch-sphere:hover {
  transform: scale(2.5);
}
</style>