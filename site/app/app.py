# Imports
from flask import Flask, redirect, url_for, render_template, request, session, flash, jsonify
import os
import pymongo

import ast

from config import DevelopmentConfig
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'pic/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

client = pymongo.MongoClient(
    "mongodb+srv://user1:2NvZYRipodUWsipy@cluster1.swpth.mongodb.net/sample_airbnb?retryWrites=true&w=majority")
db = client.chal48_passion_froid
col = db.picture


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def homepage():
    if request.method == 'POST':
        current_dir = os.getcwd()
        current_path = current_dir + "\\pictures\\"
        print(request.values.get('picture_type'))
        return render_template("index.html")
    else:
        images = [ a for a in col.find() ]
        print(images)
        return render_template("index.html", images=images)


@app.route("/update/<path>", methods=["GET", "POST"])
def update(path):
    if request.method == 'GET':
        obj = col.find_one({"path": path})
        if obj:
            return render_template("update.html", path=path, obj=obj)
        elif not obj:
            return redirect(url_for('create'))
        print('ERROR')


@app.route("/create", methods=["GET", "POST"])
def create():
    req = request.form
    if req:
        picture = request.files["picture"]
        current_dir = os.getcwd()
        path = current_dir + "\\static\\"
        imgPath = path + secure_filename(picture.filename)
        picture.save(imgPath)
        pictureName = req.get("picture_name")
        pictureType = req.get("picture_type")

        if req.get("with_product") == None:
            pictureWithProduct = False
        else:
            pictureWithProduct = True
        # pictureWithProduct = req.get("with_product")

        if req.get("with_human") == None:
            pictureWithHuman = False
        else:
            pictureWithHuman = True
        # pictureWithHuman = req.get("with_human")

        if req.get("is_instit") == None:
            pictureInstitutional = False
        else:
            pictureInstitutional = True
        # pictureInstitutional = req.get("is_instit")

        if req.get("is_vertical") == None:
            pictureVertical = False
        else:
            pictureVertical = True
        # pictureVertical = req.get("is_vertical")

        if req.get("is_limited") == None:
            pictureLimited = False
        else:
            pictureLimited = True
        # pictureLimited = req.get("is_limited")
        i = 0
        test = 0
        tags = []
        if req.get("tag0") : 
            while test == 0:
                tag = "tag" + str(i)
                if req.get(tag) is not None :
                    tags.append(req.get(tag))
                else :
                    test = 1
                i += 1
        print(tags)
            
        
        pictureCredit = req.get("picture_author")
        pictureCopyright = req.get("picture_copyright")
        pictureDate = req.get("picture_date")
        insert = {"name": pictureName, "type": pictureType, "path": secure_filename(picture.filename), "with_product": pictureWithProduct,
                  "with_human": pictureWithHuman, "institutional": pictureInstitutional, "format": pictureVertical,
                  "credits": pictureCredit, "user_permissions": pictureLimited, "copyright": pictureCopyright,
                  "end_date": pictureDate, "tags": tags}
        col.insert_one(insert)
        print(picture)
    return render_template("create.html")


@app.route("/delete/<path>", methods=["GET", "POST"])
def delete(path):
    col.delete_one({"path": path})
    message = 'Image has been deleted !'
    return render_template("index.html", message=message)


@app.route("/upload", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('homepage'))
    return render_template("upload.html")


@app.route("/search", methods=['GET', 'POST'])
def search():

    req = request.form

    if req:
        
        filters = {
            'with_product' : 'true' if req.get("with_product") == 'on' else 'false',
            'with_human' : 'true' if req.get("with_human") == 'on' else 'false',
            'institutional' : 'true' if req.get("institutional") == 'on' else 'false',
            'format' : 'true' if req.get("is_vertical") == 'on' else 'false'
        }

        if req.get("name") != '':
            filters['name'] = req.get("name") 

        if req.get("type") != '':
            filters['type'] = req.get("type") 

        if req.get("credits") != '':
            filters['credits'] = req.get("credits") 

        if req.get("tags") != '':
            filters['tags'] = req.get("tags") 

        search_str = '['

        if 'name' in filters:
            search_str += '{ "name" : {"$regex": \'.*' + filters['name'] + '.*\' }},'

        if 'type' in filters:
            search_str += '{ "type" : {"$regex": \'.*' + filters['type'] + '.*\' }},'
            
        if 'credits' in filters:
            search_str += '{ "credits" : {"$regex": \'.*' + filters["credits"] + '.*\' }},'
            
        if 'with_human' in filters :
            search_str += '{ "with_humans" :  {"$eq" :'+ filters["with_human"] +'}},'
            
        if "with_product" in filters:
             search_str += '{ "with_product" : {"$eq" :' + filters["with_product"] + '}},'
             
        if "format" in filters :
            search_str += '{ "format" : {"$eq" :' + filters["format"] + '}},'
             
        if "institutional" in filters:
             search_str += '{ "institutional" : {"$eq" :' + filters["institutional"] + '}},'
             
        if "tags" in filters :
            search_str += '{ "tags" : {"$in" : [ ' + filters["tags"] + ' ] }},'
        
        search_str += ']'


        
        query = 'col.find({ "$and" : ' + search_str + '})'
        
        collection_cursor = eval(query)

        images = [ a for a in collection_cursor ]

        return render_template("search.html", images=images)
    
    else:
        return render_template("search.html")


if __name__ == "__main__":
    app.run(debug=True)
