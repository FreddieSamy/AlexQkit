<template>
  <div class="trash">
    <!-- Add and Remove Wire buttons -->
    <div v-if="!this.$parent.circuitDrawingFlag" class="add-remove-wire">
      <button class="add-wire" @click="this.$parent.createWire">+</button>
      <button class="remove-wire" @click="deleteWire">-</button>
    </div>
    <!-- end Add and Remove Wire buttons -->
    
    <!-- Trash-Area -->
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
    <!-- end Trash-Area -->

  </div>
</template>
<!-- =============================================================  -->
<script>
import draggable from "vuedraggable";
import { mapState, mapGetters, mapActions } from "vuex";

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
    ...mapActions(["addWire"]),
    ...mapActions(["removeWire"]),
    ...mapActions(["setCountControls"]),
    ...mapActions(["setCountSwaps"]),
    ...mapActions(["setCountCustoms"]),

    // Event handling on gates dropped in the wire
    
    // When dropping the gates in trash if the gate are dropped from the circuit then
    // replace it by Identity Gate , but if it dropped from toolbox do nothing
    add: function(evt) {
      if (evt.from.classList != "toolbox-gates-area") {
        // Put i (identity) gate in the same position
        var wire = evt.from.id.replace("list", "");
        this.$parent.$refs.wire[wire - 1].addGateByIndex(evt.oldIndex, "i");

        // check for gates need for validations as (control , swaps , custom)
        if (evt.clone.id === "●" || evt.clone.id === "○") {
          this.setCountControls(-1);
          this.$parent.controlSystem();
        } else if (evt.clone.id == "Swap") {
          this.setCountSwaps(-1);
        }
      }
      this.list = [];
    },
    // Call the deleteWire fnuction from parent Clone 
    deleteWire(){
      this.$parent.deleteWire(this.jsonObject.wires-1)
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
