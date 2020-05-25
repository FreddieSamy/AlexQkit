export default {
  setColsCount: ({ commit }, count) => {
    commit("setCols", count);
  },
  setExeCount: ({ commit }, count) => {
    commit("setExe", count);
  },
  setWire: ({ commit }, wire) => {
    commit("setRow", wire);
  },
  addMessage: ({ commit }, message) => {
    //window.console.log("hello message")

   commit("appendMessage", message);
  },
  addWire: ({ commit }) => {
    commit("appendInit");
    commit("appendWire");
  },
  addCustomGate({commit},customGate){
    commit("appendCustomGate",customGate);
  },
  removeWire: ({ commit }) => {
    commit("popInit");
    commit("popWire");
  },
  resetCircuit: ({ commit }) => {
    commit("reset");
  },
  removeMessages:({commit}) => {
    commit("removeMessages")
  },
  runCircuit: ({ commit }) => {
    commit("sendCircuit");
  },
  checkSwapSystem: ({ commit }) => {
    commit("swapConstrains");
  },
};
