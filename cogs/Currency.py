import asyncio
import random

import aiosqlite
import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

shop = {
    "watch" : {
        "price" : 200,
        "sale" : 100
    },
    "computer" : {
        "price" : 2000,
        "sale" : 1000
    },
    "apple" : {
        "price" : 100,
        "sale" : 0
    }
}

class Currency(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def open_account(self, user):
        db = await aiosqlite.connect('currency.db')
        cursor = await db.cursor()
        
        await cursor.execute(f'SELECT user_id FROM main WHERE user_id = {user.id}')
        result1 = await cursor.fetchone()
        if result1 is not None:
            await cursor.execute(f'CREATE TABLE IF NOT EXISTS u{user.id} (item TEXT, amount INT)')
            return False
        else:
            await cursor.execute(f'INSERT INTO main (user_id, wallet, bank, items) VALUES ({user.id}, 0, 0, 0)')
        await cursor.execute(f'CREATE TABLE IF NOT EXISTS u{user.id} (item TEXT, amount INT)')
        await db.commit()
        await cursor.close()
        await db.close()

    async def update_bank(self, user, amt = 0):
        db = await aiosqlite.connect('currency.db')
        cursor = await db.cursor()

        
        await cursor.execute(f'SELECT wallet FROM main WHERE user_id = {user.id}')
        oldamt = await cursor.fetchone()

        await cursor.execute(f'UPDATE main SET wallet = {oldamt[0]+amt} WHERE user_id = {user.id}')
        await db.commit()
        await cursor.close()
        await db.close()
    
    async def get_amt(self, user):
        db = await aiosqlite.connect('currency.db')
        cursor = await db.cursor()

        await cursor.execute(f'SELECT wallet FROM main WHERE user_id = {user.id}')
        walamt = await cursor.fetchone()
        
        await cursor.execute(f'SELECT bank FROM main WHERE user_id = {user.id}')
        bankamt = await cursor.fetchone()

        return walamt, bankamt

    @commands.command(aliases=['bal'])
    async def balance(self, ctx):
        await self.open_account(ctx.author)
        walamt, bankamt = await self.get_amt(ctx.author)
        embed = discord.Embed(
            title=f"{ctx.author.name}'s Balance",
            colour=ctx.author.colour
        )
        embed.add_field(name="Wallet Amount:", value=f"{walamt[0]} moners")
        embed.add_field(name="Bank Amount:", value=f"{bankamt[0]} moners")
        embed.add_field(name="Total:", value=f"{bankamt[0]+walamt[0]} moners")
        await ctx.send(embed=embed)
    
    @commands.command(aliases=['dep'])
    async def deposit(self, ctx, amt):
        db = await aiosqlite.connect('currency.db')
        cursor = await db.cursor()
        walamt, bankamt = await self.get_amt(ctx.author)
        await self.open_account(ctx.author)
        if amt == "all":
            await cursor.execute(f'UPDATE main SET wallet = 0 WHERE user_id = {ctx.author.id}')
            await cursor.execute(f'UPDATE main SET bank = {walamt[0]+bankamt[0]} WHERE user_id = {ctx.author.id}')
            await ctx.send(f"{walamt[0]} moners have been deposited to your bank.")
        elif int(amt)>walamt[0]:
            await ctx.send("You don't have enough moners in your wallet to deposit that much!")
        elif int(amt)<0:
            await ctx.send("You cannot deposit negative numbers!")
        else:
            await cursor.execute(f'UPDATE main SET wallet = {walamt[0]-int(amt)} WHERE user_id = {ctx.author.id}')
            await cursor.execute(f'UPDATE main SET bank = {int(amt)+bankamt[0]} WHERE user_id = {ctx.author.id}')
            await ctx.send(f'{int(amt)} moners have been deposited to your bank.')
        await db.commit()
        await cursor.close()
        await db.close()

    @commands.command(aliases=["with"])
    async def withdraw(self, ctx, amt):
        db = await aiosqlite.connect('currency.db')
        cursor = await db.cursor()
        walamt, bankamt = await self.get_amt(ctx.author)
        await self.open_account(ctx.author)
        if amt == "all":
            await cursor.execute(f'UPDATE main SET bank = 0 WHERE user_id = {ctx.author.id}')
            await cursor.execute(f'UPDATE main SET wallet = {walamt[0]+bankamt[0]} WHERE user_id = {ctx.author.id}')
            await ctx.send(f"{bankamt[0]} moners have been withdrawn your bank.")
        elif int(amt)>bankamt[0]:
            await ctx.send("You don't have enough moners in your bank to withdraw that much!")
        elif int(amt)<0:
            await ctx.send("You cannot withdraw negative numbers!")
        else:
            await cursor.execute(f'UPDATE main SET wallet = {walamt[0]+int(amt)} WHERE user_id = {ctx.author.id}')
            await cursor.execute(f'UPDATE main SET bank = {bankamt[0]-int(amt)} WHERE user_id = {ctx.author.id}')
            await ctx.send(f'{int(amt)} moners have been withdrawn from your bank.')
        await db.commit()
        await cursor.close()
        await db.close()

    @commands.command()
    async def buy(self, ctx, item, quantity=1):
        db = await aiosqlite.connect('currency.db')
        cursor = await db.cursor()
        check = shop.get(item)

        await self.open_account(ctx.author)
        if quantity < 1:
            await ctx.send("You can't buy a negative quantity of items. Use `cb sell` for that!")
            return
        
        if check is not None:
            price = shop[item].get('price')
            await cursor.execute(f"SELECT amount FROM u{ctx.author.id} WHERE item = '{item}'")
            check1 = await cursor.fetchone()
            walamt, bankamt = await self.get_amt(ctx.author)
            if walamt[0] + bankamt[0] < price*quantity:
                    await ctx.send("You don't have enough money to make that purchase.")
            elif walamt[0] < price*quantity:
                await ctx.send("You need to withdraw some bank money to make this purchase.")
            else:
                if check1 is not None:
                    await cursor.execute(f"UPDATE u{ctx.author.id} SET amount = {check1[0] + quantity} WHERE item = '{item}'")
                if check1 is None:
                    await cursor.execute(f"INSERT INTO u{ctx.author.id} (item, amount) VALUES ('{item}', {quantity})")
                await cursor.execute(f'UPDATE main SET wallet = {walamt[0] - quantity*price} WHERE user_id = {ctx.author.id}')
                await ctx.send(f"You just bought {quantity} {item}s for {price*quantity}")   
        else:
            await ctx.send("You must specify a valid item or item ID.")
        await db.commit()
        await cursor.close()
        await db.close()

    @commands.command()
    async def sell(self, ctx, item, quantity=1):
        db = await aiosqlite.connect('currency.db')
        cursor = await db.cursor()
        check0 = shop.get(item)
        if check0 is None:
            await ctx.send("That item doesn't exist.")
            return
        sale = shop[item].get('sale')
        await cursor.execute(f"SELECT item FROM u{ctx.author.id} WHERE item = '{item}'")
        check = await cursor.fetchone()
        await cursor.execute(f"SELECT amount FROM u{ctx.author.id} WHERE item = '{item}'")
        check1 = await cursor.fetchone()
        print(sale)
        print(check0)
        print(check1)
        print(check)
        if check is None:
            await ctx.send("You don't own that item.")
            return
        else:
            if quantity < 1:
                await ctx.send("You can't sell a negative number of items. Use the buy command for that!")
            elif quantity > check1[0]:
                await ctx.send(f"You don't have that many {item}s to sell.")
            else:
                await cursor.execute(f"UPDATE u{ctx.author.id} SET amount = {check1[0] - quantity} WHERE item = '{item}'")
                await self.update_bank(ctx.author, sale)
                await ctx.send(f"You just sold {quantity} {item}s and gained {sale*quantity}")
        await db.commit()
        await cursor.close()
        await db.close()

    @commands.command()
    @commands.cooldown(1, 15, BucketType.user)
    async def beg(self, ctx):
        await self.open_account(ctx.author)
        amt = random.randint(1, 100)
        people = ['Phil Swift', 'Hugh Jass', 'Mike Oxlong', 'UnsoughtConch', 'That bitch stacy',
                'Your grumpy old neighbor', 'Jerk Mehoff', 'That one kid from school who only showers once a month', 'I',
                'Jeff Bezos', 'Bobby', 'Garret Bobby Ferguson']

        await self.update_bank(ctx.author, amt)
        await ctx.send(f"{random.choice(people)} gave you {amt} coins!")
    
    @commands.command()
    @commands.cooldown(1, 15, BucketType.user)
    async def slots(self, ctx, amt):
        # TEMP: 4% chance of getting the mega jackpot!
        await self.open_account(ctx.author)
        walamt, bankamt = await self.get_amt(ctx.author)
        totalamt = walamt[0]+bankamt[0]
        amt = int(amt)

        if amt>totalamt:
            await ctx.send("You don't have that many moners!")

        elif amt>walamt[0]:
            await ctx.send("You need to withdraw some bank money to bet that much on slots!")

        elif amt<0:
            await ctx.send("You can't bet negative moners.")

        else:
            final = []
            for i in range(3):
                a = random.choice([":fire:","<:Conch:741462553846087721>", ":heart:",":middle_finger:",":smiling_imp:"])
                final.append(a)

            if final[0] == final[1] == final[2] == "<:Conch:741462553846087721>":
                embed = discord.Embed(
                    title=f"{ctx.author.name}'s Slot Game",
                    colour=discord.Colour.gold()
                )
                embed.add_field(name="Result:", value=str(final), inline=False)
                embed.add_field(name="Jackpot!", value="You hit the jackpot!", inline=False)
                embed.add_field(name="Amount Won:", value=f"{amt*10} moners!", inline=False)
                await ctx.send(embed=embed)
                await self.update_bank(ctx.author, amt*10)

            elif final[0] == final[1] == final[2]:
                embed = discord.Embed(
                    title=f"{ctx.author.name}'s Slot Game",
                    colour=discord.Colour.green()
                )
                embed.add_field(name="Result:", value=str(final), inline=False)
                embed.add_field(name="Three in a row!", value="You got three of the same emoji!", inline=False)
                embed.add_field(name="Amount Won:", value=f"{amt*5} moners!", inline=False)
                await ctx.send(embed=embed)
                await self.update_bank(ctx.author, amt*5)

            elif final[0] == final[1] or final[1] == final[2]:
                embed = discord.Embed(
                    title=f"{ctx.author.name}'s Slot Game",
                    colour=discord.Colour.green()
                )
                embed.add_field(name="Result:", value=str(final), inline=False)
                embed.add_field(name="Amount Won:", value=f"{amt*2} moners!", inline=False)
                await ctx.send(embed=embed)
                await self.update_bank(ctx.author, amt*2)

            else:
                embed = discord.Embed(
                    title=f"{ctx.author.name}'s Slot Game",
                    colour=discord.Colour.red()
                )
                embed.add_field(name="Result:", value=str(final), inline=False)
                embed.add_field(name="You lost!", value="You did not get any matching emoji that align :(", inline=False)
                embed.add_field(name="Amount Lost:", value=f"{amt} moners.", inline=False)
                await ctx.send(embed=embed)
                await self.update_bank(ctx.author, amt*-1)

    @commands.command()
    @commands.cooldown(1, 86400, BucketType.user)
    async def daily(self, ctx):
        await self.open_account(ctx.author)
        await self.update_bank(ctx.author, 200)

        embed = discord.Embed(
            title="Daily Moners",
            colour=ctx.author.colour
        )
        embed.add_field(name="200 moners have been placed in your wallet.", value="Come back tomorrow for more moners.")
        await ctx.send(embed=embed)

    @deposit.error
    async def deposit_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You must specify an amount you want to deposit.")

    @withdraw.error
    async def withdraw_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to specify an amount you would like to withdraw.")

    @buy.error
    async def buy_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Your amount must be an integer!")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to specify an item to buy.")
        else:
            print(error)

    @beg.error
    async def beg_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"Woah there pal! You gotta wait **{int(error.retry_after)}** seconds.")

    @slots.error
    async def slots_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You must specify an amount of moners to bet.")
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"Woah there pal! You gotta wait **{int(error.retry_after)}** seconds.")

    @daily.error
    async def daily_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            m, s = divmod(error.retry_after, 60)
            h, m = divmod(m, 60)
            if int(h) == 0 and int(m) == 0:
                em = discord.Embed(title="**Woah there pal!**", description=f'Come back in {int(s)} seconds to collect more daily moners!', colour=discord.Colour.red())
                await ctx.send(embed=em)
            elif int(h) == 0 and int(m) != 0:
                em = discord.Embed(title="**Woah there pal!**", description=f'Come back in {int(m)} minutes and {int(s)} seconds to collect more daily moners!', colour=discord.Colour.red())
                await ctx.send(embed=em)
            else:
                em = discord.Embed(title="**Woah there pal!**", description=f'Come back in {int(h)} hours, {int(m)} minutes and {int(s)} seconds to collect more daily moners!', colour=discord.Colour.red())
                await ctx.send(embed=em)

def setup(client):
    client.add_cog(Currency(client))
