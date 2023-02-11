from discord import Embed, Colour

import json


class MsgEmbed(Embed):
    def __init__(self, x):
        super().__init__()
        self.x = x
        with open('config/embed_msg.json') as embed_msg_file:
            embed_msg = json.load(embed_msg_file)
        
        self.title = embed_msg["title"]
        self.description = embed_msg["description"]

        if bool(embed_msg["use_footer"]):
            self.set_footer(text=embed_msg["footer"])

        if  bool(embed_msg["use_colour"]):
            self.colour = Colour.from_rgb(int(embed_msg["r"]), int(embed_msg["g"]), int(embed_msg["b"]))
        
        for field in embed_msg["fields"]:
            self.add_field(name=field["header"], value=field["text"], inline=bool(field["inline"]))

        