from PIL import Image
from .yuchunlib import process
from flask import Flask, request
from flask import send_file
import os

CURRENT_PATH = os.path.abspath(__file__)

app = Flask(__name__)

@app.route('/photo/process', methods=['POST'])
def get_photos():
    file = request.files.get("file")
    model = request.args.get("model", "la_muse")

    print("{} - {}".format(file, file.filename))
    if file is None:
        raise Exception("文件数据丢失, 请重新上传")

    try:
        image = Image.open(file)

        tmp_image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp2.jpg")
        image.save(tmp_image_path)

        width, height = image.size
        print(f"图片大小为:{width} * {height}")
        image = resize_images(image, 160000)

        image = process(image, model=model)
        print(os.path.join(os.path.dirname(CURRENT_PATH), "tmp.jpg"))
        tmp_image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp.jpg")
        image.save(tmp_image_path)
        response = send_file(tmp_image_path,
                             mimetype='image/jpeg')
    except Exception as e:
        print("处理失败")
        raise e

    return response


def resize_images(image,  threshold):
    import math
    width, height = image.size
    if width * height >= threshold:
        s = math.sqrt(width * height / threshold)

        new_height = int(height / s)
        new_width = int(width / s)
        image = image.resize((new_width, new_height))
        print(f"需要压缩，new size: {new_width} * {new_height}={new_width * new_height}")
    return image