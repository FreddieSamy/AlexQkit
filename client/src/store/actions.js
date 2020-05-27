export default {
  // Setters Functions
  setColsCount: ({ commit }, count) => {
    commit("setCols", count);
  },
  setExeCount: ({ commit }, count) => {
    commit("setExe", count);
  },
  setWire: ({ commit }, wire) => {
    commit("setRow", wire);
  },
  // in the next 3 counters function
  //  if val +1 increment count , if -1 decrement count
  setCountControls({ commit }, val) {
    commit("setContorls", val);
  },
  setCountSwaps({ commit }, val) {
    commit("setSwaps", val);
  },
  setCountCustoms({ commit }, val) {
    commit("setCustoms", val);
  },

  // Adders Functions
  addMessage: ({ commit }, message) => {
    commit("appendMessage", message);
  },
  addWire: ({ commit }) => {
    commit("appendInit");
    commit("appendWire");
  },
  addCustomGate({ commit }, customGate) {
    commit("appendCustomGate", customGate);
  },

  // Removers Functions
  removeWire: ({ commit }) => {
    commit("popInit");
    commit("popWire");
  },
  removeMessages: ({ commit }) => {
    commit("resetMessages");
  },

  // Reset Functions
  resetCircuit: ({ commit }) => {
    commit("resetJsonObject");
    commit("resetMessages");
    commit("resetSpecialGates");
  },

  // Checkers Functions
  checkSwapSystem: ({ commit }) => {
    commit("swapConstrains");
  },
  checkWiresCustomGates: ({ commit }) => {
    commit("wirescustom");
  },

  countGate: ({ commit }, gateName) => {
    commit("countGate", gateName);
  },

  // Run Functions
  runCircuit: ({ commit }) => {
    commit("sendCircuit");
  },
};
