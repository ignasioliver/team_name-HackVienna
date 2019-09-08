from flask import Flask, flash, request, redirect, render_template, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

import os
import time
import requests
import shutil
import random
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url

UPLOAD_FOLDER = '<upload folder location>'
UPLOAD_FOLDER_PROFILE = '<upload folder profile location>'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

os.environ["CLOUDINARY_URL"] = "<your key>"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER_PROFILE'] = UPLOAD_FOLDER_PROFILE
app.secret_key = 'key'

current_profile = ""
DEFAULT_TAG = "default_tag"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def actual_extension(filename):
    return filename.rsplit('.', 1)[1].lower()


def actual_name(filename):
    return filename.rsplit('.', 1)[0].lower()


@app.route('/', methods=['GET', 'POST'])
def profile():
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
            random_id = str(random.randint(1, 500000) * random.randint(1, 500000))
            resources = ["glasses", "glassesjunction", "silver_face_mask", "oldglasses"]
            response = upload(
                file,
                background_removal="cloudinary_ai",
                tags=DEFAULT_TAG,
                public_id=random_id,
                transformation=[
                    {'flags': "region_relative", 'gravity': "adv_eyes", 'overlay': resources[random.randint(0, 3)], 'width': 1.5}
                ]
            )

            thumbnail_url, options = cloudinary_url(
                response['public_id'],
                format=response['format'],
                width=1000,
                height=1000,
                crop="fit",
                #background_removal="cloudinary_ai"
            )

            # Allow time for the image processing to complete:
            time.sleep(15)

            image_url = thumbnail_url
            resp = requests.get(image_url, stream=True)
            random_number = "profile"
            random_name = str(random_number) + str(".") + actual_extension(filename)
            local_file = open("profile/" + str(random_name), 'wb')
            resp.raw.decode_content = True
            shutil.copyfileobj(resp.raw, local_file)
            del resp

            if actual_extension(filename) == "jpeg":
                im = Image.open("profile/profile.jpeg")
                im.save("profile/profile.png")

            elif actual_extension(filename) == "jpg":
                im = Image.open("profile/profile.jpg")
                im.save("profile/profile.png")

            circle, options = cloudinary_url(
                response['public_id'],
                format=response['format'],
                width=200,
                height=200,
                gravity="face",
                radius="max",
                crop="crop",
            )

            return render_template('buttons.html', url=thumbnail_url, circle=circle, public_id=random_id)
    return render_template('index.html')


@app.route('/buttons', methods=['GET', 'POST'])
def buttons():
    return render_template('buttons.html', url=None, circle=None)


@app.route('/nature', methods=['GET', 'POST'])
def nature():
    try:
        img = os.path.join("profile", "profile.png")
    except IOError:
        img = None

    random_number = random.randint(1, 5)
    selected_image = str("nature" + str(random_number))

    try:
        nature_image = os.path.join("profile", selected_image + ".jpg")
    except IOError:
        nature_image = None
        print("Nature image couldn't be retrieved.")

    response = upload(
        "profile/profile.png",
        background_removal="cloudinary_ai",
        tags=DEFAULT_TAG,
        public_id=random.randint(1, 50000) * random.randint(1, 50000),
        transformation=[
            {'height': 375, 'crop': "scale"},
            {'underlay': selected_image, 'gravity': "south", 'width': 800}
        ]
    )

    converted, options = cloudinary_url(
        response['public_id'],
        format=response['format'],
        crop="fit"
    )

    return render_template('nature.html', image=img, nature_image=nature_image, converted=converted)


@app.route('/city', methods=['GET', 'POST'])
def city():
    try:
        img = os.path.join("profile", "profile.png")
    except IOError:
        img = None

    random_number = random.randint(1, 3)
    selected_image = str("city"+str(random_number))

    try:
        city_image = os.path.join("profile", selected_image+".jpg")
    except IOError:
        city_image = None
        print("City image couldn't be retrieved.")

    position_options = ["north", "south", "east", "west"]

    response = upload(
        "profile/profile.png",
        background_removal="cloudinary_ai",
        tags=DEFAULT_TAG,
        public_id=random.randint(1, 50000)*random.randint(1, 50000),
        transformation=[
            {'height': 375, 'crop': "scale"},
            {'underlay': selected_image, 'gravity': position_options[random.randint(0, 3)], 'width': 800}
        ]
    )

    converted, options = cloudinary_url(
        response['public_id'],
        format=response['format'],
        crop="fit"
    )

    return render_template('city.html', image=img, city_image=city_image, converted=converted)


@app.route('/luxury', methods=['GET', 'POST'])
def luxury():
    try:
        img = os.path.join("profile", "profile.png")
    except IOError:
        img = None

    random_number = random.randint(1, 3)
    selected_image = str("luxury"+str(random_number))

    try:
        luxury_image = os.path.join("profile", selected_image+".jpg")
    except IOError:
        luxury_image = None
        print("Luxury image couldn't be retrieved.")

    position_options = ["north", "south", "east", "west"]

    response = upload(
        "profile/profile.png",
        background_removal="cloudinary_ai",
        tags=DEFAULT_TAG,
        public_id=random.randint(1, 50000) * random.randint(1, 50000),
        transformation=[
            {'height': 375, 'crop': "scale"},
            {'underlay': selected_image, 'gravity': position_options[random.randint(0, 3)], 'width': 800}
        ]
    )

    converted, options = cloudinary_url(
        response['public_id'],
        format=response['format'],
        crop="fit"
    )

    return render_template('luxury.html', image=img, luxury_image=luxury_image, converted=converted)


@app.route('/random', methods=['GET', 'POST'])
def allrandom():
    try:
        img = os.path.join("profile", "profile.png")
    except IOError:
        img = None

    random_number = random.randint(1, 4)
    selected_image = str("random"+str(random_number))

    try:
        random_image = os.path.join("profile", selected_image + ".jpg")
    except IOError:
        print("Random image couldn't be retrieved.")

    response = upload(
        "profile/profile.png",
        background_removal="cloudinary_ai",
        tags=DEFAULT_TAG,
        public_id=random.randint(1, 50000) * random.randint(1, 50000),
        transformation=[
            {'height': 375, 'crop': "scale"},
            {'underlay': selected_image, 'gravity': "south", 'width': 800}
        ]
    )

    converted, options = cloudinary_url(
        response['public_id'],
        format=response['format'],
        crop="fit"
    )

    return render_template('random.html', image=img, random_image=random_image, converted=converted)


@app.route('/profile/<filename>')
def uploaded_profile(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER_PROFILE'], filename)


if __name__ == '__main__':
    app.run()
