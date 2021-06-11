const Users = require("../models/schema.js");

// test
const users = new Users({
  username: "test",
  timezone: "GMT",
  start: "2300",
  finish: "0500",
});

module.exports = {
  name: "setsleep",
  description:
    "Setup sleeping times. Format is in 24 clock, for example: setsleep 2300 0500",
  guildOnly: true,
  args: true,
  usage: "<start sleep> <wake up>",
  execute(message, args) {
    users
      .save()
      .then((result) => {
        console.log(result);
      })
      .catch((err) => {
        console.log(err);
      });
    message.channel.send("Test");
  },
};
