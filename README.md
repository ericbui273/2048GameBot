# 2048 AI Game Bot
This is an application that allows users to observe an AI bot playing 2048. 

This project is part of the course Algorithms and AI Lab of the Bachelor's Programme in Science, Computer Science study track, at University of Helsinki.
## Documentation
[Specification documentation](https://github.com/ericbui273/2048GameBot/blob/main/Documentations/specificationdocument.md)

[Implementation documentation](https://github.com/ericbui273/2048GameBot/blob/main/Documentations/implementation.md)

[Testing documentation](https://github.com/ericbui273/2048GameBot/blob/main/Documentations/testing.md)

## Weekly report
[Week 1](https://github.com/ericbui273/2048GameBot/blob/main/Weekly%20reports/week1.md)

[Week 2](https://github.com/ericbui273/2048GameBot/blob/main/Weekly%20reports/week2.md)

[Week 3](https://github.com/ericbui273/2048GameBot/blob/main/Weekly%20reports/week3.md)

[Week 4](https://github.com/ericbui273/2048GameBot/blob/main/Weekly%20reports/week4.md)

[Week 5](https://github.com/ericbui273/2048GameBot/blob/main/Weekly%20reports/week5.md)

[Week 6](https://github.com/ericbui273/2048GameBot/blob/main/Weekly%20reports/week6.md)

## User guide
In order to start the application, it is required to have _**Python 3.10+**_ and _**Poetry**_ installed.

Clone the repository to your machine, then start poetry in the root directory of the project with the command

```bash
poetry shell
```

Download the project dependencies with the command

```bash
poetry install --no-root
```

Start the application with the command

```bash
poetry run invoke start
```

After a new window appears, you can choose the optimal level for the AI to play. You can choose default or level 2-5, with the higher level returning smarter move but taking more time. 

Next, you can choose to watch the AI play in continuous mode or step mode, where you press SPACE for the bot to make the next move.

During the game, you can click "New game" to start a new game at the same optimal level and same mode, or click "Back to Menu" to choose another mode and level.
