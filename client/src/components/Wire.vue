<template>
  <div class="wire" :id="'wire-' + id">
    <!-- Delete Wire Button  -->
    <div class="delete-wire" :id="'d-' + id">
      <button class="delete-btn" @click="deleteWire">x</button>
    </div>
    <!--end Delete wire Button  -->
    <!--wire-qubit-name-->
    <label class="qubit-name">
      q
      <sub>{{id-1}}</sub>
    </label>
    <!---end-wire-qubit-name-->
    <button class="qubit-state" :id="'q' + id + '-0'" @click="qubitState">|{{ state }}⟩</button>
    <hr class="wire-hr" />
    <!-- Wire Drop Area (Gates Place)-->
    <draggable
      class="wire-drop-area"
      :id="'list' + id"
      :list="list"
      group="gates"
      @add="add"
      @remove="remove"
      @update="update"
    >
      <!-- =================================== Start Gate ====================================== -->
      <!-- Start Gate that need to be a component urgently  -->
      <div
        class="circuit-gate"
        v-for="(element,index) in list"
        :key="element.id"
        :id="element.name"
        :row="'_'+(id)"
        :col="'_'+(index+1)"
      >
        <!-- static hard coding block in case of custom gate-->
        {{element.name[0]=='c'? element.name.slice(3) : element.name }}
        <select
          @change="setOrderId"
          v-if="element.name[0]=='c' && element.name[1]!='1'"
          class="custom-gate-order"
        >
          <option
            v-for="(item,order) in parseInt(element.name[1])"
            :key="order"
            :value="order"
          >{{ order }}</option>
        </select>
        <!-- end of hard coded block  need a vue filter or special directive -->

        <!-- in case of Condtional loop -->
        <select @change="setOrderId" v-if="element.name[0]=='l' " class="custom-gate-order">
          <option value="*">*</option>
          <option value="0">0</option>
          <option value="1">1</option>
        </select>
        <!-- end in case of Conditional loop -->
      </div>
      <!-- End Gate  -->
      <!-- =================================== End Gate ====================================== -->
    </draggable>
    <!-- end Wire Drop Area (Gates Place)-->

    <!-- Percent -->
    <Percent :probability="this.liveResults.probabilities[id-1]||0" />
    <!-- End of Percent  -->

    <!-- BlochSphere -->
    <div class="bloch-sphere-body">
      <img
        class="bloch-sphere"
        :src="defaultBlochSphereRoute"
        :id="'bloch-sphere-'+id"
      />
    </div>
    <!-- end BlockSphere -->

  </div>
</template>
<!-- =============================================================  -->
<script>
import draggable from "vuedraggable";
import Percent from "./Percent";
import { defaultBlochSphereRoute } from "./../data/routes";
import { states } from "./../data/gates_and_states";
import { mapActions, mapGetters, mapState } from "vuex";

