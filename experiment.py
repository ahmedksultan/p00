#Tiffany Cao
#SoftDev1 pd1
#K
#2019

from flask import Flask, render_template,request,Response, client, stream_with_context
import queue,time

app = Flask(__name__)
waitlist= []
editing=False;
x=0

@app.route('/')
def hello_world():
    request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    ip=request.environ["REMOTE_ADDR"]
    if(len(waitlist)!=0):
        waitlist.remove(ip)
    x=60+time.time()
    if (client.is_connected()):
        print("a")
    else:
        print("b")
    return "str"
@app.route("/edit")
def queue():
    request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    ip=request.environ["REMOTE_ADDR"]
    if(len(waitlist)==0 and ip not in waitlist):
        editing=True;
        waitlist.append(request.environ["REMOTE_ADDR"])
    rule= request.host_url[:-1]
    print (rule)
    return "hi"

if __name__ == "__main__":
    app.debug = True
    app.run()
    rule=request.url_root
    print(rule)
