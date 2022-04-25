import os
import muggle_ocr
from flask import request
from flask import jsonify
from flask import Blueprint
from flask import render_template
from werkzeug.utils import secure_filename

from app import BASE_DIR
from app.models import OCRLogging
from app.utils.toolkit import create_id
from app.utils.api_expections import *
from app.utils.my_logger import logger
from app.utils.const_system_config import ALLOWED_EXTENSIONS


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


bp_ocr = Blueprint('ocr', __name__)


@bp_ocr.route("/index", methods=['GET'])
def index():
    # {{}} 在 vue 中 和 jinjia2 中的 冲突
    return render_template('upload.html', result="{{ result }}")


@bp_ocr.route("/api/v1/muggle-ocr", methods=['POST'])
def upload_file():
    # 验证请求方法
    if request.method != 'POST':
        raise RequestMethodError

    # 接收文件
    file = request.files['file']
    if file.filename == '':
        raise RequestInvalidParams(message='无文件名!!!')
    if file and allowed_file(file.filename):
        print(file.size)
        end_pix = file.filename.rsplit('.', 1)[1].lower()
        logger.info('<文件类型:{}><文件类型:{}>'.format(end_pix, file.filename))
        security_filename = secure_filename(file.filename)
        abs_security_filename = os.path.join(
            BASE_DIR, 'muggle_images', security_filename)
        file.save(abs_security_filename)
    else:
        raise RequestInvalidParams(message='上传的文件有误!!!')

    # 接收请求参数
    model_type = request.form.get('model_type')
    logger.info('<识别类型:{}>'.format(model_type))
    if model_type == 'ocr':
        mg_sdk = muggle_ocr.SDK(muggle_ocr.ModelType.OCR)
    elif model_type == 'captcha':
        mg_sdk = muggle_ocr.SDK(muggle_ocr.ModelType.Captcha)
    else:
        raise ParameterValidationFailed(message='暂不支持其他识别方法，仅支持默认的两种方法!!!')
    # 开始解析文件
    with open(abs_security_filename, 'rb') as f:
        img_bytes = f.read()
    result = mg_sdk.predict(image_bytes=img_bytes)
    logger.info('<解析文字:{}>'.format(result))
    OCRLogging().from_dict({
        'id': create_id('ocr_log'),
        'image_file_name': abs_security_filename,
        'ocr_result': result
    })
    return jsonify({
        'result': result,
        'message': 'ok',
    })

