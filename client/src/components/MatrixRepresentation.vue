<template>
  <div id="myNav2" class="overlay" style="width:0%">
    <a href="javascript:void(0)" class="closebtn" @click="closeNav()">&#10006;</a>
    <div id="matrixRepresentation" class="matrix-box">
      <label class="matrix-label">Matrix Representation</label>
      <katex-element class="matrix" :expression="expression" />
    </div>
  </div>
</template>
<!-- =============================================================  -->

<script>
//"\left(\begin{matrix}1 & 0 \\0 & 1\end{matrix}\right)" // \begin{pmatrix}1&2 \\ 3&4\end{pmatrix}

//\left(\begin{matrix}1 &0 \\0 & 1\\0&1\end{matrix}\right)
//\left(\begin{matrix}1&0&0&0\\0&1&0&0\\0&0&1&0\\0&0&0&1\\end{matrix}\right)
import Vue from "vue";
import "katex/dist/katex.min.css"; 
import VueKatex from "vue-katex";
import axios from "axios";
import { mapState, mapGetters } from "vuex";
import { matrixRepresentationRoute } from "./../data/routes.js";

Vue.use(VueKatex, {
  globalOptions: {}
});

export default {
  name: "MatrixRepresentation",
  display: "MatrixRepresentation",
  data() {
    return {
      expression: ""
    };
  },
  computed: {
    ...mapState(["jsonObject"]),
    ...mapGetters(["liveResults"])
  },
  methods: {
    // ----------------------------------------------------
    openNav() {
      var json_object = {
        rows: this.jsonObject.rows.reverse(),
        radian: this.jsonObject.radian,
        init: this.jsonObject.init,
        exeCount: this.jsonObject.exeCount,
        custom: this.jsonObject.custom,
        repeated: this.jsonObject.repeated,
        wires: this.jsonObject.wires
      };
      window.console.log(this.jsonObject.rows.reverse());
      axios.post(matrixRepresentationRoute, json_object).then(res => {
        this.liveResults.matrixRepresentation = res.data.matrixRepresentation;
        this.expression = this.matrixLatex();
      });
      document.getElementById("myNav2").style.width = "100%";
    },
    // ----------------------------------------------------
    closeNav() {
      document.getElementById("myNav2").style.width = "0%";
    },
    // ----------------------------------------------------
    matrixLatex() {
      // eslint-disable-next-line no-useless-escape
      let prefix = "\\left(\\begin{matrix}";
      let postfix = "end{matrix}\\right)";
      var matlatex = "";
      var matrix = this.liveResults.matrixRepresentation;
      for (let i = 0; i < matrix.length; i++) {
        for (let j = 0; j < matrix[0].length; j++) {
          matlatex += matrix[i][j] + "&";
        }
        matlatex = matlatex.slice(0, -1);
        matlatex += "\\\\";
      }
      matlatex = matlatex.slice(0, -1);
      //window.console.log(prefix+matlatex+postfix)
      return prefix + matlatex + postfix;
    }
    // ----------------------------------------------------
  }
};
</script>
<!-- =============================================================  -->

<style scoped>
.matrix-box {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 10px;
  margin: 10px;
  border-radius: 0.5em;
  background: black;

}
.matrix-label {
  margin: 0px 0px 20px 0px;
}
div {
  color: white;

}
.overlay {
  height: 100%;
  top: 0;
  left: 0;
  position: fixed;
  z-index: 1;
  background-color: rgba(103, 106, 97, 0.55);
  overflow-x: hidden;
  transition: 0.5s;
  display: flex;
  justify-content: center;
  align-items: stretch;
  flex-wrap: wrap;
}
.overlay a {
  padding: 8px;
  text-decoration: none;
  font-size: 36px;
  color: rgba(255, 255, 255, 0.7);
  display: block;
  transition: 0.3s;
}

.overlay a:hover,
.overlay a:focus {
  color: #f1f1f1;
}

.overlay .closebtn {
  position: absolute;
  top: 20px;
  right: 45px;
  font-size: 30px;
}

@media screen and (max-height: 450px) {
  .overlay a {
    font-size: 20px;
  }
  .overlay .closebtn {
    font-size: 40px;
    top: 15px;
    right: 35px;
  }
}
</style>