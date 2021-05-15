import discord
from discord.ext import commands
import aiosqlite
import uuid
import datetime


class Tags(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def create_table(self, id):
        db = await aiosqlite.connect("db/tags.db")
        cursor = await db.cursor()

        await cursor.execute(f"CREATE TABLE IF NOT EXISTS g{id} (name TEXT, content TEXT, creator_id INT, created_at TEXT"
        ", last_edited TEXT, tag_id TEXT)")

    async def check_existance(self, name, guild):
        db = await aiosqlite.connect("db/tags.db")
        cursor = await db.cursor()

        await cursor.execute(f"SELECT name FROM g{guild} WHERE name = '{name.lower()}'")
        result = await cursor.fetchone()

        if result is None:
            return False
        else:
            return True

    async def edit_info(self, guild, name, column, info):
        today = datetime.date.today()
        d2 = today.strftime("%B %d, %Y")
        db = await aiosqlite.connect("db/tags.db")
        cursor = await db.cursor()

        await cursor.execute(f"UPDATE g{guild} SET {column} = '{info}' WHERE name = '{name}'")
        await cursor.execute(f"UPDATE g{guild} SET last_edited = '{d2}' WHERE name = '{name}'")
        
        await db.commit()
        await cursor.close()
        await db.close()

    @commands.group(invoke_without_command=True, aliases=['tags'])
    async def tag(self, ctx, content, *, val1=None):
        db = await aiosqlite.connect("db/tags.db")
        cursor = await db.cursor()
        await self.create_table(ctx.guild.id)

        if content.lower() == "create":
            if val1 is None:
                await ctx.send("You must specify a name for your tag.")
            else:
                try:
                    name, content = val1.split(",")
                except:
                    await ctx.send("You must separate your values by a comma.")
                    return
                today = datetime.date.today()
                d2 = today.strftime("%B %d, %Y")
                db = await aiosqlite.connect("db/tags.db")
                cursor = await db.cursor()
                await self.create_table(ctx.guild.id)

                check = await self.check_existance(name, ctx.guild.id)
                
                if check is True:
                    await ctx.send("That tag already exists!")
                    return
                
                id = uuid.uuid4()

                await cursor.execute(f"INSERT INTO g{ctx.guild.id} (name, content, creator_id, created_at, last_edited, tag_id)"
                f" VALUES ('{name.lower()}', '{content}', {ctx.author.id}, '{d2}', '{d2}', '{id}')")

                await ctx.send(f"Tag {name} successfully created with tag ID {id}")

        elif content.lower() == "delete":
            if val1 is None:
                await ctx.send("You must provide a valid ID to delete a tag.")
            else:
                await cursor.execute(f"SELECT creator_id FROM g{ctx.guild.id} WHERE tag_id = '{val1}'")
                result = await cursor.fetchone()

                if result is None:
                    await ctx.send("Invalid tag ID.")
                elif int(result[0]) == int(ctx.author.id) or ctx.author.has_permissions(manage_messages=True):
                    await cursor.execute(f"DELETE FROM g{ctx.guild.id} WHERE tag_id = '{val1}'")
                    await ctx.send(f"Successfully deleted tag `{val1}`.")
                else:
                    tagcreator = self.client.get_user(result[0])
                    await ctx.send(f"You can't delete a tag that isn't yours! This tag belongs to {tagcreator}!")

        elif content.lower() == "edit":
            try:
                name, content = val1.split(',')
                print(content)
                print(name)
            except:
                await ctx.send("You have to tell us what you want to edit it into.")
                return
            await cursor.execute(f"SELECT creator_id FROM g{ctx.guild.id} WHERE name = '{name.lower()}'")
            result = await cursor.fetchone()

            if val1 is None:
                await ctx.send("You must provide a tag name to edit.")
                return
            
            if int(result[0]) == int(ctx.author.id):
                await cursor.execute(f"SELECT name FROM g{ctx.guild.id} WHERE name = '{name.lower()}'")
                status = await cursor.fetchone()

                if status is None:
                    await ctx.send("Invalid tag provided.")
                else:
                    await self.edit_info(ctx.guild.id, name, "content", content)
                    await ctx.send("Tag successfully edited.")
            else:
                tagcreator = self.client.get_user(result[0])
                await ctx.send(f"You can't edit a tag that isn't yours! This tag belongs to {tagcreator}!")

        else:
            status = await self.check_existance(content, ctx.guild.id)
            
            if status is False:
                await ctx.send("Tag not found.")

            else:
                await cursor.execute(f"SELECT content FROM g{ctx.guild.id} WHERE name = '{content}'")
                result = await cursor.fetchone()

                await ctx.send(result[0])

        await db.commit()
        await cursor.close()
        await db.close()
    
def setup(client):
    client.add_cog(Tags(client))