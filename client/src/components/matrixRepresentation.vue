<template>
  <div id="matrixRepresentation" class="matrixRepresentation">
    <center>
      <h4>Matrix Representation</h4>
      <!--<katex-element  expression="\left(\begin{matrix}1 & 0 \\0 & 1\end{matrix}\right)"/>-->

      <span id="elementRepresntation">
        <li v-for="(i , row ) in this.value" :key="row">{{i}}</li>
      </span>
    </center>
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
  name: "matrixRepresentation",
  display: "matrixRepresentation",
  data() {
    return {
      value: []
    };
  }
};
</script>
<!-- =============================================================  -->

<style scoped>
/*
#elementRepresntation {
  display: none;
  position: absolute;
  background-color: lightgray;
  padding: 10px;
  border: solid;
  border-radius: 5px;
}
#matrixRepresentation:hover #elementRepresntation {
  display: block;
}
.matrixRepresentation {
  //border: 1px solid black;
  border-radius: 0.5em;
}
.matrixRepresentation h4{
    display: inline-block;
    margin: 1em 1em 1em 1em;
}*/
.matrixRepresentation {
  flex: 1;
  border: 0.05em solid black;
  padding: 0em 0em 0em 0.1em;
  margin: 0em 0em 0em 0em;
  border-radius: 0.5em;
}
</style>