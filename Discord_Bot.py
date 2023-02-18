import discord
import config
from random import randint
from discord.ext import commands
from Sliding_Puzzle import Board
from Emoji_Dictionary import emoji_dict

bot = commands.Bot(command_prefix='!',intents=discord.Intents.all())
hashmap = {}

def BoardDisplay(board_obj):
    output = ''
    for i in range(board_obj.size + 2):
        line = ''
        for j in range(board_obj.size + 2):
            if i > 0 and i < board_obj.size + 1 and j > 0 and j < board_obj.size + 1:
                if board_obj.board[i-1][j-1] == 16:
                    line += ':black_large_square:'
                else:
                    line += f'{emoji_dict[board_obj.board[i-1][j-1]]}'
            else:
                line += ':blue_square:'
        output += line + '\n'
    return output

def GenerateBoard(board_obj):
    for i in range(randint(100,200)):
        move_index = randint(0,3)
        if move_index == 0:
            board_obj.MoveUp()
        elif move_index == 1:
            board_obj.MoveLeft()
        elif move_index == 2:
            board_obj.MoveDown()
        else:
            board_obj.MoveRight()
    
    

@bot.event
async def on_ready():
    print('Bot is ready!')
    try:
        synced = await bot.tree.sync()
    except Exception as e:
        print(f'Error: {e}')

@bot.tree.command(name='play')
async def play(interaction: discord.Interaction):
    print(interaction.user.id)
    user_id = interaction.user.id
    if user_id not in hashmap:
        b = Board()
        GenerateBoard(b)
        hashmap[user_id] = b
    else:
        b = hashmap[user_id]
    
    text = BoardDisplay(b)
    embed = discord.Embed(title='Playing...',
                        description=f'Enter your next move!\n\n{text}',
                        color=0x5865F2)
    
    response = await interaction.response.send_message(embed=embed)
    response = await interaction.original_response()

    reactions = ['⬅️','⬆️','⬇️','➡️']

    while b.board != b.final_board_pos:
        for reaction in reactions:
            await response.add_reaction(reaction)
        reaction,user = await bot.wait_for('reaction_add',
                                            check = lambda r,user: user == interaction.user and r.emoji in reactions)
        await reaction.remove(user)

        if reaction.emoji == reactions[0]:
            b.MoveLeft()
        elif reaction.emoji == reactions[1]:
            b.MoveUp()
        elif reaction.emoji == reactions[2]:
            b.MoveDown()
        elif reaction.emoji == reactions[3]:
            b.MoveRight()
        
        text = BoardDisplay(b)
        embed = discord.Embed(title='Playing...',
                            description=f'Enter your next move!\n\n{text}',
                            color=0x5865F2)
        response = await interaction.edit_original_response(embed=embed)

    embed = discord.Embed(title='You WON! 🏆',
                                description=f'You completed the puzzle!\n\n{text}',
                                color=0x65D532)  
    response = await interaction.edit_original_response(embed=embed)

bot.run(config.TOKEN)