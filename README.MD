# JoJoBot
## About JoJoBot
JoJoBot is 'JoJo's bizarre adventure' themed discord bot made with pycord that I decided to create ages ago. It went through many revisions in my early days of programming, but now I've finally learned enough about Object-Oriented Programming to create a readable, extensible and fast version of this project.

I'm excited to launch this when it is ready so, for tracking's sake, I'm going to upload my development to this git repository to keep track of where I'm at and also to move the code between machines.

JoJoBot works on a system where a user will obtain a stand randomly (5 resets are allowed if it is an undesirable one, such as Holly's stand or Cheap Trick) and level up through sending messages. As they level up, they will unluck new moves, or even ACTs, that they can use in combat against other users. Currently, the combat system is not turn based, relying on users enabling and disabling "battle mode", which dictates whether or not other users can attack them and if they can attack other users. With this, a user could attack another user twice in a row, but some moves have heavy downsides to using multiple times a row, such as decreasing your accuracy, damage, health or even experience. There are plans to eventually add a timer for moves to stop users from spamming moves to win a fight instantly, and to later on add a 'turn based' command to start a turn based battle with another user, if that's what they prefer.

## What's new?
In this new version, I've taken a different approach to how the bot is structured. I learned more about object oriented programming and about discord.py/pycord after I created the first three versions. With this version, there is a series of dictionaries in JSON files and in classes within Python files. The stand list contains a stand's name, moveset, type and when they change to a new ACT (if they do). There is also a JSON file containing user information and two Python files that deal with moves. The big change here is that, instead of trying to fit every move's code within the code of the `/move` command, in the moves dictionary, each move contains a sub-entry that holds the method that the move runs, so that each move has it's individual function written and encapsulated within a `movefunctions.py` file.

## Dependencies
**Add later**

# This project is on hold :(
