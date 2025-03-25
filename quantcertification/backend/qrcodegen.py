import segno as sg
from flask import Flask, render_template_string, send_file
from io import BytesIO


logo = 'some path'
def createqrcode(url: str):
    bio = BytesIO()
    assert type(url) == str
    qr = sg.make_qr(url)
    qr.save(bio, kind='png', embeded_image_path = logo)