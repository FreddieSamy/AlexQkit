
import axios from "axios";
import { appRoute } from "../data/routes"

export default {

  // Setters
  setCols: (state, count) => { state.jsonObject.colsCount = count; },
  setExe: (state, count) => { state.jsonObject.exeCount = count; },
  setRow: (state, { qstate, list, idx }) => {
    state.jsonObject.init[idx] = qstate;
    state.jsonObject.rows[idx] = list;
  },
  setResult: (state, data) => {
    state.results.chart = data.chart
    state.results.diracNotation = data.diracNotation
    state.results.link = data.link
    state.results.matrixRepresentation = data.matrixRepresentation
    state.results.qasm = data.qasm
    state.results.qasmError = data.qasmError
  },


  // Appenders Functions
  appendInit: state => state.jsonObject.init.push("0"),
  appendWire: state => state.jsonObject.wire++,


  // Remove Functions
  removeInit: state => state.jsonObject.init.pop(),
  removeWire: (state) => {
    state.jsonObject.wire--;
    state.jsonObject.rows.pop();
  },

  // Reset System
  reset: (state) => {
    state.jsonObject.maxWire = 0;
    state.jsonObject.exeCount = 0;
    state.jsonObject.wires = 2;
    state.jsonObject.init = ['0', '0'];
    state.jsonObject.rows = [[], []];
  },




  // Server Functions
  sendCircuit: (state) => {
    try {
      window.console.log(state.jsonObject)
      axios.post(appRoute, state.jsonObject).then(
        res => { state.results = res.data; },
        error => { window.console.log(error) }
      )
    } catch (error) {
      window.console.log("i think there is an error " + error);
    }

  },
};
