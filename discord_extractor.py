import datetime
import json
import os
import discord
intents=discord.Intents.default()
intents.message_content = True
intents.guilds = True
client = discord.Client(intents=intents)

BOT_TOKEN = ''
@client.event
#當機器人完成啟動時
async def on_ready():
    print('完成啟動，目前登入身份：', client.user)

@client.event
async def on_message(message):
    async def check_if_referenced(message):
        if message.reference is not None:
            return True
        else:
            return False

    try:
        os.mkdir('user_messages_dataset')
    except:
        pass

    #排除自己的訊息，避免陷入無限循環
    if message.author == client.user:
        return 0
    if message.content.startswith("測試"):
        
        if '抓取' in message.content and '@' in message.content and 'limit=' in message.content:
            await message.delete()
            # 设置程序开始时间
            start_time = datetime.datetime.now()
            start_time = start_time.strftime("%Y-%m-%d_%H:%M:%S")
            author_id = message.content.split('@')[1].split(' ')[0].replace('>','')
            limit = int(message.content.split('limit=')[1].split(' ')[0])
            author_name = ""
            author_counter = 0
            reference_counter = 0
                      
            async for user_message in message.channel.history(limit=limit):
                if str(user_message.author.id) == str(author_id):
                    author_name = user_message.author.name
                    author_counter += 1
                    with open(f"user_messages_dataset/{author_name}-{start_time}-{limit}.jsonl", 'a', encoding='utf-8') as file:
                        if await check_if_referenced(user_message):
                            try:
                                referenced_message = await message.channel.fetch_message(user_message.reference.message_id)
                            except:
                                referenced_message = ""
                            if referenced_message.content == "" or "@" in referenced_message.content:
                                continue
                            output = {'input': f"User: {referenced_message.content}", 'output': f"Assistant: {user_message.content}"}
                            file.write(json.dumps(output, ensure_ascii=False) + '\n')
                            reference_counter += 1
            
            await message.channel.send(f"最新的 {limit} 則訊息中，共有 {author_counter} 條 <@{author_id}> 發送的訊息")
            await message.channel.send(f"其中共有 {reference_counter} 條回覆他人的訊息")
            
            
            

try:
    client.run(BOT_TOKEN)
except Exception as e:
    print(e)