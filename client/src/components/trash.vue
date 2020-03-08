<template>
  <div class="trashArea">
    <draggable 
    class="trash-drop-area" 
     group="gates"

     >
      Trash Drop Area
    </draggable>
  </div>
</template>
<!-- =============================================================  -->
<script>
import draggable from "vuedraggable";
export default {
  name: "trash",
  display: "trash",
  components: {
    draggable,
  },
  methods:{
  }
};
</script>
<!-- =============================================================  -->
<style scoped>
.trashArea {
  color: #ef9494;
  border: 0.1em dashed #ef9494;
  border-radius: 0.2em;
  display: block;
  margin: 0.2em 0.2em 0em 0.2em;
  padding: 0.1em 0.5em 0.1em 0.5em;
  width: 97%;
  text-align: center;
}
</style>
