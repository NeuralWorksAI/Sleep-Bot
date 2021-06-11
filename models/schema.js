const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const schema = new Schema({
  username: {
    type: String,
    required: true,
  },
  activestreak: {
    type: Number,
    default: 0,
  },
  timezone: {
    type: String,
    default: "UTC",
  },
  start: {
    type: String,
  },
  finish: {
    type: String,
  },
});

const Users = mongoose.model("Main", schema);

module.exports = Users;
