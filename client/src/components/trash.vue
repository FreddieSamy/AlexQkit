<template>
  <div class="trashArea">
    <draggable :list="list" class="trash-drop-area" group="gates" @add="add">
      Trash Drop Area
      <div
        class="circuit-gate"
        v-for="element in list"
        :key="element.id"
        :id="element.name"
      >
        {{ element.name }}
      </div>
      <!-- Trash Drop Area -->
    </draggable>
  </div>
</template>
<!-- =============================================================  -->
<script>
import draggable from "vuedraggable";
export default {
  name: "trash",
  display: "trash",
  components: {
    draggable,
  },
  data() {
    return {
      list: [],
    };
  },
  methods: {
    add: function(evt) {
      var wire = evt.from.id.replace("list","")
      this.$parent.$refs.wire[wire-1].addGateByIndex(evt.oldIndex);
      this.list = [];
    },
  },
};
0;
</script>
<!-- =============================================================  -->
<style scoped>
.trashArea {
  color: #ef9494;
  border: 0.1em dashed #ef9494;
  border-radius: 0.2em;
  display: block;
  margin: 0.2em 0.2em 0em 0.2em;
  padding: 0.1em 0.5em 0.1em 0.5em;
  width: 97%;
  text-align: center;
}
.circuit-gate {
  color: white;
  /*text-align: center;*/
  line-height: 2.5em;
  border: 0.15em solid black;
  border-radius: 0.7em;
  display: inline-block;
  margin: 0.8em 0.5em 0.5em 0.5em;
  padding: 0em 0em 0em 0em;
  width: 2.5em;
  height: 2.5em;
  background-color: #5d6d7e;
  z-index: 2;
}
</style>
