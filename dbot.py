import discord
from discord.ext import commands
from scraper import scrape_shoes
import os
from dotenv import load_dotenv
import requests

class ShoeBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()  # Enable all intents
        super().__init__(command_prefix='!', intents=intents)

    async def on_ready(self):
        print(f'Bot is ready! Logged in as {self.user}')
        try:
            await self.add_cog(ShoeCog(self))
            print("ShoeCog loaded successfully")
        except Exception as e:
            print(f"Error loading ShoeCog: {e}")

class ShoeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("ShoeCog initialized")

    @commands.Cog.listener()
    async def on_ready(self):
        print("ShoeCog is ready!")

    @commands.command()
    async def test(self, ctx):
        """Simple test command"""
        await ctx.send("Bot is working!")

    @commands.command()
    async def shoes(self, ctx, search_type: str, *, query: str):
        """Search for shoes by brand or price"""
        await ctx.send(f"Received command: {search_type} with query: {query}")
        try:
            search_params = {}
            if search_type.lower() == 'brand':
                search_params['brand'] = query
            elif search_type.lower() == 'price':
                search_params['price'] = float(query)
            else:
                await ctx.send("Please use either 'brand' or 'price' as search type")
                return

            await ctx.send("Searching for shoes... Please wait.")
            results = scrape_shoes(search_params)

            if not results:
                await ctx.send("No matching shoes found.")
                return

            for item in results:
                embed = discord.Embed(title=item['name'], color=discord.Color.blue())
                embed.add_field(name="Price", value=f"${item['price']}", inline=True)
                if 'url' in item:
                    embed.add_field(name="Link", value=item['url'], inline=False)
                await ctx.send(embed=embed)

        except ValueError:
            await ctx.send("Invalid price value. Please enter a number.")
        except Exception as e:
            await ctx.send(f"An error occurred: {str(e)}")
            print(f"Error details: {e}")

def main():
    load_dotenv()
    bot = ShoeBot()
    bot.run(os.getenv('DISCORD_TOKEN'))
if __name__ == "__main__":
    main()