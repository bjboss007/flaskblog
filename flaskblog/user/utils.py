from flask import url_for
from flask_mail import Message
import os
import secrets
from PIL import Image

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, ext = os.path.splitext(form_picture.filename)
    picture_name = random_hex+ext
    picture_path = os.path.join(current_app.root_path,'static/images/',picture_name)
    
    output_size = (120, 120)
    i =  Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_name

def send_reset_email(user):
    token = user.get_reset_token()
    sender = 'noreply@demo.com'
    recipients = [user.email]
    msg = Message('Password Reset Request', sender = sender, recipients = recipients)
    body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token = token, _external =True)}

If you did not make this request then simply ignore this email and no change(s) will be made.
    '''   
    msg.body = body 
    msg.send(msg)
