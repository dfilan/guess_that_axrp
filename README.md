# Guess that AXRP

A guessing game: the game randomly picks an AXRP episode, randomly picks a sentence in that episode, presents the user with the sentence, and the user has to guess what episode it's from.

They can do this multiple times, and optimally submit to a leaderboard.

Things that still need to be done (bolded things will teach me stuff):
  - Show URL of episode
  - **That type of field where the user types a search term in a box to go down a list**
  - Test I've correctly started the episode db
  - Get right answer not stored in user cookies
    - Could store it in a database with the UUID
    - or could encrypt it in the cookies
  - Reset session when you submit your score (so you can't submit multiple times)
    - or otherwise do something so you can't submit multiple times
  - Deal with key errors without breaking the user experience.

## Credits
  - The design of this website was heavily based off of the [Flask tutorial](https://flask.palletsprojects.com/en/3.0.x/tutorial/).
  - It is being run on [Render](https://render.com/).
  - The stylesheet was taken from [bestmotherfucking.website](https://bestmotherfucking.website/).
