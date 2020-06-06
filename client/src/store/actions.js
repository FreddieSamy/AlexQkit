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
  setAlgorithms({commit},algorithms){
    commit("setAlgorithms",algorithms)
  },
  // Adders Functions
  addMessage: ({ commit }, message) => {
    commit("appendMessage", message);
  },
  addWire: ({ commit }) => {
    commit("addWire");
  },
  addCustomGate({ commit }, customGate) {
    commit("appendCustomGate", customGate);
  },

  // Removers Functions
  removeWire: ({ commit },wireIdx) => {
    commit("removeWire",wireIdx);
    commit("setCountSpecialGates");
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

  setCountSpecialGates:({commit}) => {
      commit("setCountSpecialGates")
  },

  // Run Functions
  runCircuit: ({ commit }) => {
    commit("sendCircuit");
  },


  // Store at Local Store of the browser
  storeLocal:({ commit },objectName)=>{
    commit('storeLocal',objectName); 
  } ,
  getLocal:({commit},objectName)=>{
    commit('getLocal',objectName); 
  },
  isStored:({commit},objectName)=>{
    commit('isStored',objectName); 
  }

};
