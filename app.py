import pickle
from collections import Counter
import datetime
from reply_mentions import reply_form
from flask import Flask,render_template,request,redirect,url_for,send_file,jsonify

app = Flask(__name__)


def check_stats(add=False):
    with open('assets/stats.pickle', 'rb') as file:
    		stats=pickle.load(file)
    		if add==True:
    			stats["count"]+=1
    		return stats
    		
def save_stats(stats):
    with open('assets/stats.pickle', 'wb') as outputfile:
    	pickle.dump(stats, outputfile)

stats=Counter()
stats["count"]=0
start_time=datetime.datetime.now()
save_stats(stats)
		
def get_id_from_link(link):
    tweet_id = link.split("/status/")[1].split("?")[0]
    return tweet_id
    
def save_images(imgs):
    file_paths=[]
    for i,img in enumerate(imgs):
    	img.save(f"static/tweet_screenshot{i}.jpg")
    	file_paths.append(f"tweet_screenshot{i}.jpg")
    return file_paths



#   		for i,img in enumerate(images):
#    			img.save(f"static/tweet_screenshot{i}.jpg")
#    			return send_file(f"static/tweet_screenshot{i}.jpg",as_attachment=True)

    
@app.route("/",methods=["GET","POST"])
def home():
    if request.method=="POST":
    	link=request.form.get("link")
    	type=request.form.get("type")
    	color=request.form.get("color")
    	id=get_id_from_link(link)
    	images=reply_form(id,type,color)
    	images_paths=save_images(images)
    	stats=check_stats(add=True)
    	save_stats(stats)
    	return render_template('index.html', files=images_paths)    	
    return render_template("index.html")
    
@app.route("/stats")
def get_stats():
    current_time=datetime.datetime.now()
    no_downloads=check_stats()["count"]
    date_difference=(current_time-start_time).seconds/3600
    return jsonify({"no of requested screenshots":no_downloads,"time difference":date_difference})
    
@app.route('/files_download/<filename>')
def files_download(filename):
    return send_file("static/"+filename,as_attachment=True)


if __name__ == "__main__":
    app.run(debug=False)
