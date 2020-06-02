<template>
  <div>
    <GChart class="chart" type="ColumnChart" :data="chart" :options="chartOptions" />
  </div>
</template>
<!-- ========================================================== -->
<script>
import { GChart } from "vue-google-charts";
import { mapGetters } from "vuex"
export default {
  name:'Histogram',
  display:'Histogram',
  components:{ GChart },
  computed: {
    ...mapGetters(['liveResults']),
    chart(){
        let temp = this.liveResults.chart;
        temp.unshift( ["Qbit", "state"])
        return temp;
    }
  },
  data() {
    return {
    
      chartOptions: {
        title:"Circuit Histogram",
        explorer: {axis: 'horizontal'},
        chartArea: {width:this.width},
      vAxis: {
            maxValue: 1,
          }
      },
    }
  },
  }
</script>
<!-- ========================================================== -->
<style scoped>
div{
  left:10px
}
chart{
  overflow-x: auto; 
}
</style>
