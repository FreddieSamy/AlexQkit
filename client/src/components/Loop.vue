<template>
  <div>
    <!-- select column to start (FROM)-->
    <select v-model="from">
      <option disabled selected>{{from}}</option>
      <option
        class="from"
        type="number"
        min="1"
        v-for="column in this.jsonObject.colsCount"
        :key="column"
      >{{column}}</option>
    </select>
    <!-- select column to end (TO)-->
    <select v-model="to">
      <option disabled selected>{{to}}</option>
      <option
        class="to"
        type="number"
        min="1"
        v-for="column in this.jsonObject.colsCount"
        :key="column"
      >{{column}}</option>
    </select>
    <!-- select Number of repetitions -->
    <input class="repeat" type="number" min="1" v-model="repeat" placeholder="Repeat" />
  </div>
</template>
<!-- ================================================  -->
<script>
import { mapState, mapActions } from "vuex";
// eslint-disable-next-line no-undef
export default {
  name: "Loop",
  display: "Loop",
  data() {
    return {
      from: "from",
      to: "to",
      repeat: null
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
option {
  padding: 0em 0em 0em 0.5em;
  width: 40px;
  border-radius: 5px;
  background: #f3f3f3;
}
select{
  margin: 5px;
  border-radius:5px;
}
.repeat {
  margin: 0px 0px 0px 50px;
  width: 60px;
  border-radius: 5px;
}
</style>

