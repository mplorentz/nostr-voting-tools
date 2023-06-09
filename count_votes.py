from nostr.relay_manager import RelayManager
from nostr.key import PrivateKey, PublicKey
from nostr.filter import Filter, Filters
from nostr.event import EventKind
import time
import threading
import sys

rootNote = "1d808b3f110d6a8b58d15103c3edcac8a0c486d7fbd9f5f4517b23fc372ffa30"
author = "0f22c06eac1002684efcc68f568540e8342d1609d508bcd4312c038e6194f8b6"
vote_close_date = 1680019200

voters = set()

with open('voters.txt','r') as f:
    voters = eval(f.read())

relay_manager = RelayManager()
relay_manager.add_relay("wss://nos.lol")
relay_manager.add_relay("wss://relay.damus.io")
relay_manager.add_relay("wss://nostr-pub.wellorder.net")
relay_manager.add_relay("wss://relay.snort.social")
relay_manager.add_relay("wss://relay.nostr.band")
relay_manager.add_relay("wss://eden.nostr.land")
relay_manager.add_relay("wss://relay.current.fyi")
relay_manager.add_relay("wss://brb.io")
relay_manager.add_relay("wss://nostr.oxtr.dev")
relay_manager.add_relay("wss://relay.nostr.bg")
relay_manager.add_relay("wss://no.str.cr")
relay_manager.add_relay("wss://nostr.mom")
relay_manager.add_relay("wss://nostr.zebedee.cloud")
relay_manager.add_relay("wss://relay.plebstr.com")
relay_manager.add_relay("wss://offchain.pub")

project_notes_filter = Filter(kinds=[EventKind.TEXT_NOTE], event_refs=[rootNote], authors=[author])
subscription = Filters([project_notes_filter])
relay_manager.add_subscription_on_all_relays("replies", subscription)
print("requesting replies to root note: ", rootNote)
time.sleep(1.25)

project_notes = []
vote_events = []

while relay_manager.message_pool.has_events():
    event = relay_manager.message_pool.get_event().event
    if event.public_key == author:
        print("found reply: ", event.id, event.content.partition("\n")[0])
        project_notes.append(event)

relay_manager.close_subscription_on_all_relays("replies")

for note in project_notes:
    voter_like_count = 0
    likes_filter = Filter(kinds=[EventKind.LIKE], event_refs=[note.id])
    relay_manager.add_subscription_on_all_relays(note.id, Filters([likes_filter]))
    time.sleep(1.25)
    already_voted = set()
    while relay_manager.message_pool.has_events():
        event = relay_manager.message_pool.get_event().event
        if event.created_at > vote_close_date or event in vote_events:
            continue
        vote_events.append(event)
        etags = list(filter(lambda t: t[0] == "e", event.tags))
        referenced_event = etags[-1][1]
        if referenced_event != note.id:
            continue
        if event.public_key in voters and event.public_key not in already_voted:
            voter_like_count += 1
            already_voted.add(event.public_key)
    relay_manager.close_subscription_on_all_relays(note.id)
    print("found ", voter_like_count, " votes for ", note.content.partition("\n")[0])

with open('votes.txt','w') as f:
    f.write(str(vote_events))  # set of numbers & a tuple
    
print("done")
sys.exit()