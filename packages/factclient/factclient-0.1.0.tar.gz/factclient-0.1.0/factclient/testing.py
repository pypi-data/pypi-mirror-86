from factclient.fact import Fact

from  factclient.io.TCPSender import TCPSender

io = TCPSender()
Fact.boot({"inlcudeEnvironment": False, "io": io, "send_on_update": True})
Fact.start(None, None)
Fact.update(None, "test updating", {1: "no no no"})
Fact.done(None, "test done", ["jo", "args"])

