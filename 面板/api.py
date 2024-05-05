from flask import Flask,jsonf

app=Flask(__name__)
return_template={
    "code":404,
    "message":"does not exist",
    "data":[]
}
@app.r("/")
async def index():
    return jsonf(return_template)


app.run()