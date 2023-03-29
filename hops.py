from nostr.relay_manager import RelayManager
from nostr.key import PrivateKey, PublicKey
from nostr.filter import Filter, Filters
from nostr.event import EventKind
import time
import threading
import sys

hackathon_participants = set([
"npub1pez4lttr28mhfdzx3047wt4j7qzgkh2asjuxa6626rzdrkk39ggqe0xdvg",
"npub14ps5krdd2wezq4kytmzv3t5rt6p4hl5tx6ecqfdxt5y0kchm5rtsva57gc",
"npub1uaajg6r8hfgh9c3vpzm2m5w8mcgynh5e0tf0um4q5dfpx8u6p6dqmj87z6",
"npub1uucu5snurqze6enrdh06am432qftctdnehf8h8jv4hjs27nwstkshxatty",
"npub1wmr34t36fy03m8hvgl96zl3znndyzyaqhwmwdtshwmtkg03fetaqhjg240",
"npub16zsllwrkrwt5emz2805vhjewj6nsjrw0ge0latyrn2jv5gxf5k0q5l92l7",
"npub1lur3ft9rk43fmjd2skwefz0jxlhfj0nyz3zjfkxwe3y8xlf5r6nquat0xg",
"npub1x2e2s7us27zf5tvzl7k4xetgk2jl93y7hdk29zg32spkxqs9fjgs6q3dt6",
"npub1vp8fdcyejd4pqjyrjk9sgz68vuhq7pyvnzk8j0ehlljvwgp8n6eqsrnpsw",
"npub1q3tgrnudgaqnjp8lvs5h20ndtfq7qh5dn4gdh48vqyjnsrvgduasje52tq",
"npub1z9n5ktfjrlpyywds9t7ljekr9cm9jjnzs27h702te5fy8p2c4dgs5zvycf",
"npub1uucu5snurqze6enrdh06am432qftctdnehf8h8jv4hjs27nwstkshxatty",
"npub1k7cnst4fh4ajgg8w6ndcmqen4fnyc7ahhm3zpp255vdxqarrtekq5rrg96",
"npub1aq69ynhpgxhncd47ml4dqfgdcs374vwn6g67axsuyt4u49ql84tqqw3pts",
"npub1vp8fdcyejd4pqjyrjk9sgz68vuhq7pyvnzk8j0ehlljvwgp8n6eqsrnpsw",
"npub1dcl4zejwr8sg9h6jzl75fy4mj6g8gpdqkfczseca6lef0d5gvzxqvux5ey",
"npub1qqmqhp7j0q0dx43wh2lf50p0dhkcwt3d9huufmmdvvvahrlyqz8q402vng",
"npub1q3tgrnudgaqnjp8lvs5h20ndtfq7qh5dn4gdh48vqyjnsrvgduasje52tq",
"npub1m3zv8cvsxyxk2pdekzl6wj4p2t8vf4pwsd52z660mpw5q98gwn2qku63z0",
"npub1z9n5ktfjrlpyywds9t7ljekr9cm9jjnzs27h702te5fy8p2c4dgs5zvycf",
"npub1z3gdcd5zp0z0fudczjf4grlrkga6ls3yhgr54ph78ufm5lkteywsfmcayu",
"npub1qd0smfnmu8936edjx3maet6rckw80wz36jdf6a4lj2gn6ayq2m3q76lelz",
"npub12zpfs3yq7we83yvypgsrw5f88y2fv780c2kfs89ge5qk6q3sfm7spks880",
"npub12zpfs3yq7we83yvypgsrw5f88y2fv780c2kfs89ge5qk6q3sfm7spks880",
"npub1lunaq893u4hmtpvqxpk8hfmtkqmm7ggutdtnc4hyuux2skr4ttcqr827lj",
"npub1a7n2h5y3gt90y00mwrknhx74fyzzjqw25ehkscje58x9tfyhqd5snyvfnu",
"npub1ruj546gf5d4sqqxrk68ndwf245tg73fjwfwhekdk0adsjzy0yyjsrzsqw2",
"npub1v4j3007xt2wy40ydx3tzug290xjv9e5czg5cxda277klxfcjmj5ql6t2c6",
"npub1k7cnst4fh4ajgg8w6ndcmqen4fnyc7ahhm3zpp255vdxqarrtekq5rrg96",
"npub1qv0nc6gxr80sgredulxm7g6zm6z9gp4ns9nudq6mfxq0ed87gsnq7wswaz",
])

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


all_voters = set()

def get_follow_list_npub(npub):
    user_pub_key = PublicKey.from_npub(npub).hex()
    get_follow_list_hex(user_pub_key)

def get_follow_list_hex(user_pub_key):
    all_voters.add(user_pub_key)
    filters_pm = Filter(kinds=[EventKind.CONTACTS], authors=[user_pub_key])
    subscription = Filters([filters_pm])
    relay_manager.add_subscription_on_all_relays(user_pub_key, subscription)
    time.sleep(1.25)

    while relay_manager.message_pool.has_events():
        event_msg = relay_manager.message_pool.get_event()
        for tag in event_msg.event.tags:
            if tag[0] == "p":
                all_voters.add(tag[1])

    relay_manager.close_subscription_on_all_relays(user_pub_key)

        
print("searching for 1 hops for " + str(len(hackathon_participants)) + " profiles")
i = 0
for npub in hackathon_participants:
    print("Getting contact list for profile ", i, ",", npub)
    get_follow_list_npub(npub)
    i += 1

print("searching for two hops for " + str(len(all_voters)) + " profiles")
i = 0
one_hop = all_voters.copy()
for hex in one_hop:
    print("Getting contact list for profile ", i, ",", hex)
    get_follow_list_hex(hex)
    i += 1
    
relay_manager.close_all_relay_connections()
relay_manager = None

print("finished. Writing.")
    
with open('voters.txt','w') as f:
    print("found ", len(all_voters), " voters")
    f.write(str(all_voters))  # set of numbers & a tuple
