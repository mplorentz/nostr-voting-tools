This is a set of python scripts I wrote to conduct a community vote for the best 2023 #nostripical hackathon project after Nostrica. You can read more details in note1rkqgk0c3p44gkkx32ypu8mw2ezsvfpkhl0vltaz30v3lcde0lgcq7spqkk. I open sourced it for transparency and in case it is useful for others wanting to conduct votes or polls on Nostr.

It is not particularly good python. The gist is that you run hops.py to generate a list of valid voters. For us that was people within 2 hops of the social graph from the hackathon attendees. You can edit the list of participants in hops.py. Then post a root note announcing the vote, and 1 reply for each option. People can then like the replies to vote for them. We let people vote for as many options as they wanted. Then when voting closes you run count_votes.py, replacing rootNote, author, and vote_close_date vars. This will print the number of valid votes for each option.
