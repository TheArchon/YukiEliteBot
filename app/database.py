# ============================================================
# YukiEliteBot | app/database.py
# Purpose: SQLite persistence for users, chats and statistics.
# Version: 1.0.0 | Author: Archon | License: MIT
# ============================================================
import asyncio,sqlite3
from datetime import datetime,timezone
from app.config import DB_PATH

class Database:
    def __init__(self,path=DB_PATH): self.path=path; self.lock=asyncio.Lock()
    async def init(self):
        async with self.lock:
            con=sqlite3.connect(self.path)
            con.executescript("""CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY,username TEXT,first_name TEXT,created_at TEXT NOT NULL,last_seen TEXT NOT NULL);CREATE TABLE IF NOT EXISTS chats(chat_id INTEGER PRIMARY KEY,title TEXT,type TEXT,created_at TEXT NOT NULL,last_seen TEXT NOT NULL);CREATE TABLE IF NOT EXISTS stats(key TEXT PRIMARY KEY,value INTEGER NOT NULL DEFAULT 0);CREATE TABLE IF NOT EXISTS tag_stats(chat_id INTEGER PRIMARY KEY,total_runs INTEGER NOT NULL DEFAULT 0,total_members INTEGER NOT NULL DEFAULT 0);""")
            con.commit();con.close()
    async def _run(self,sql,args=(),fetch=False):
        async with self.lock:
            con=sqlite3.connect(self.path);cur=con.execute(sql,args);rows=cur.fetchall() if fetch else None;con.commit();con.close();return rows
    async def track_user(self,user):
        now=datetime.now(timezone.utc).isoformat();await self._run("INSERT INTO users(user_id,username,first_name,created_at,last_seen) VALUES(?,?,?,?,?) ON CONFLICT(user_id) DO UPDATE SET username=excluded.username,first_name=excluded.first_name,last_seen=excluded.last_seen",(user.id,user.username or "",user.first_name or "",now,now))
    async def track_chat(self,chat):
        now=datetime.now(timezone.utc).isoformat();await self._run("INSERT INTO chats(chat_id,title,type,created_at,last_seen) VALUES(?,?,?,?,?) ON CONFLICT(chat_id) DO UPDATE SET title=excluded.title,type=excluded.type,last_seen=excluded.last_seen",(chat.id,chat.title or "",str(chat.type),now,now))
    async def increment(self,key,amount=1): await self._run("INSERT INTO stats(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=value+excluded.value",(key,amount))
    async def record_tag(self,chat_id,count): await self._run("INSERT INTO tag_stats(chat_id,total_runs,total_members) VALUES(?,?,?) ON CONFLICT(chat_id) DO UPDATE SET total_runs=total_runs+1,total_members=total_members+excluded.total_members",(chat_id,1,count))
    async def ids(self,table):
        column="user_id" if table=="users" else "chat_id";return [row[0] for row in await self._run(f"SELECT {column} FROM {table}",fetch=True)]
    async def stats(self):
        users=(await self._run("SELECT COUNT(*) FROM users",fetch=True))[0][0];chats=(await self._run("SELECT COUNT(*) FROM chats",fetch=True))[0][0];runs=(await self._run("SELECT COALESCE(SUM(total_runs),0) FROM tag_stats",fetch=True))[0][0];members=(await self._run("SELECT COALESCE(SUM(total_members),0) FROM tag_stats",fetch=True))[0][0];return users,chats,runs,members
