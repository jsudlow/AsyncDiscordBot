import discord
import sqlite3
import time
import asyncio
def get_restock_updates():
    message = ''
    sql = "SELECT * from discord_restock"
    #print sql
    c.execute(sql)
    rows = c.fetchall()
    
    return rows

def delete_stail_restock(id):
    sql = 'delete from discord_restock where id=' + str(id)
    c.execute(sql)
    conn.commit()  


conn = sqlite3.connect('supreme_monitor.db')
c = conn.cursor()



class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def my_background_task(self):
        await self.wait_until_ready()
        
        channel = self.get_channel(496011196021997588) # channel ID goes here
        chan2 = self.get_channel(512417611640995852)
        while True:
            await asyncio.sleep(5)
            print('looping')
            rows = get_restock_updates()
            if rows:
              for row in rows:
                e = discord.Embed(title=row[1],description=row[2])
                e.set_image(url=row[3])
                await channel.send(embed=e)
                await chan2.send(embed=e)
                delete_stail_restock(row[0])
                time.sleep(1)
            

            
            


client = MyClient()
client.run('NDk1OTk5OTAzNDg3NDkyMTA2.DpKRoA.rjKR72ybyfjwHMy6793SNsBt7-o')
