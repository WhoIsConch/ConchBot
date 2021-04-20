class Blacklisted(Exception):
    def __init__(self,ctx):
        self.ctx = ctx
    
    async def memsend(self):
        await self.ctx.send("You are blacklisted from using ConchBot.")
    
    async def guildsend(self):
        await self.ctx.send("This guild is blacklisted from using ConchBot.")