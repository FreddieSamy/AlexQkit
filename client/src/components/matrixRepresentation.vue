<template>
   <div id="matrixRepresentation" class="matrixRepresentation">
    <h4>MatrixRepresentation</h4>
    <span id="elementRepresntation">
        <li v-for="(i , row ) in this.$parent.matrixRepresentation" :key=row  >
          {{i}}
        </li>
    </span>
  </div>
</template>
<script>
export default {
     name: "matrixRepresentation",
     display: "matrixRepresentation",
};
</script>

<style scoped>
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
  /*border: 1px solid black;*/
  border-radius: 0.5em;
}
.matrixRepresentation h4{
    display: inline-block;
    margin: 1em 1em 1em 1em;
}
</style>