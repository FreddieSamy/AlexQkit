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
      if(evt.from.classList != 'toolbox-gates-area'){
      var wire = evt.from.id.replace("list","")
      this.$parent.$refs.wire[wire-1].addGateByIndex(evt.oldIndex);
      }
      this.list = [];
    }
  }
};
</script>
<!-- =============================================================  -->
<style scoped>
.trashArea {
  color: #ef9494;
  border: 0.1em dashed #ef9494;
  border-radius: 0.2em;
  display: block;
  margin: 0em 0em 0em 3.5em;
  padding: 0.1em 0.5em 0.1em 0.5em;
  width: 92%;
  text-align: center;
}

</style>
