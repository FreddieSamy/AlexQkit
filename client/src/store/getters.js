export default {
  gates:(state) => state.gates, // in case of add custom gates 
  wiresCount: (state) => state.jsonObject.wires,
  messages: (state) => state.messages,
  liveResults: (state) => state.results,
  // I should make getters to all live results objects
};
