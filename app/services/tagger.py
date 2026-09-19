# ============================================================
# YukiEliteBot | app/services/tagger.py
# Purpose: Per-group tagging engine with pause/resume/stop.
# Version: 1.0.0 | Author: Archon | License: MIT
# ============================================================
import asyncio
from dataclasses import dataclass
from pyrogram.enums import UserStatus,ChatMemberStatus
from pyrogram.errors import FloodWait,RPCError
from app.config import TAG_DELAY,MENTIONS_PER_MESSAGE,MAX_MEMBERS_PER_SCAN
from app.emojis import emoji
from app.utils.formatting import combine,premium_parts

@dataclass
class TagState:
    task: asyncio.Task
    paused: asyncio.Event
    stopped: asyncio.Event
    kind: str
    total: int=0
    sent: int=0

class TagManager:
    def __init__(self,client,db):
        self.client=client;self.db=db;self.tasks={};self.lock=asyncio.Lock()

    def running(self,chat_id):
        state=self.tasks.get(chat_id)
        return bool(state and not state.task.done())

    async def start(self,chat_id,kind,users,custom=""):
        async with self.lock:
            if self.running(chat_id):return False,None
            paused=asyncio.Event();paused.set();stopped=asyncio.Event()
            state=TagState(None,paused,stopped,kind,len(users))
            state.task=asyncio.create_task(self._run(chat_id,kind,users,custom,state))
            self.tasks[chat_id]=state
            return True,state

    async def _send(self,chat_id,text,entities=None):
        while True:
            try:return await self.client.send_message(chat_id,text,entities=entities or [])
            except FloodWait as error:await asyncio.sleep(error.value+1)
            except RPCError:return None

    async def _status(self,chat_id,key,label):
        text,entities=premium_parts([(key,emoji(key)),f" {label}"])
        return await self._send(chat_id,text,entities)

    async def _run(self,chat_id,kind,users,custom,state):
        try:
            intro={"hitag":("tag","Hindi Tag Is LIVE! 🇮🇳"),"entag":("tag","English Tag Is LIVE! 🇬🇧"),"gmtag":("start","Good Morning Tag Is LIVE! 🌅"),"gntag":("clock","Good Night Tag Is LIVE! 🌙"),"tagall":("tag","Tag All Is LIVE! 🔥"),"jtag":("spark","Joke Tag Is LIVE! 😂"),"vctag":("vc","VC Tag Is LIVE! 🎙️"),"admin":("admin","Admin Tag Is LIVE!"),"all":("members","Mentioning All Members!")}.get(kind,("tag","Tagging Is LIVE!"))
            await self._status(chat_id,*intro)
            for start in range(0,len(users),MENTIONS_PER_MESSAGE):
                await state.paused.wait()
                if state.stopped.is_set():break
                batch=users[start:start+MENTIONS_PER_MESSAGE]
                text,entities=combine(self._parts(kind,custom),batch)
                await self._send(chat_id,text,entities)
                state.sent+=len(batch)
                if state.sent<len(users):await asyncio.sleep(TAG_DELAY)
            if not state.stopped.is_set():
                text,entities=premium_parts([("success",emoji("success")),f" Tagging completed successfully.\n\n",("members",emoji("members")),f" Members tagged: {state.sent}"])
                await self._send(chat_id,text,entities)
                await self.db.record_tag(chat_id,state.sent)
                await self.db.increment("tag_runs")
                await self.db.increment("tagged_members",state.sent)
        except asyncio.CancelledError:
            return
        finally:
            async with self.lock:
                if self.tasks.get(chat_id) is state:self.tasks.pop(chat_id,None)

    def _parts(self,kind,custom):
        if custom:return [custom,"\n\n"]
        return {
            "hitag":[("tag",emoji("tag"))," Namaste dosto 🇮🇳❤️\n\n"],
            "entag":[("tag",emoji("tag"))," Hey everyone! 👋\n\n"],
            "gmtag":[("start",emoji("start"))," Good Morning dosto 🌅☕\nUth jao sab!\n\n"],
            "gntag":[("clock",emoji("clock"))," Good Night dosto 🌙✨\nSleep well!\n\n"],
            "tagall":[("tag",emoji("tag"))," Everyone, where are you? 🔥\n\n"],
            "jtag":[("spark",emoji("spark"))," Joke time 😂 Don't ignore this!\n\n"],
            "vctag":[("vc",emoji("vc"))," VC is live! 🎙️🔥 Join karo!\n\n"],
            "admin":[("admin",emoji("admin"))," Admins, please check this. 👮‍♂️\n\n"],
            "all":[("members",emoji("members"))," Attention everyone! 📢\n\n"]
        }.get(kind,[("tag",emoji("tag"))," Tagging...\n\n"])

    async def members(self,chat_id,kind):
        members=[]
        async for member in self.client.get_chat_members(chat_id):
            if len(members)>=MAX_MEMBERS_PER_SCAN:break
            user=member.user
            if not user or user.is_bot or user.is_deleted:continue
            if kind=="admin" and member.status not in (ChatMemberStatus.ADMINISTRATOR,ChatMemberStatus.OWNER):continue
            members.append(user)
        if kind=="vctag":
            online={UserStatus.ONLINE:0,UserStatus.RECENTLY:1,UserStatus.LAST_WEEK:2,UserStatus.LAST_MONTH:3}
            members.sort(key=lambda user:online.get(getattr(user,"status",None),4))
        return members

    async def stop(self,chat_id):
        state=self.tasks.get(chat_id)
        if not state or state.task.done():return False
        state.stopped.set();state.paused.set();state.task.cancel()
        return True

    async def pause(self,chat_id):
        state=self.tasks.get(chat_id)
        if not state or state.task.done():return False
        state.paused.clear();return True

    async def resume(self,chat_id):
        state=self.tasks.get(chat_id)
        if not state or state.task.done():return False
        state.paused.set();return True
