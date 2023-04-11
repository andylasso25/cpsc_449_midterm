import os
from flask import request, jsonify, send_from_directory, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_jwt_extended import create_access_token, jwt_required
from app import app, db, dropzone
from app.models import User, Item



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            return jsonify({"msg": "Both username and password are required"}), 400

        existing_user = User.query.filter_by(username=username).first()
        if existing_user is not None:
            return jsonify({"msg": "User already exists"}), 400

        user = User(username=username, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()

        return jsonify({"msg": "User created successfully"}), 201
    
    return jsonify({"msg": "Forbidden"}), 403

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form['username']
    password = request.form['password']

    if not username or not password:
        print("Missing username or password")
        return jsonify({"msg": "Missing username or password"}), 400

    user = User.query.filter_by(username=username).first()

    if user is None or not check_password_hash(user.password, password):
        print("Invalid credentials")
        return jsonify({"msg": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200


@app.route('/protected', methods=['GET', 'POST'])
@jwt_required()
def protected():
    if request.method == 'GET':
        return render_template('protected.html')
    elif request.method == 'POST':
        jwt_token = request.form.get('jwt_token', None)
        if jwt_token:
            return "Access granted. You are now viewing the protected page."
        else:
            return "Access denied. Invalid or missing JWT token."


def allowed_file(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        allowed_file_types = set(['png', 'jpg', 'jpeg', 'gif'])
        max_file_size = app.config['DROPZONE_MAX_FILE_SIZE']
        return render_template('upload.html', allowed_file_types=allowed_file_types, max_file_size=max_file_size)

    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({"msg": "No file part"}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({"msg": "No file selected"}), 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            # Print the upload folder path
            print(f"Upload folder path: {app.config['DROPZONE_UPLOAD_FOLDER']}")

            # Check if the folder exists and create it if it does not
            upload_folder = app.config['DROPZONE_UPLOAD_FOLDER']
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)

            # Print the complete path that the file is being saved to
            save_path = os.path.join(app.config['DROPZONE_UPLOAD_FOLDER'], filename)
            print(f"Saving file to: {save_path}")

            # Save the file
            file.save(save_path)

            return jsonify({"msg": "File uploaded successfully"}), 200
        else:
            return jsonify({"msg": "Invalid file type"}), 400




@app.route('/public-items', methods=['GET'])
def public_items():
    items = Item.query.all()
    item_list = []

    for item in items:
        item_list.append({
            'id': item.id,
            'name': item.name,
            'description': item.description
        })

    return jsonify(items=item_list), 200


#eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4MTE2NzY4NSwianRpIjoiNTIwNTY1NTgtZjg5YS00NTA1LWFkZDctOWQ3M2YyOWE2YWY5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjgxMTY3Njg1LCJleHAiOjE2ODExNjg1ODV9.IyYDOWnpzW4q_bXfXdLvlB1Yjzg7UsA53fQKe4AvRFk