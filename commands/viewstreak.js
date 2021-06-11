module.exports = {
  name: "mystreak",
  description: "View your current sleep streak",
  guildOnly: true,
  args: false,
  execute(message, args) {
    message.reply("Your current streak is, 0");
  },
};
