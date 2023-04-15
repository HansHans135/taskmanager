from flask import Flask, render_template, request, redirect, session,jsonify
from zenora import APIClient
import requests
from discord_webhook import DiscordWebhook



url="https://mycard.lol/"
app = Flask(__name__)
client = APIClient("bot token", client_secret="")

app.config["SECRET_KEY"] = "mysecret"


@app.route("/")
def home():
    access_token = session.get("access_token")
    if not access_token:
        return render_template("login.html")
    bearer_client = APIClient(access_token, bearer=True)
    current_user = bearer_client.users.get_current_user()
    g=bearer_client.users.get_my_guilds()
    
    server={}
    servers=0
    ok=0
    for i in g:

        if i.icon_url==None:
            icon="https://images-ext-2.discordapp.net/external/KBc71VevCfURqkpKKhaVn83Bi4311swZjRVT_v5G40A/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/1048838352427831308/ed16753729de36d739f2c3e07f09ec41.webp?width=662&height=662"
        else:
            icon=i.icon_url
        if i.owner==True:
            server[i.name]={"icon":icon,"name":i.name,"id":i.id}
            ok+=1
        servers+=1
    return render_template("index.html",server=server,servers=servers,ok=ok,user=current_user)

@app.route("/set/<id>")
def setting(id):
    access_token = session.get("access_token")
    if not access_token:
        return render_template("login.html")
    bearer_client = APIClient(access_token, bearer=True)
    current_user = bearer_client.users.get_current_user()
    g=bearer_client.users.get_my_guilds()
    for i in g:
        if i.id == current_user.id:
            if i.is_owner==False:
                return redirect("/")
    l=[]
    for i in g:
        l.append(str(i.id))
    if not id in l:
        return redirect("/")
    d=requests.get(url=f"{url}/api/getserver/{id}",timeout=5).json()
    if d["try"] == False:
        return render_template("set.html",user=current_user,channels="--",members="--")
    else:
        return render_template("set.html",user=current_user,d=d,channels=d["channels"],members=d["members"])

@app.route("/login")
def login():
    return redirect("https://discord.com/api/oauth2/authorize?client_id=1091019040274780252&redirect_uri=https%3A%2F%2Ftaskmanager.mycard.lol%2Foauth%2Fcallback&response_type=code&scope=identify%20guilds%20email")


@app.route("/logout")
def logout():
    session.pop("access_token")
    return redirect("/")


@app.route("/oauth/callback")
def oauth_callback():
    code = request.args["code"]
    access_token = client.oauth.get_access_token(
        code, redirect_uri="https://taskmanager.mycard.lol/oauth/callback"
    ).access_token
    session["access_token"] = access_token
    return redirect("/log")

@app.route("/log")
def log():
    access_token = session.get("access_token")

    if not access_token:
        return redirect("/")

    bearer_client = APIClient(access_token, bearer=True)
    current_user = bearer_client.users.get_current_user()
    webhook = DiscordWebhook(url="webhook", content=f"用戶: {current_user.username} ({current_user.id})")
    response = webhook.execute()
    return redirect("/")

app.run(host="0.0.0.0",port=25577,debug=True)