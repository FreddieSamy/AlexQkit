<template>
  <div class="trash">
    <div v-if="!this.$parent.circuitDrawingFlag" class="add-remove-wire">
      <button class="add-wire" @click="addWire">+</button>
      <button class="remove-wire" @click="removeWire">-</button>
    </div>

    <div class="trashArea">
      <draggable :list="list" class="trash-drop-area" group="gates" @add="add">
        Trash Drop Area
        <div
          class="circuit-gate"
          v-for="element in list"
          :key="element.id"
          :id="element.name"
        >{{ element.name }}</div>
      </draggable>
    </div>
  </div>
</template>
<!-- =============================================================  -->
<script>
import draggable from "vuedraggable";
import { mapState, mapGetters } from "vuex";

export default {
  name: "Trash",
  display: "Trash",
  components: {
    draggable
  },
  data() {
    return {
      list: []
    };
  },
  computed: {
    ...mapState(["jsonObject"]),
    ...mapGetters(["liveResults"])
  },

  methods: {
    add: function(evt) {
      if (evt.from.classList != "toolbox-gates-area") {
        var wire = evt.from.id.replace("list", "");
        this.$parent.$refs.wire[wire - 1].addGateByIndex(evt.oldIndex);
      }
      this.list = [];
    },
    addWire: function() {
      this.jsonObject.wires++;
      this.$parent.$refs.tracingLine.updateTracingLine();
      this.jsonObject.init.push("0");
      this.liveResults.probabilities.push(0);
    },
    removeWire: function() {
      this.jsonObject.wires = Math.max(0, this.jsonObject.wires - 1);
      this.jsonObject.init.pop();
      this.jsonObject.rows.pop();
      this.liveResults.probabilities.pop();
      this.$parent.$refs.tracingLine.updateTracingLine();
    }
  }
};
</script>
<!-- =============================================================  -->
<style scoped>
.trash {
  display: flex;
  flex-wrap: nowrap;
  margin: 0px 10px 0px 2px;
  justify-content: flex-start;
  align-items: flex-start;
}
.add-remove-wire {
  display: flex;
  flex-wrap: nowrap;
  flex-basis: 4%;
}
.add-remove-wire button {
  background: white;
  border-radius: 7px;
  padding: 0px;
  flex-basis: 50%;
  margin: 2px 5px 0px 0px;
  border: 2px solid grey;
  font-weight: bolder;
}
.trashArea {
  color: #ef9494;
  border: 0.1em dashed #ef9494;
  border-radius: 0.2em;
  display: block;
  margin: 0em 0em 0em 0em;
  padding: 0.1em;
  text-align: center;
  flex-basis: 96%;
}
</style>
