<template>
  <div>
    <svg width="30" height="30">
        <rect
          width="30"
          height="30"
          x="0"
          y="0"
          stroke="black"
          stroke-width="0.5"
          fill="white"
          rx="1"
        />
        <rect width="30" :height=percent x="0" :y=yAxis fill="lightgreen" rx="0" />
        <text x="50%" y="18" text-anchor="middle" font-size="10" v-text="percent+'%'">%</text>
    </svg>
  </div>
</template>
<!-- =============================================================  -->
<script>

export default {
  name: "Probability",
  display: "Probability",
  components: {},
  props: ["percent"],
  data(){
     return {   
         
     }
  },
  computed:{
    yAxis() {
        return (100 - this.percent)+"%"
    }
  }

};
</script>
<!-- =============================================================  -->
<style scoped>
div {
  display: flex;
  transition: transform .2s;
  z-index: 0;
}

div:hover{
  transform: scale(2);
  z-index: 2;
}
svg{
    text-align: center;
}
</style>
