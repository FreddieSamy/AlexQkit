<template>
  <div>
    <GChart class="chart" type="ColumnChart" :data="chart" :options="chartOptions" />
  </div>
</template>
<!-- ========================================================== -->
<script>
import { GChart } from "vue-google-charts";
import { mapGetters } from "vuex";
export default {
  name: "Histogram",
  display: "Histogram",
  components: { GChart },
  computed: {
    ...mapGetters(["liveResults"]),
    chart() {
      let temp = this.liveResults.chart;
      temp.unshift(["state", "Non zero probabilities "]);
      return temp;
    },
    chartOptions() {
      return {
        title: "Circuit Histogram",
        explorer: { axis: "horizontal" },
        chartArea: {
          width: Math.max(this.liveResults.chart.length * 50, 250)
        },
        vAxis: {
          maxValue: 1
        }
      };
    }
  }
};
</script>
<!-- ========================================================== -->
<style scoped>
div {
  /* left: 10px; */
  max-width: 95%;
}
chart {
  overflow-x: auto;
}
</style>
