# coding: utf-8
from http.server import BaseHTTPRequestHandler
from io import BytesIO
from urllib.parse import urlparse
import json
import base64

from PIL import Image, ImageFont
from handright import Template, handwrite

DEFAULT_FONT = "Bo Le Locust Tree Handwriting Pen Chinese Font-Simplified Chinese Fonts"


class handler(BaseHTTPRequestHandler):

    def do_POST(self):

        req_datas = self.rfile.read(int(self.headers['content-length']))
        req = json.loads(req_datas.decode())
        # print(req_data_obj['width'])

        # attributeNames = [
        #     'width', 'height', 'font_size', 'line_spacing', 'word_spacing',
        #     'top_margin', 'bottom_margin', 'left_margin', 'right_margin',
        #     'line_spacing_sigma', 'font_size_sigma', 'word_spacing_sigma',
        #     'perturb_x_sigma', 'perturb_y_sigma', 'perturb_theta_sigma'
        # ]

        template = Template(
            background=Image.new(mode="1", size=(
                req['width'], req['height']), color=1),
            font=ImageFont.truetype(
                "data/{}.ttf".format(DEFAULT_FONT), size=req['font_size']),
            line_spacing=req['line_spacing'],
            fill=0,
            left_margin=req['left_margin'],
            top_margin=req['top_margin'],
            right_margin=req['right_margin'],
            bottom_margin=req['bottom_margin'],
            word_spacing=req['word_spacing'],
            line_spacing_sigma=req['line_spacing_sigma'],
            font_size_sigma=req['font_size_sigma'],
            word_spacing_sigma=req['word_spacing_sigma'],
            end_chars=req['end_chars'],
            perturb_x_sigma=req['perturb_x_sigma'],
            perturb_y_sigma=req['perturb_y_sigma'],
            perturb_theta_sigma=req['perturb_theta_sigma'],
        )

        try:
            images = handwrite(req['text'], template)
            ret = []
            for i, im in enumerate(images):
                assert isinstance(im, Image.Image)
                f = BytesIO()
                im.save(f, 'webp')
                ret.append(base64.encodebytes(f.getvalue()).decode())

            self.send_response(200)
            self.send_header('Content-type', 'text/json')
            self.end_headers()
            self.wfile.write(json.dumps(ret).encode())

        except Exception as err:
            self.send_response(400)
            self.send_header('Content-type', 'text/json')
            self.end_headers()
            self.wfile.write(str(err).encode())

        return
