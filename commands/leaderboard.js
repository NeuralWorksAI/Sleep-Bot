module.exports = {
  name: "leaderboard",
  description: "View the highest active sleep streaks",
  guildOnly: true,
  args: false,
  execute(message, args) {
    message.reply("Leaderboard: \nMichael: 9\nSarah: 4\nJames: 2");
  },
};
