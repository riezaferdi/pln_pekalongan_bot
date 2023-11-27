import discord
from discord.ext import tasks, commands
from bs4 import BeautifulSoup
import requests

# Set up your Discord bot
bot = commands.Bot(command_prefix='!')

# Your Discord channel ID
channel_id = 123456789012345678

# Instagram profile URL
instagram_url = "https://www.instagram.com/plnpekalongan/"

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@tasks.loop(minutes=15)  # Check for new posts every 15 minutes
async def check_instagram():
    channel = bot.get_channel(channel_id)
    
    # Fetch Instagram profile page
    response = requests.get(instagram_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract the URL of the latest post
        post_div = soup.find('div', {'class': 'v1Nh3'})  # Adjust this based on Instagram HTML structure
        if post_div:
            post_url = "https://www.instagram.com" + post_div.a['href']
            await channel.send(f'New Instagram Post: {post_url}')

@bot.command()
async def start_instagram_check(ctx):
    check_instagram.start()
    await ctx.send('Instagram post checking has started!')

@bot.command()
async def stop_instagram_check(ctx):
    check_instagram.stop()
    await ctx.send('Instagram post checking has been stopped.')

# Replace 'YOUR_TOKEN' with your actual Discord bot token
bot.run('YOUR_TOKEN')