export default {
  name: "wire",
  display: "wire",
  components: {
    draggable,
    Percent,
  },
  props: ["id"],

  data() {
    return {
      list: [],
      state: states[0],
      defaultBlochSphereRoute: defaultBlochSphereRoute
    };
  },
  watch: {
    list: {
      immediate: true,
      handler() {
        //this.updateWireAttributes();
        // watcher may be terminated 
      }
    }
  },

  /*  Life Cycle Hook of wire component  */
  created: function() {
    this.addIdentityRow(this.jsonObject.colsCount);
  },
  updated() {
    // act like wathcer on all data
    let wire = {
      qstate: this.state,
      list: this.getGates(this.id - 1),
      idx: this.id - 1
    };
    this.setWire(wire);
  },
  destroyed() {
    this.$parent.controlSystem();
  },
  computed: {
    ...mapGetters(["wiresCount"]),
    ...mapGetters(["liveResults"]),
    ...mapState(["jsonObject"])
  },
  methods: {
    ...mapActions(["setWire"]),
    ...mapActions(["runCircuit"]),
    ...mapActions(["setCountControls"]),
    ...mapActions(["setCountSwaps"]),
    ...mapActions(["setCountCustoms"]),
    ...mapActions(["removeWire"]),

    //== Start Events Handling Functions ===============================================
    add: function(evt) {
      // in case droped between 2 gates
      if (
        evt.newIndex < this.jsonObject.colsCount &&
        this.list[evt.newIndex + 1]["name"] == "i"
      ) {
        this.list.splice(evt.newIndex + 1, 1);
      } else {
        this.$parent.addGateColumn(this.id, evt.newIndex, "i");
      }

      if (evt.from.id[0] == "l") {
        var wire = evt.from.id.replace("list", "");
        this.$parent.$refs.wire[wire - 1].addGateByIndex(evt.oldIndex, "i");
      } else if (evt.clone.id === "●" || evt.clone.id === "○") {
        this.setCountControls(1);
      } else if (evt.clone.id == "Swap") {
        this.setCountSwaps(1);
      } else if (evt.clone.id[0] == "c") {
        this.setCountCustoms(1);
      } else if (evt.clone.id[0] == "l") {
        window.console.log("add conditional loop");
      }
      this.$parent.updateMaxWire();
    },
    //-----------------------------------------------------------------------
    update: function() {
      this.$parent.updateMaxWire();
      this.$parent.removeIdentitySystem();
    },
    //-----------------------------------------------------------------------
    remove: function() {
      this.$parent.updateMaxWire();
      this.$parent.removeIdentitySystem();
    },
    //== End Events Handling Functions ===============================================

    qubitState: function(evt) {
      var i = (parseInt(evt.target.id.slice(-1)) + 1) % 6;
      var id = evt.target.id.substring(0, evt.target.id.search("-") + 1);
      evt.target.id = id + i;
      this.state = states[i];
      evt.target.innerHTML = "|" + this.state + "⟩";
      this.jsonObject.init[id.slice(1, -1) - 1] = this.state;
      // this.runCircuit();
    },
    //-----------------------------------------------------------------------
    deleteWire: function() {
      this.removeWire(this.id - 1);
      this.$nextTick(() => {
        this.$parent.setAlgorithm({ circuit: this.jsonObject }, false, false);
        this.$parent.removeIdentitySystem();
      });
    },
    //-----------------------------------------------------------------------
    addIdentityRow: function(length) {
      this.list.push(...new Array(length).fill({ name: "i" }));
    },
    //-----------------------------------------------------------------------
    addGateByIndex: function(columnIndex, gateName) {
      this.list.splice(columnIndex, 0, { name: gateName });
    },
    //-----------------------------------------------------------------------
    removeGateByIndex: function(gateIndex) {
      if (this.list[gateIndex]["name"] == "i") {
        this.list.splice(gateIndex, 1);
      }
    },
    //-----------------------------------------------------------------------
    resetWire: function() {
      this.list = [];
      this.setState("0");
    },
    //-----------------------------------------------------------------------
    getGates: function(rowId) {
      var gates = [];
      for (let colIdx = 0; colIdx < this.list.length; colIdx++) {
        if (this.list[colIdx]["name"][0] == "c") {
          window.console.log("custom here at " + this.id + " at col " + rowId);
          gates.push(this.list[colIdx]["name"]);
        } else {
          gates.push(this.list[colIdx]["name"]);
        }
      }
      return gates;
    },
    //-----------------------------------------------------------------------
    setState: function(state) {
      let i = this.$store.state.states.indexOf(this.state);
      document.getElementById("q" + this.id + "-" + i).innerHTML =
        "|" + state + "⟩";
      document.getElementById("q" + this.id + "-" + i).id =
        "q" + this.id + "-" + state;
      this.state = state;
    },
    //-----------------------------------------------------------------------
    setGates: function(gatesList, append = true) {
      if (append == false) {
        this.list = []; // disabled to push on the wire
      }
      for (let colIdx = 0; colIdx < gatesList.length; colIdx++) {
        // can be optimized more
        this.list.push({ name: gatesList[colIdx] });
        if (gatesList[colIdx] === "●" || gatesList[colIdx] === "○") {
          this.setCountControls(1);
        } else if (gatesList[colIdx] === "Swap") {
          this.setCountSwaps(1);
        } else if (gatesList[colIdx][0] === "c") {
          this.setCountCustoms(1);
        }
      }
    },
    setOrderId(evt) {
      //  work for both  custom gates  and loops
      var gateId = evt.srcElement.parentElement.id.substring(
        0,
        evt.srcElement.parentElement.id.indexOf(".") + 1
      );

      evt.srcElement.parentElement.id = gateId + evt.srcElement.value;
      let col = evt.srcElement.parentElement
        .getAttribute("col")
        .replace("_", "");
      col = parseInt(col) - 1;
      this.list[col] = { name: evt.srcElement.parentElement.id };

      let wire = {
        qstate: this.state,
        list: this.getGates(this.id - 1),
        idx: this.id - 1
      };
      this.setWire(wire);
      this.$parent.updateMaxWire();
      window.console.log(this.jsonObject.rows);
    }
  }
};
</script>
<!-- =============================================================  -->
<style scoped>
.wire {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  width: 100%;
  z-index: 0;
  margin: 5px 0px;

}
.wire-drop-area {
  height: 37px;
  display: flex;
  flex-basis: 75%;
}
.wire-hr {
  position: fixed;
  position: -webkit-sticky;

  stroke-width: 10;
  width: 100%;
  margin: 0px;
  z-index: -4;
  stroke: black;
  color: black;
}

