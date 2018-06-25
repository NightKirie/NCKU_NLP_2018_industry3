#-*-coding:utf-8-*-
import tempfile, os
from imgurpython import ImgurClient
from config import client_id, client_secret, album_id, access_token, refresh_token, line_channel_access_token, line_channel_secret

static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')


def getUrl(img):
    ext = 'png'
    with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix=ext + '-', delete=False) as tf:
        img.save(tf, "PNG")
        img.close()
    tempfile_path = tf.name

    dist_path = tempfile_path + '.' + ext
    dist_name = os.path.basename(dist_path)
    os.rename(tempfile_path, dist_path)
    client = ImgurClient(client_id, client_secret, access_token, refresh_token)
    config = {
        'album': album_id,
        'name': '',
        'title': '',
        'description': ''
    }
    path = os.path.join('static', 'tmp', dist_name)
    image = client.upload_from_path(path, config=config, anon=False)
    os.remove(path)
    print(path)
    return image['link']