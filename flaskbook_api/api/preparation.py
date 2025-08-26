from pathlib import Path
from PIL import Image

basedir = Path(__file__).parent.parent


def load_image(request, reshaped_size=(256, 256)):
    filename = request.json["filename"]
    dir_image = str(basedir / "data" / "original" / filename)
    # 画像データのオブジェクトを作成
    image_obj = Image.open(dir_image).convert("RGB")
    # 画像のデータサイズ変更
    image = image_obj.resize(reshaped_size)
    return image, filename
