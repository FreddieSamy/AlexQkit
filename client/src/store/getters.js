export default {
  wiresCount: (state) => state.jsonObject.wires,
  messages: (state) => state.messages,
  liveResults: (state) => state.results,
  // I should make getters to all live results objects
};
