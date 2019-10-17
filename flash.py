from flask import Flask, render_template, request,send_file
from werkzeug.utils import secure_filename
import csv,itertools,os
app = Flask(__name__)

@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def uploads_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save("uploads/"+secure_filename(f.filename))
        reader = csv.DictReader(itertools.islice(open("uploads/"+secure_filename(f.filename)), 1, None))
        outputarray=[]
        total={}
        for row in reader:
            name=""
            team=""
            for a in row:
                temp=[]
                if row[a]!="":
                    if "Select your team" in a:
                        team=row[a]
                    if "Select Your Name" in a:
                        name=row[a]
                    elif "-" in a:
                        abc=a.split(" - ")
                        if len(abc)==2 and "ImportId" not in name:
                            if a.split(" - ")[0] not in total:
                                total[a.split(" - ")[0]]=[a.split(" - ")[0],0]
                            temp.append(a.split(" - ")[0])
                            temp.append(name)
                            temp.append(team)
                            temp.append(a.split(" - ")[1])
                            try:
                                temp.append(int(row[a].split(".")[0]))
                            except:
                                temp.append(row[a])
                            outputarray.append(temp)
                            outputarray.sort(key = lambda x: x[0]) 
        outputarray=[["name","by","team","Question","Answer","score"]]+outputarray
        with open("output.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerows(outputarray)
        del(outputarray)
        os.system("rm uploads/*")
        path="output.csv"
        return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.config['UPLOAD_FOLDER']="."
    app.run(debug = True)