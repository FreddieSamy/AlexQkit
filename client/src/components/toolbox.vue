<template>
  <div class="toolbox">
    <draggable
      class="dragArea"
      :list="list"
      :group="{ name: 'gates', pull: 'clone', put: false }"
      :clone="cloneGate"
      @change="log"
    >
      <transition-group type="transition" name="flip-list">
        <div class="toolbox-gates" v-for="element in list" :key="element.id" :id="element.name">
          <div class="gate-name">{{ element.name }}</div>
        </div>
      </transition-group>
    </draggable>
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
      list: [
        { name: "x"    , id: "x"    },
        { name: "y"    , id: "y"    },
        { name: "z"    , id: "z"    },
        { name: "h"    , id: "h"    },
        { name: "i"    , id: "i"    },
        { name: "c"    , id: "c"    },
        { name: "oc"   , id: "oc"   },
        { name: "swap" , id: "swap" },
        { name: "s"    , id: "s"    },
        { name: "sdg"  , id: "sdg"  },
        { name: "t"    , id: "t"    },
        { name: "tdg"  , id: "tdg"  },
        { name: "m"    , id: "m"    }
      ]
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
      this.list.push({ name: "j", id: 10 });
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
  display: inline-table;
  min-width: 70%;
  max-width: 70%;
}
.toolbox-gates {
  border: 1px dashed black;
  display: inline-block;
  margin: 0em 0.7em 0em 0em;
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
  display: inline-block;
  padding: 0.2em 0.2em 0.2em 0.2em;
  margin: 0.2em 0.2em 0.2em 0.2em;
  max-width: 50%;
}
.flip-list-move {
  transition: transform 0.3s;
}
.user-tools {
  margin: 1.2em 0em 0em 0.2em;
  height: 2em;
}
#c {
  /*
  background-color: red;
  */
}
</style>
