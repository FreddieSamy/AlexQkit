<template>
  <div id="matrixRepresentation" class="matrix-box">
    <label class="matrix-label">Matrix Representation</label>
    <katex-element class="matrix"  :expression=matrixLatex />-
  </div>
</template>
<!-- =============================================================  -->

<script>
//"\left(\begin{matrix}1 & 0 \\0 & 1\end{matrix}\right)" // \begin{pmatrix}1&2 \\ 3&4\end{pmatrix}

//\left(\begin{matrix}1 &0 \\0 & 1\\0&1\end{matrix}\right)
//\left(\begin{matrix}1&0&0&0\\0&1&0&0\\0&0&1&0\\0&0&0&1\\end{matrix}\right)
import Vue from "vue";
import "katex/dist/katex.min.css"; // eh dah .... ?
import VueKatex from "vue-katex";
import { mapGetters } from "vuex";

Vue.use(VueKatex, {
  globalOptions: {
    
  }
});

export default {
  name: "MatrixRepresentation",
  display: "MatrixRepresentation",
  data() {
    return {
    
    }
  },
  computed: {
    ...mapGetters(["liveResults"]),
      matrixLatex(){
      // eslint-disable-next-line no-useless-escape
      let prefix = "\\left(\\begin{matrix}"
      let postfix = "end{matrix}\\right)"
      var matlatex = ""
      var matrix = this.liveResults.matrixRepresentation
      for (let i = 0; i < matrix.length; i++) {
            for (let j = 0; j < matrix[0].length; j++) {
                matlatex += matrix[i][j]+"&"
              
            }
            matlatex = matlatex.slice(0, -1);
             matlatex += "\\\\"
            
      }
      matlatex = matlatex.slice(0, -1);
      //window.console.log(prefix+matlatex+postfix)
      return prefix+matlatex+postfix
    }

  },
};
</script>
<!-- =============================================================  -->

<style scoped>
.matrix-box {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 0px;
  margin: 0px;
  border-radius: 0.5em;
}
.matrix-label{
  margin: 0px 0px 20px 0px;
}
</style>