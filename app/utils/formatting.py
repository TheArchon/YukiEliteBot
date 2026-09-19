# ============================================================
# YukiEliteBot | app/utils/formatting.py
# Purpose: Telegram custom-emoji and mention entity builders.
# Version: 1.0.0 | Author: Archon | License: MIT
# ============================================================
from pyrogram.types import MessageEntity
from app.emojis import emoji_id

def u16(value): return len(value.encode("utf-16-le"))//2

def premium_parts(parts):
    text="";entities=[]
    for part in parts:
        if isinstance(part,tuple):
            key,value=part;offset=u16(text);text+=value
            entities.append(MessageEntity(type="custom_emoji",offset=offset,length=u16(value),custom_emoji_id=emoji_id(key)))
        else:text+=part
    return text,entities

def mention_parts(users):
    text="";entities=[]
    for user in users:
        if text:text+=" "
        name=(user.first_name or "User").replace("\n"," ")[:64]
        offset=u16(text);text+=name
        entities.append(MessageEntity(type="text_mention",offset=offset,length=u16(name),user=user))
    return text,entities

def combine(prefix_parts,users):
    text,entities=premium_parts(prefix_parts)
    if users:
        if text and not text.endswith("\n"):text+="\n\n"
        base=u16(text);names,name_entities=mention_parts(users);text+=names
        for entity in name_entities:entity.offset+=base
        entities.extend(name_entities)
    return text,entities
