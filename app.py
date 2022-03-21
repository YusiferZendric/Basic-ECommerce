from flask import Flask, render_template,request,session
import json
import random
import smtplib
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.secret_key = 'mysecret'
db = SQLAlchemy(app)


class Item(db.Model):
    name = db.Column(db.String(length=30),nullbale=False,unique=True)


def productMaker(n):
    items = ["shoes","biscuits","salwar","Man suits", "Book","Novel","Wardrobe","Knife","Smartphone","Laptop"]
    companies = ["Samsung","LG","Apple","Parle","Jocky","Nike","Harry Potter","Kashmiri"]
    for i in range(n):
        random.shuffle(items)
        random.shuffle(companies)
        newCode = int("".join([str(random.randint(0,9)) for i in range(10)]))
        newProduct = f"{random.choice(companies)} {random.choice(items)}"
        newPrice = random.randint(400,20000)
        newRating = round(random.randint(50,100)/20,1)
        newDiscount = random.randint(2,70)
        def randomText(no):
            words = ['this','will','be','the','best','product','happening','in','there','cheap','rate','best quality','worth','it','to','buy']
            answer = []
            for i in range(no):
                answer.append(random.choice(words))

            return " ".join(answer)
        newDesc = [randomText(random.randint(40,120))]
        with open("product.json") as we:
            content = json.loads(we.read())
        content[newProduct] = {}
        content[newProduct]['code'] = newCode
        content[newProduct]['price'] = newPrice
        content[newProduct]['rating'] = newRating
        content[newProduct]['discount'] = newDiscount
        content[newProduct]['desc'] = newDesc
        newObj = json.dumps(content)
        with open("product.json",'w') as ew:
            ew.write(newObj)

# productMaker(5)

@app.route("/")
@app.route("/home")
def home():
    with open("product.json") as we:
        mainData = json.loads(we.read())
    reqData = {}
    a = list(mainData.keys())
    random.shuffle(a)
    for i in range(len(a)):
        reqData[a[i]] = mainData[a[i]]
    with open("product.json",'w') as ew:
        ew.write(json.dumps(reqData))
    # implement infinite scroll in reqData to the html file
    return render_template("home.html", instance='home',data=reqData,round=round,len=len)
@app.route("/<instance>")
def controller(instance):
    return render_template("home.html", instance=instance)
@app.route("/<prod>/<code>")
def productDesc(prod,code):
    with open("product.json") as we:
        mainData = json.loads(we.read())
    return render_template("product.html", product=prod, code=code,data=mainData,type=type,list=list)
@app.route("/Buy-<prod>/<code>")
def buy(prod,code):
    with open("product.json") as we:
        mainData = json.loads(we.read())
    session['prod'] = prod
    session['code'] = code
    return render_template('buy.html',product=prod,data=mainData,code=code,round=round)
@app.route("/success",methods=['GET','POST'])
def success():
    if request.method == 'POST':
        email = request.form['email']
        with open("product.json") as we:
            mainData = json.loads(we.read())
        print(mainData[session['prod']]['code'])
        print(session['code'])
        if str(mainData[session['prod']]['code']) == session['code']:
            price = round(((100-mainData[session['prod']]['discount'])/100)*mainData[session['prod']]['price'])
            message = f"Your order is placed successfully.\nProduct Name: {session['prod']}\nProduct code: {session['code']}\nProduct Price: {price} Rupees"
            server = smtplib.SMTP('smtp.gmail.com',587)
            server.starttls()
            server.login("codeislife4896@gmail.com",'setuppcop')
            server.sendmail("codeislife4896@gmail.com", email,message)
        return render_template('success.html',order=True,product=session['prod'],data=mainData,code=session['code'],round=round)
if __name__ == "__main__":
    app.run(debug=True)
