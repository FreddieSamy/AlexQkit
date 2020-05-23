<template>
  <div class="editor" v-if="this.qasmFlag">
    <div class="qasm">
      <prism-editor
        :lineNumbers="true"
        :code="liveResults.qasm"
        v-model="liveResults.qasm"
        language="js"
      ></prism-editor>
    </div>
    <button class="qasmBtn" @click="sendQasm">Run</button>
  </div>
</template>
<!-- ========================================================== -->
<script>
import "prismjs";
import "prismjs/themes/prism.css";
import "vue-prism-editor/dist/VuePrismEditor.css";
import PrismEditor from "vue-prism-editor";
import axios from "axios";
import { qasmCircuitRoute, qasmRoute } from "./../data/routes.js";
import { mapGetters, mapState } from "vuex";

export default {
  name: "qasm",
  display: "qasm",
  data() {
    return { qasmFlag: false };
  },
  computed: {
    ...mapGetters(["liveResults"]),
    ...mapState(["jsonObject"])
  },
  components: { PrismEditor },
  methods: {
    //-----------------------------------------------------------------------
    qasm: function() {
      this.qasmFlag = !this.qasmFlag;
      this.$parent.controlSystem();
      if (this.qasmFlag) {
        // Me7tag a3adel deh 
        document.getElementById("qasmToolboxBtn").innerHTML = "⟨ qasm |";
      } else {
        // Me7tag a3del deh
        document.getElementById("qasmToolboxBtn").innerHTML = "| qasm ⟩";
        this.liveResults.qasm =
          'OPENQASM 2.0;\ninclude "qelib1.inc";\nqreg q[2];\ncreg c[2];';
        this.$parent.circuitDrawingFlag = false;
      }
      if (!this.$parent.circuitDrawingFlag) {
        this.$parent.$refs.tracingLine.updateTracingLine();
      } else {
        this.$parent.resetSystem();
      }
    },
    //-----------------------------------------------------------------------
    sendQasm: function() {
      // window.console.log(this.qasmCode);
      this.$parent.circuitDrawingFlag = true;
      let json_object = {
        qasm: this.liveResults.qasm,
        shots: this.jsonObject.shots,
        API_TOKEN: this.jsonObject.API_TOKEN,
        device: this.jsonObject.device
      };
      axios.post(qasmRoute, json_object).then(res => {
        if (res.data.qasmError == "") {
          this.draw();
          // me7tag a7ot setter hena 
          this.liveResults.probabilities = res.data.probabilities;
          this.liveResults.blochSpheres = res.data.blochSpheres;
          this.liveResults.chart = res.data.chart;
          this.liveResults.diracNotation = res.data.diracNotation;
          this.liveResults.link = res.data.link;
          this.jsonObject.wires = res.data.wires;

          if (this.qasmFlag) {
            this.qasmCode = res.data.qasm;
          }
        } else {
          alert("qasm code error :\n" + res.data.qasmError);
        }
      });
    },
    //-----------------------------------------------------------------------
    draw: function() {
      // var imgofblochSphere = document.getElementById("bloch");
      // imgofblochSphere.src = blockSphereRoute + new Date();
      
      // me7tag a3adel deh 
      var imgOfCircuit = document.getElementById("circuitDrawing");
      imgOfCircuit.src = qasmCircuitRoute + new Date();
    }
    //-----------------------------------------------------------------------
  }
};
</script>
<!-- ========================================================== -->
<style scoped>
.editor {
  display: block;
  height: 100%;
  width: 18em;
}
.qasm {
  overflow-y: auto;
  width: 18em;
  max-height: 20em;
  margin: 0em 0.2em 0em 0em;
  border-radius: 0.5em;
}
.qasmBtn {
  margin: 0.2em 0.2em 0.2em 0em;
  display: block;
  padding: 0.1em 0.5em 0.1em 0.5em;
  background-color: white;
  border-radius: 0.5em;
  right: 0;
  top: 0;
}
</style>
