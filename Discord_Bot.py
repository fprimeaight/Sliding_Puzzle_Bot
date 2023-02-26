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
    
    # Adding button functionality
    left_button = discord.ui.Button(style=discord.ButtonStyle.blurple, emoji='⬅️')
    right_button = discord.ui.Button(style=discord.ButtonStyle.blurple, emoji='➡️')
    up_button = discord.ui.Button(style=discord.ButtonStyle.blurple, emoji='⬆️')
    down_button = discord.ui.Button(style=discord.ButtonStyle.blurple, emoji='⬇️')
    
    view = discord.ui.View()   

    view.add_item(left_button)
    view.add_item(up_button)
    view.add_item(down_button)
    view.add_item(right_button)

    async def left_button_callback(interaction):
        b.MoveLeft()
        text = BoardDisplay(b)
        
        if b.board == b.final_board_pos:
            embed = discord.Embed(title='You WON! 🏆',
                                description=f'You completed the puzzle!\n\n{text}',
                                color=0x65D532)
            response = await interaction.response.edit_message(embed=embed,view=None)
            del hashmap[user_id]
        else:
            embed = discord.Embed(title='Playing...',
                                description=f'Enter your next move!\n\n{text}',
                                color=0x5865F2)
            response = await interaction.response.edit_message(embed=embed,view=view)
    
    async def up_button_callback(interaction):
        b.MoveUp()
        text = BoardDisplay(b)
        
        if b.board == b.final_board_pos:
            embed = discord.Embed(title='You WON! 🏆',
                                description=f'You completed the puzzle!\n\n{text}',
                                color=0x65D532)
            response = await interaction.response.edit_message(embed=embed,view=None)
            del hashmap[user_id]
        else:
            embed = discord.Embed(title='Playing...',
                                description=f'Enter your next move!\n\n{text}',
                                color=0x5865F2)
            response = await interaction.response.edit_message(embed=embed,view=view)

    async def down_button_callback(interaction):
        b.MoveDown()
        text = BoardDisplay(b)
        
        if b.board == b.final_board_pos:
            embed = discord.Embed(title='You WON! 🏆',
                                description=f'You completed the puzzle!\n\n{text}',
                                color=0x65D532)
            response = await interaction.response.edit_message(embed=embed,view=None)
            del hashmap[user_id]
        else:
            embed = discord.Embed(title='Playing...',
                                description=f'Enter your next move!\n\n{text}',
                                color=0x5865F2)
            response = await interaction.response.edit_message(embed=embed,view=view)

    async def right_button_callback(interaction):
        b.MoveRight()
        text = BoardDisplay(b)
        
        if b.board == b.final_board_pos:
            embed = discord.Embed(title='You WON! 🏆',
                                description=f'You completed the puzzle!\n\n{text}',
                                color=0x65D532)
            response = await interaction.response.edit_message(embed=embed,view=None)
            del hashmap[user_id]
        else:
            embed = discord.Embed(title='Playing...',
                                description=f'Enter your next move!\n\n{text}',
                                color=0x5865F2)
            response = await interaction.response.edit_message(embed=embed,view=view)
            
    left_button.callback = left_button_callback
    up_button.callback = up_button_callback
    down_button.callback = down_button_callback
    right_button.callback = right_button_callback
    
    response = await interaction.response.send_message(embed=embed,view=view)

bot.run(config.TOKEN)