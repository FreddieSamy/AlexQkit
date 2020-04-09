export default [
  {
    name: "tele_algorithm1",
    circuit: {
      wires: 3,
      init: ["0", "0", "0"],
      rows: [
        ["x", "i", "c", "h", "i", "h"],
        ["i", "h", "c", "x", "c", "i"],
        ["i", "i", "x", "i", "h", "c"],
      ],
    },
  },
  {
    name: "mario_algorithm2",
    circuit: {
      wires: 3,
      init: ["0", "0", "0"],
      rows: [
        ["x", "i", "c", "x", "i", "h"],
        ["x", "h", "c", "x", "c", "i"],
        ["x", "i", "x", "x", "h", "c"],
      ],
    },
  },
  {
    name: "tele_algorithm3",
    circuit: {
      wires: 3,
      init: ["0", "0", "0"],
      rows: [
        ["x", "i", "c", "h", "x", "h"],
        ["i", "x", "c", "x", "x", "i"],
        ["i", "i", "x", "i", "x", "c"],
      ],
    },
  },
  {
    name: "tele_algorithm4",
    circuit: {
      wires: 3,
      init: ["0", "0", "0"],
      rows: [
        ["x", "x", "x", "x", "x", "x"],
        ["i", "h", "c", "x", "c", "x"],
        ["i", "i", "x", "i", "h", "x"],
      ],
    },
  },
];