.delete-wire {
  margin: 0px;
  padding: 0px 5px 0px 5px;
  background: white;
  /* border:1px solid black; */
}
.delete-btn {
  color: white;
  background: #ff9890;
  border-radius: 100%;
  padding: 0px 3px 0px 3px;
  border: transparent;
  opacity: 0.5;
}
.delete-btn:hover {
  opacity: 1;
  transform: scale(1.5);
}
.qubit-name {
  margin: 0;
  padding: 0px 7px 0px 7px;
  background: white;
  justify-self: center;
  align-self: center;
  /* border:1px solid black; */
}
.qubit-state {
  border-radius: 0.5em;
  width: 2.5em;
  height: 2em;
  margin-right: 0.6em;
  background-color: white;
  border: 2px solid #306ba2;
}
.circuit-gate {
  color: white;
  font-size: 15px;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  text-align: center;
  border-radius: 20%;
  margin: 0 5px;
  padding: 0;
  width: 35px;
  height: 35px;
  background-color: #5d6d7e;
  z-index: 0;
}
.custom-gate-order {
  display: flex;
  flex-basis: 100%;
  height: 15px;
  max-width: 30px;
  padding: 0;
  margin: -5px 0px 0px 0px;
  font-size: 10px;
  border-radius: 10px;
}
/* Bloch sphere */
.bloch-sphere-body{
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
.angle-input {
  display: flex;
  flex-basis: 100%;
  margin: 0px auto;
  text-align: center;
  padding: 2px 0px 2px 0px;
  width: 75%;
  border-radius: 8px;
}
#Rx,
#Ry,
#Rz {
  align-self: center;
}
div[id^="R"],
#Swap,
#Reset {
  font-size: 10px;
  margin: 0px 5px 0px 5px;
}
div[id^="Rx"],
div[id^="Ry"],
div[id^="Rz"] {
  font-weight: bold;
  background: #ff8c61;
}
#○,
#● {
  color: black;
  margin: -2px 4.9px 0px 4.9px;

  transform: scale(1.7);
  background: none;
  border: none;
}
#○ {
  background-image: url("../assets/whitedot.png");
  background-repeat: no-repeat;
  background-position: center;
  background-size: 7px 6px;
}
#i {
  opacity: 0.8;
}
#m .circuit-gate text {
  opacity: 0.01;
}
/* all Inputs focus */
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
/* Firefox */
input[type="number"] {
  -moz-appearance: textfield;
}
option:focus,
select:focus,
textarea:focus,
input:focus {
  outline: none;
}
</style>
