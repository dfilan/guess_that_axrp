# Guess that AXRP

A guessing game: the game randomly picks an AXRP episode, randomly picks a sentence in that episode, presents the user with the sentence, and the user has to guess what episode it's from.

They can do this multiple times, and optimally submit to a leaderboard.

Things that still need to be done (bolded things will teach me stuff):
  - **Auto-update the DB**
    - use github webhook???
    - conditional requests to check if things have been modified?
  - Show URL of episode
  - **That type of field where the user types a search term in a box to go down a list**
  - Test I've correctly started the episode db
  - Button to reset session
  - Get right answer not stored in user cookies
    - Could store it in a database with the UUID
  - Reset session when you submit your score (so you can't submit multiple times)
    - or otherwise do something so you can't submit multiple times
  - Create section saying what stuff I used / stole from
    - GitHub repo
    - Flask tutorial
    - Render
    - [bestmotherfucking.website](https://bestmotherfucking.website/)
  - Deal with key errors without breaking the user experience.
