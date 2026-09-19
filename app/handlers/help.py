# ============================================================
# YukiEliteBot | app/handlers/help.py
# Purpose: Help menu and command documentation.
# Version: 1.0.0 | Author: Archon | License: MIT
# ============================================================
from app.keyboards import help_page,home
from app.emojis import emoji

def page(number):
    if number==1:return f"{emoji('tag')} <b>Tagging Commands</b>\n\n<code>/hitag</code> — Hindi tag 🇮🇳\n<code>/entag</code> — English tag 🇬🇧\n<code>/gmtag</code> — Good Morning tag 🌅\n<code>/gntag</code> — Good Night tag 🌙\n<code>/tagall</code> — General tag 🔥\n<code>/jtag</code> — Joke tag 😂\n<code>/vctag</code> — VC tag, online members first 🎙️"
    if number==2:return f"{emoji('members')} <b>Mention Commands</b>\n\n<code>/admin</code> or <code>@admin</code> — tag admins, 6 per message\n<code>/all</code> or <code>@all</code> — tag members, 6 per message\n\n{emoji('text')} Custom message:\n<code>/admin plz join vc</code>\n<code>/all meeting starts now</code>"
    return f"{emoji('tools')} <b>Control & Owner Commands</b>\n\n<code>/stop</code> — stop tagging\n<code>/pause</code> — pause tagging\n<code>/resume</code> — resume tagging\n\n{emoji('owner')} <b>Owner</b>\n<code>/broadcast &lt;message&gt;</code> — broadcast\n<code>/stats</code> — bot statistics"

async def help_command(client,message):await message.reply_text(page(1),reply_markup=help_page(1),disable_web_page_preview=True)
async def help_callback(client,query):
    if query.data=="noop":return await query.answer("This is the current page.")
    if query.data=="home":
        await query.message.edit_text(f"{emoji('bot')} <b>YukiEliteBot</b>\n\n{emoji('spark')} Your professional group tagging assistant.",reply_markup=home());return await query.answer()
    number=int(query.data.split(":")[1]);await query.message.edit_text(page(number),reply_markup=help_page(number),disable_web_page_preview=True);await query.answer()
