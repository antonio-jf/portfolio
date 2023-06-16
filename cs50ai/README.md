# CS50ai
A subdirectory for my [cs50ai](https://cs50.harvard.edu/ai/2020/) code.

## What is CS50ai?
CS50ai is an intermediate Harvard online course focused on teaching Artificial Intelligence fundamentals with Python through lectures and a fully fledged seven-week program.
After every weekly lecture there are program implementations a course-taker is expected to be able to solve which include concepts seen in the lectures, as well as some aditional concepts related to the content.

## What can you find in this subdirectory?
Basically, here you can find my solutions for CS50ai's problems.
A brief description of what each code does is found below. Feel free to move around and browse each of the subdirectories and take a look at the code.

<p align="center">
  <img src="figs/ai_work.jpg" />
</p>

### Week 0
- In [`degrees`](wk0/degrees) you can find code created for a breadth-first search algorithm which has the main goal of iterating over movies and finding a link between two people by means of the people they have co-starred with. 
- In [`tictactoe`](wk0/tictactoe) the main goal of the program is to implement a tictactoe-playing AI algorithm which is impossible to beat.
### Week 1
- In [`knights`](wk1/knights) the task was to knowledge-engineer a series of logical sentences so as to help an AI understand how to classify a series of Knights and Knaves.
- In [`minesweeper`](wk1/minesweeper) an AI has been implemented to play minesweeper on its own, beating the game according to knowledge that is being acquired as it progresses. 
### Week 2
- [`heredity`](wk2/heredity) is a program that takes a document full of people and its genetic characteristics and calculates the probabilities that the structure observed is true, according to a series of conditional probabilities.
- Continuing with probability, [`pagerank`](wk2/pagerank) takes a corpus of webpages and calculates the probability that an agent ends in one of the webpages at any given point, according to the amount of links to that page, as well as some other conditions.
### Week 3
- [`crossword`](wk3/crossword) is an app that takes a `.txt` representation of a crossword and desciphers, according to a document filled with words, which combination suits the crossword, printing it after conclusion.
### Week 4
- [`nim`](wk4/nim) is also a game-playing AI which is trained heavily to play the famous game *Nim* according to a reinforcement learning algorithm known as `Q-learning`,  which rewards the AI for winning and punishes it for losing.
- For [`shopping`](wk4/shopping) a dataset containing information about website visitors is used in order to train a model and predict, according to a `K-NearestNeighbors` algorithm, which users made a purchase and which ones didn't.
### Week 5
- In [`traffic`](wk5/traffic) a convolutional neural network was created and trained with several traffic sign images in order to be able to classify a test dataset of traffic signs according to the category they belong to.

### Week 6
- [`parser`](wk6/parser) is a program that tries to understand the underlying structure behind a bunch of sentences given a set of semantic and syntax rules represented as trees using the [Natural language Toolkit](https://www.nltk.org/_modules/nltk/tree.html), `nltk`, module.
- [`questions`](wk6/questions) takes a query from the user and searches over a series of documents contained in a corpus the top n sentences it deems most suitable for answering the query.
