class Blacklisted(Exception):
    def __init__(self,ctx):
        self.ctx = ctx
    
    async def memsend(self):
        await self.ctx.send("You are blacklisted from using ConchBot.")
    
    async def guildsend(self):
        await self.ctx.send("This guild is blacklisted from using ConchBot.")

class VoteLockedCmd(Exception):
    def __init__(self,ctx):
        self.ctx = ctx
    
    async def send(self):
        await self.ctx.send("The three latest image generation commands are vote locked! You can either wait for "
        "them to become available or vote for ConchBot at (<https://bit.ly/2PiLbwh>)!")