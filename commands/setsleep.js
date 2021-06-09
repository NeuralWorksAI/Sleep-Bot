module.exports = {
  name: "setsleep",
  description:
    "Setup sleeping times. Format is in 24 clock, for example: setsleep 2300 0500",
  args: true,
  usage: "<start sleep> <wake up>",
  execute(message, args) {
    message.channel.send("Test");
  },
};
