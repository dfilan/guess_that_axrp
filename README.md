# Guess that AXRP

A guessing game: the game randomly picks an AXRP episode, randomly picks a sentence in that episode, presents the user with the sentence, and the user has to guess what episode it's from.

They can do this multiple times, and optimally submit to a leaderboard.

Things I need to do to make this happen:
- Make a database of AXRP episodes that updates when I upload more of them. (Or maybe just dynamically get the list each time? Or update the whole list every day?)
- User interaction
- That type of field where the user types a search term in a box to go down a list
- Implement a leaderboard, user interaction with the leaderboard
- Figure out how much of this can be done on Render+Flask (presumably I can have a little database? and presumably Flask has some way for me to run a thing repeatedly)

So I guess I'll just sort of go thru the flask tutorial but do it the way i think makes most sense?

TODO write test to check that I correctly started the episode db
