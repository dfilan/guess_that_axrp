# Guess that AXRP

A guessing game: the game randomly picks an AXRP episode, randomly picks a sentence in that episode, presents the user with the sentence, and the user has to guess what episode it's from.

They can do this multiple times, and optimally submit to a leaderboard.

Things that still need to be done (bolded things will teach me stuff):
  - **Deal with github API not giving me stuff**
    - Add github deets to the instance so that I get less rate-limited?
  - **Auto-update the DB**
  - Show URL of episode
  - **That type of field where the user types a search term in a box to go down a list**
  - Test I've correctly started the episode db
  - Button to reset session
  - Get right answer not stored in user cookies
    - Could store it in a database with the UUID
  - Reset session when you submit your score (so you can't submit multiple times)
    - or otherwise do something so you can't submit multiple times
  - **Figure out why render keeps nuking my database each time I push to github**
    - Ah I figured it out
    - Could add a disk or move to PostgreSQL
    - Moving to PostgreSQL would teach me more
  - Create section saying what stuff I used / stole from
    - GitHub repo
    - Flask tutorial
    - Render
    - [bestmotherfucking.website](https://bestmotherfucking.website/)
  - **Deal with people visiting leaderboard.submit or guess.result without playing**
  - Store sentences in database rather than making them whenever someone wants another guess
