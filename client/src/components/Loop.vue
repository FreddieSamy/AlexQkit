<template>
  <div>
    <div>

    <select v-model="from">
    <option disabled selected>{{from}}</option>
    <option class="from" type="number" min="1" v-for="column in this.jsonObject.colsCount" :key="column">{{column}}</option>
    </select>

     <select v-model="to">
    <option disabled selected >{{to}}</option>
    <option class="to" type="number" min="1" v-for="column in this.jsonObject.colsCount" :key="column">{{column}}</option>
    </select>
      <input class="repeat" type="number" min="1" v-model="repeat" placeholder="Repeat" />
    </div>
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
      from: "FROM",
      to: "TO",
      repeat: "repeat",
    };
  },
    computed: {
    ...mapState(["jsonObject"])
  },
  methods :{
    ...mapActions(["addMessage"]),
    ...mapActions(["removeMessages"]),
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
.repeat{
  margin:0px 0px 0px 50px;
  width:60px;
}
</style>

