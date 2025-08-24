from pathlib import Path
import numpy as np
import cv2
import torch
from flask import current_app, jsonify  # abort は使っていないので削除

from flaskbook_api.api.postprocess import draw_lines, draw_texts, make_color, make_line
from flaskbook_api.api.preparation import load_image
from flaskbook_api.api.preprocess import image_to_tensor

# ── パス設定（api/ の 1 つ上＝flaskbook_api/ を基準にする）
BASEDIR = Path(__file__).parent.parent
MODEL_PATH = BASEDIR / "model.pt"

# ── 起動時に一度だけモデルを読み込み（PyTorch 2.6 対応）
# 本の配布モデル（pickle 保存）なので weights_only=False を明示
model = torch.load(MODEL_PATH, map_location="cpu", weights_only=False)
model = model.eval()


@torch.inference_mode()
def detection(request):
    dict_results = {}

    # ラベル取得（未設定なら安全にフォールバック）
    labels = current_app.config.get("LABELS", [])

    # 画像の読み込み
    image, filename = load_image(request)

    # 画像をテンソルへ
    image_tensor = image_to_tensor(image)  # CPU のままでOK（model も CPU で読み込み）

    # ★ ここで再ロードしない！上で読み込んだグローバル model を使う
    output = model([image_tensor])[0]

    result_image = np.array(image.copy())

    # 物体の枠とラベルを描画
    for box, label, score in zip(output["boxes"], output["labels"], output["scores"]):
        if (
            score > 0.6
            and (0 <= int(label) < len(labels))
            and labels[int(label)] not in dict_results
        ):
            color = make_color(labels)
            line = make_line(result_image)

            c1 = (int(box[0]), int(box[1]))
            c2 = (int(box[2]), int(box[3]))

            draw_lines(c1, c2, result_image, line, color)
            draw_texts(result_image, line, c1, color, labels[int(label)])
            dict_results[labels[int(label)]] = round(100 * score.item())

    # 出力先
    out_dir = BASEDIR / "data" / "output"
    out_dir.mkdir(parents=True, exist_ok=True)  # フォルダが無ければ作成
    out_path = out_dir / filename

    # 保存（OpenCV は BGR 前提）
    cv2.imwrite(str(out_path), cv2.cvtColor(result_image, cv2.COLOR_RGB2BGR))

    return jsonify(dict_results), 201
