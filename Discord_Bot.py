import discord
import config
import time
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
                line += ':black_square_button:'
        output += line + '\n'
    return output

def GenerateBoard(board_obj):
    for i in range(randint(200,300)):
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
        board = Board()
        move_num = 0
        start_time = time.time()

        GenerateBoard(board)
        hashmap[user_id] = {'board': board,
                            'move_num' : move_num,
                            'start_time': start_time}
    
    board = hashmap[user_id]['board']
    start_time = hashmap[user_id]['start_time']
    
    text = BoardDisplay(board)
    embed = discord.Embed(title='Playing...',
                        description=f'Enter your next move!\n\n{text}',
                        color=0x5865F2)
    
    # Adding button functionality
    def initialise_view():
        up_button = discord.ui.Button(style=discord.ButtonStyle.blurple, emoji='⬆️',row=1)
        down_button = discord.ui.Button(style=discord.ButtonStyle.blurple, emoji='⬇️',row=2)
        left_button = discord.ui.Button(style=discord.ButtonStyle.blurple, emoji='⬅️',row=2)
        right_button = discord.ui.Button(style=discord.ButtonStyle.blurple, emoji='➡️',row=2)
        dummy_button1 = discord.ui.Button(label='⠀', style=discord.ButtonStyle.grey,row=1)
        dummy_button1.disabled = True
        dummy_button2 = discord.ui.Button(label='⠀', style=discord.ButtonStyle.grey,row=1)
        dummy_button2.disabled = True
        
        view = discord.ui.View()   
        view.add_item(dummy_button1)
        view.add_item(up_button)
        view.add_item(dummy_button2)
        view.add_item(left_button)
        view.add_item(down_button)
        view.add_item(right_button)
        
        left_button.callback = left_button_callback
        up_button.callback = up_button_callback
        down_button.callback = down_button_callback
        right_button.callback = right_button_callback

        return view

    def button_pressed(interaction,direction):
        if interaction.user.id == user_id:
            if direction == 'left':
                board.MoveLeft()
            elif direction == 'right':
                board.MoveRight()
            elif direction == 'up':
                board.MoveUp()
            else:
                board.MoveDown()
            
            text = BoardDisplay(board)
            hashmap[user_id]['move_num'] += 1

            if board.board == board.final_board_pos:
                end_time = time.time()
                time_diff = end_time - start_time
                embed = discord.Embed(title='You WON! 🏆',
                                    description=f'''You completed the puzzle!
                                                    You took {hashmap[user_id]['move_num']} moves.
                                                    You took {round(time_diff,2)} seconds.⏰\n
                                                    {text}''',
                                    color=0x65D532)
                view = None
                ephemeral = False
                del hashmap[user_id]
            else:
                embed = discord.Embed(title='Playing...',
                                    description=f'Enter your next move!\n\n{text}',
                                    color=0x5865F2)
                view = initialise_view()
                ephemeral = False
        else:
            embed = discord.Embed(description=f"You cannot play other people's games!\n\n",
                                color=0xDA5252)
            view = None
            ephemeral = True  

        return embed,view,ephemeral
    
    async def left_button_callback(interaction):
        embed, view, ephemeral = button_pressed(interaction,'left')
        if ephemeral == False:
            await interaction.response.edit_message(embed=embed,
                                                    view=view)
        else:
            await interaction.response.send_message(embed=embed,ephemeral=ephemeral)
    
    async def up_button_callback(interaction):
        embed, view, ephemeral = button_pressed(interaction,'up')
        if ephemeral == False:
            await interaction.response.edit_message(embed=embed,
                                                    view=view)
        else:
            await interaction.response.send_message(embed=embed,ephemeral=ephemeral)
        
    async def down_button_callback(interaction):
        embed, view, ephemeral = button_pressed(interaction,'down')
        if ephemeral == False:
            await interaction.response.edit_message(embed=embed,
                                                    view=view)
        else:
            await interaction.response.send_message(embed=embed,ephemeral=ephemeral)

    async def right_button_callback(interaction):
        embed, view, ephemeral = button_pressed(interaction,'right')
        if ephemeral == False:
            await interaction.response.edit_message(embed=embed,
                                                    view=view)
        else:
            await interaction.response.send_message(embed=embed,ephemeral=ephemeral)

    await interaction.response.send_message(embed=embed,view=initialise_view())

bot.run(config.TOKEN)