# app/activitypub/actor.py

class Actor:
    def __init__(self, id, type, inbox, outbox, public_key):
        self.id = id
        self.type = type
        self.inbox = inbox
        self.outbox = outbox
        self.public_key = public_key

    def to_dict(self):
        return {
            "@context": "https://www.w3.org/ns/activitystreams",
            "id": self.id,
            "type": self.type,
            "inbox": self.inbox,
            "outbox": self.outbox,
            "publicKey": {
                "id": f"{self.id}#main-key",
                "owner": self.id,
                "publicKeyPem": self.public_key
            }
        }

    # Add methods for signing/verifying interactions
