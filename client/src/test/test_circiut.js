
export const testCases = [
  {
    name: "test0",
    circuit: {
      wires: 1,
      init: ["0"],
      rows: [["x"]]
    },
    result : '|1⟩'
  },
  {
    name: "test1",
    circuit: {
      wires: 2,
      init: ["0", "0"],
      rows: [[],[]],
    },
    result : '|00⟩'
  },
  {
    name: "test2",
    circuit: {
      wires: 2,
      init: ["0", "0"],
      rows: [
        ["x"],
        ["i"],
      ],
    },
    result : '|10⟩'
  },
  {
    name: "test3",
    circuit: {
      wires: 2,
      init: ["0", "0"],
      rows: [
        ["i"],
        ["x"],
      ],
    },
    result : '|01⟩'
  },

];



//  we will manually add as much as we can a unit test 

//  we will run an automation test by setAlgorithm , sendSystem Functions
//  then caluclate results and compoare it by dirac also we calulate the time needed
//  to run the circiut printing all result in the console


