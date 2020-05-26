// I should make getters to all live results objects
export default {
  // Live Results of the current circuit
  liveResults: (state) => state.results,

  gates: (state) => state.gates, // in case of add custom gates
  messages: (state) => state.messages,

  // Counters
  wiresCount: (state) => state.jsonObject.wires,
  specialGatesCounter:(state) => state.specialGatesCounter,

/*
// i think i dont need it but keep it
  messagesCount: (state) => { 
    state.messages.advanced.length +
      state.messages.advanced.length +
      state.messages.errors.length;
  },
*/
};
