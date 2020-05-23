<template>
  <div class="messages">
    <p class="advanced" v-if="this.messages.advanced.length">Advanced : {{this.messages.advanced}}</p>
    <p class="alert" v-if="this.messages.alert.length">Alert:{{this.messages.alert}}</p>
    <p class="violations" v-if="this.messages.violation.length">violation:{{this.messages.violation}}</p>
    <p class="errors" v-if="this.messages.errors.length">Alert : {{this.messages.errors}}</p>
  </div>
</template>
<!-- ========================================================== -->
<script>
import { mapGetters } from "vuex";
export default {
  name: "MessageBox",
  display: "MessageBox",
  data() {
    return {};
  },
  computed: {
    ...mapGetters(["messages"])
  }
};
</script>
<!-- ========================================================== -->
<style scoped>
#circuitDrawing {
  margin: -15px 0px 0px 0px;
}
</style>
