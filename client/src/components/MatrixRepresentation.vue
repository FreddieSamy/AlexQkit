<template>
  <div id="matrixRepresentation" class="matrix-box">

      <label>Matrix Representation</label>
      <!--<katex-element  expression="\left(\begin{matrix}1 & 0 \\0 & 1\end{matrix}\right)"/>-->


        <ul>
        <li v-for="(i , row ) in this.value" :key="row">{{i}}</li>
        </ul>
  

  </div>
</template>
<!-- =============================================================  -->

<script>
//"\left(\begin{matrix}1 & 0 \\0 & 1\end{matrix}\right)" // \begin{pmatrix}1&2 \\ 3&4\end{pmatrix}
import Vue from "vue";
import "katex/dist/katex.min.css";
import VueKatex from "vue-katex";

Vue.use(VueKatex, {
  globalOptions: {
    //... Define globally applied KaTeX options here
  }
});

export default {
  name: "MatrixRepresentation",
  display: "MatrixRepresentation",
  data() {
    return {
      value: []
    };
  }
};
</script>
<!-- =============================================================  -->

<style scoped>

ul {
   list-style-type: none;
   flex-basis: 100%;
   align-self: center;
   padding: 0px;
}
li {
   padding: 10px;
}
label{
  flex-basis: 100%;
  margin:10px 0px 0px 0px;
  align-self: center;
}
.matrix-box {
  display: flex;
  flex-direction: column;
  justify-content:center;
  align-items:stretch;
  padding: 0px;
  margin: 0px;
  border-radius: 0.5em;
}
</style>