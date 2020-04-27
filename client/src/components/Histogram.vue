<template>
  <div class="histogram">
    <GChart style="width:500px" type="ColumnChart" :data="chartData" :options="chartOptions" />
  </div>
</template>
<!-- ========================================================== -->
<script>
import { GChart } from "vue-google-charts";
export default {
  name:'Histogram',
  display:'Histogram',
  components:{ GChart },
  data() {
    return {
 chartData: [
        ["Qbit", "state"],
        ["000",  0.49267578125,],
        ["001", 0.0],
        ["010",  0.50732421875,],
        ["011", 0],
        ["100", 0],
        ["101", 0.8],
        ["110", 0],
        ["111", 0]
      ],
      chartOptions: {
        chart: {
          title: "Company Performance",
          subtitle: "Sales, Expenses, and Profit: 2014-2017"
        },vAxis: {
            maxValue: 1,
          }
      },
    }
  },
  }
</script>
<!-- ========================================================== -->
<style scoped>

</style>
