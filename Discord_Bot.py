import discord
import config
from discord.ext import commands
from Sliding_Puzzle import Board
from Emoji_Dictionary import emoji_dict

bot = commands.Bot(command_prefix='!',intents=discord.Intents.all())

@bot.event
async def on_ready():
    global b 
    b = Board()

    print('Bot is ready!')
    try:
        synced = await bot.tree.sync()
    except Exception as e:
        print(f'Error: {e}')

@bot.tree.command(name='test_cmd')
async def test(interaction: discord.Interaction):
    text = ''

    # Displays characters in board array into a single string.
    for i in range(b.size):
        line = ''
        for j in range(b.size):
            if b.board[i][j] == 16:
                line += ':black_large_square:'
            else:
                line += f'{emoji_dict[b.board[i][j]]}'
        text += line + '\n'
        
    embed = discord.Embed(title='Playing...',
                        description=f'Enter your next move!\n\n{text}',
                        color=0x5865F2)
    
    response = await interaction.response.send_message(embed=embed)
    response = await interaction.original_response()

    await discord.InteractionMessage.add_reaction(response,'⬅️')
    await discord.InteractionMessage.add_reaction(response,'⬆️')
    await discord.InteractionMessage.add_reaction(response,'⬇️')
    await discord.InteractionMessage.add_reaction(response,'➡️')

@bot.event
async def on_raw_reaction_add(reaction,user):
    if user != bot.user:
        print('reacted')
        if reaction == '⬅️':
            b.MoveLeft()
        elif reaction == '⬆️':
            b.MoveUp()
        elif reaction == '⬇️':
            b.MoveDown()
        elif reaction == '➡️':
            b.MoveRight()
        #await bot.interaction.response.edit_message('test')
        

bot.run(config.TOKEN)