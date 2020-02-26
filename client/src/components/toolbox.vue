<template>
  <div class="toolbox">
    <div class="shots">
      <label>Number<br />Of<br />Shots</label><br />
      <input
        type="number"
        name="shots"
        placeholder="1024"
        id=""
      /><br /><br /><br />
    </div>
    <div class="box">
      <div class="lbl1"><label>Toolbox</label></div>
      <div class="lbl1"><label>Custom Gates</label></div>

      <br />

      <div class="dragArea">
        <draggable
          class="Area1"
          :list="gates1"
          :group="{ name: 'gates', pull: 'clone', put: false }"
          :clone="cloneGate"
          @change="log"
        >
          <transition-group type="transition" name="flip-list">
            <div
              class="toolbox-gates"
              v-for="element in gates1"
              :key="element.id"
              :id="element.name"
            >
              <div class="gate-name">{{ element.name }}</div>
            </div>
          </transition-group>
        </draggable>
        <draggable
          class="Area2"
          :list="gates2"
          :group="{ name: 'gates', pull: 'clone', put: false }"
          :clone="cloneGate"
          @change="log"
        >
          <transition-group type="transition" name="flip-list">
            <div
              class="toolbox-gates"
              v-for="element in gates2"
              :key="element.id"
              :id="element.name"
            >
              <div class="gate-name">{{ element.name }}</div>
            </div>
          </transition-group>
        </draggable>
        <div class="Area2">
          <draggable
            :list="gates3"
            :group="{ name: 'gates', pull: 'clone', put: false }"
            :clone="cloneGate"
            @change="log"
          >
            <transition-group type="transition" name="flip-list">
              <div
                class="toolbox-gates"
                v-for="element in gates3"
                :key="element.id"
                :id="element.name"
              >
                <div class="gate-name">{{ element.name }}</div>
              </div>
            </transition-group>
          </draggable>
          <input class="angle" type="number" name="rx" placeholder="90" id="" />
          <input
            class="angle"
            type="number"
            name="ry"
            placeholder="PI/2"
            id=""
          />
          <input
            class="angle"
            type="number"
            name="rz"
            placeholder="PI/2"
            id=""
          />
        </div>

        <draggable
          class="Area1"
          :list="gates4"
          :group="{ name: 'gates', pull: 'clone', put: false }"
          :clone="cloneGate"
          @change="log"
        >
          <transition-group type="transition" name="flip-list">
            <div
              class="toolbox-gates"
              v-for="element in gates4"
              :key="element.id"
              :id="element.name"
            >
              <div class="gate-name">{{ element.name }}</div>
            </div>
          </transition-group>
        </draggable>
      </div>
      <draggable
        class="dragArea2"
        :list="customGates"
        :group="{ name: 'gates', pull: 'clone', put: false }"
        :clone="cloneGate"
        @change="log"
        :style="w"
      >
        <transition-group type="transition" name="flip-list">
          <div
            class="toolbox-gates"
            v-for="element in customGates"
            :key="element.id"
            :id="element.name"
          >
            <div class="gate-name">{{ element.name }}</div>
          </div>
        </transition-group>
      </draggable>
    </div>
    <div class="user-tools">
      <button class="addGate" @click="addGate">Add Custom Gate</button>
    </div>
  </div>
</template>
<!-- =============================================================  -->
<script>
import draggable from "vuedraggable";
export default {
  name: "toolbox",
  display: "toolbox",
  components: {
    draggable
  },
  data() {
    return {
      gates1: [
        { name: "c", id: "c", index: "" },
        { name: "m", id: "m", index: "" },
        { name: "oc", id: "oc", index: "" },
        { name: "reset", id: "reset", index: "" }
      ],
      gates2: [
        { name: "x", id: "x", index: "" },
        { name: "y", id: "y", index: "" },
        { name: "z", id: "z", index: "" },
        { name: "h", id: "h", index: "" },
        { name: "swap", id: "swap", index: "" }
      ],
      gates3: [
        { name: "rx", id: "rx", index: "" },
        { name: "ry", id: "ry", index: "" },
        { name: "rz", id: "rz", index: "" }
      ],
      gates4: [
        { name: "s", id: "s", index: "" },
        { name: "t", id: "t", index: "" },
        { name: "sdg", id: "sdg", index: "" },
        { name: "tdg", id: "tdg", index: "" }
      ],
      customGates: [],
      w: "width:7.7em"
    };
  },
  methods: {
    log: function(/*evt*/) {},
    cloneGate({ name }) {
      return {
        name: name
      };
    },
    addGate() {
      this.customGates.push({
        name: "" + (this.customGates.length + 1),
        id: this.customGates.length + 1
      });
      this.w = "width:" + Math.ceil(this.customGates.length / 2) * 3.85 + "em";
    }
  }
};
</script>
<!-- =============================================================  -->
<style scoped>
.addGate {
  margin: 0em 0em 0em 0.2em;
  background-color: white;
  border-radius: 0.5em;
}
.toolbox {
  /*border: 1px dashed black;*/
  /*background-color: red;*/
  display: table;
  width: 100%;
}
.toolbox-gates {
  border: 1px dashed black;
  display: inline-block;
  margin: 0.3em 0.7em 0.3em 0.5em;
  width: 2.5em;
  height: 2.5em;
  border-radius: 0.3em;
  background-color: #d5d8dc;
}
.gate-name {
  text-align: center;
  margin: 0.7em 0.5em 0.5em 0.5em;
  color: black;
}
.dragArea {
  border: 1px solid black;
  display: inline-block;
  margin-right: 0.4em;
  width: 40em;
  white-space: pre-wrap;
  height: 7.4em;
  overflow: auto;
  border-radius: 0.3em;
}
.dragArea2 {
  border: 1px solid black;
  display: inline-block;
  /*position: fixed;*/
  /*margin: 0.2em 0.2em 0.2em 0.2em;*/
  max-width: 39.4em;
  min-width: 7.7em;
  white-space: pre-wrap;
  height: 7.4em;
  overflow: auto;
  border-radius: 0.3em;
}
.Area1 {
  margin: 0.1em 0.1em 0.1em 0.1em;
  display: inline-block;
  /*overflow: auto;*/
  border: 1px dashed black;
  white-space: pre-wrap;
  height: 6.6em;
  border-radius: 0.3em;
  width: 7.7em;
}
.Area2 {
  margin: 0.1em 0.1em 0.1em 0.1em;
  display: inline-block;
  /*overflow: auto;*/
  border: 1px dashed black;
  white-space: pre-wrap;
  height: 6.6em;
  border-radius: 0.3em;
  width: 11.6em;
}
.flip-list-move {
  transition: transform 0.3s;
}
.user-tools {
  margin: 0em 0em 0em 0em;
  height: 2em;
}
.lbl1 {
  display: inline-block;
  min-width: 40em;
  margin-right: 0.4em;
}
.shots {
  display: inline-block;
  margin: 0em 1em 0em 1em;
}
.angle {
  margin: 0.3em 0.7em 0.3em 0.5em;
  width: 3em;
  height: 3em;
  border-radius: 0.3em;
}
.box {
  display: inline-block;
}
#c {
  /*
  background-color: red;
  */
}
</style>