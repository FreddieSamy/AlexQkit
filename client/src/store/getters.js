// I should make getters to all live results objects
export default {

  // Live Results of the current circuit
  liveResults: (state) => state.results,


  gates:(state) => state.gates, // in case of add custom gates 
  messages: (state) => state.messages,
  
  // Counters 
  wiresCount: (state) => state.jsonObject.wires,
  swapsCount:(state) => state.specialGatesCounter.swaps,
  controlsCount:(state) => state.specialGatesCounter.controls,
  customsCount:(state) => state.specialGatesCounter.customs,

  
};
