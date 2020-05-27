<template>
  <div class="conditional-loop">
    <h1>Conditional Loop</h1>
    <div class="from-to">

   
     <input class="from" type="number" min="1" v-model="from" placeholder="from " /> :
     <input class="to" type="number" min="1" v-model="to" placeholder="to " />
      </div>
    <div class="select-wire" v-for="(item, index) in this.jsonObject.wires" :key="index">
      <label>Wire {{index+1}}</label>
      <select v-model="wiresChoosen[index]">
        <option value="*" selected>don't care</option>
        <option value="0">0</option>
        <option value="1">1</option>
      </select>
    </div>
  </div>
</template>
<!-- ================================================  -->
<script>
import { mapState, mapActions } from "vuex";
export default {
  name: "conditional",
  display: "conditional",

  data() {
    return {
      from: "",
      to: "",
      wiresChoosen: new Array(this.$parent.jsonObject.wires).fill("*")
    };
  },

  computed: {
    ...mapState(["jsonObject"])
  },
  methods: {
    ...mapActions(["addMessage"]),
    ...mapActions(["removeMessages"])
  }
};
</script>
<!-- ================================================  -->
<style scoped>
.conditional-loop {
  margin: 100px auto;
}
.from-to{
    margin: 30px;
}
.from-to input{
    width:50px;
    border-radius:5px;
}
.select-wire {
  margin: 30px;
}
</style>


