import discord
import threading
from flask import Flask, jsonify
app = Flask(__name__)
bot = discord.Bot()


@app.route("/api/getserver/<id>")
def api(id):
    data = {}
    g = bot.get_guild(int(id))
    if g == None:
        data={"try": False}
    else:
        data={"try": True,"members":g.member_count,"channels":len(g.channels)}
    response = jsonify(data)
    return response

def startweb():
    app.run(host="0.0.0.0", port=25576)
t = threading.Thread(target=startweb)
t.start()

bot.run("token")
