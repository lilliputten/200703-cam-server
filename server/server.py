# -*- coding:utf-8 -*-
# @module server
# @since 2019.03.28, 21:32
# @changed 2020.10.26, 03:26

import pathmagic  # noqa

#  import os
import traceback

#  from flask import current_app as app
from .app import app

from flask import redirect
from flask import render_template
#  from flask import url_for
from flask import jsonify
from flask import request

#  from config import config
from .logger import DEBUG

from .upload import uploadImage

import listImages
import imageUtils
#  import removeImages

from externalApi import externalApi


#  DEBUG('Server started', {
#      'FLASK_ENV': os.getenv('FLASK_ENV'),
#      'buildTag': config['buildTag'],
#  })


app.register_blueprint(externalApi)


@app.route('/app')
def serveAppFile():
    #  # Method 1: Using `file().read()`
    #  clientTemplatePath = config['clientTemplatePath']
    #  filePath = os.path.join(clientTemplatePath, 'index.html')
    #  return file(filePath).read()
    # Method 2: Using `send_static_file()`
    return app.send_static_file('index.html')


@app.route('/')
def rootPage():
    """
    Default page (last image or all images list)
    """
    return redirect('/last')
    #  return listImages.listAllImages()
    #  return listImages.viewLastImage()


@app.route('/image/<id>')
def sendImageFile(id=None):
    """
    Send image file
    """
    return listImages.sendImageFile(id)


@app.route('/view/<id>')
def viewImage(id=None):
    """
    View image
    """
    return listImages.viewImage(id)


@app.route('/list')
def listAllImages():
    """
    List images
    """
    return listImages.listAllImages()


@app.route('/last')
def viewLastImage():
    """
    View last image
    """
    return listImages.viewLastImage()


@app.route('/remove')
def removeAllImages():
    """
    Remove all uploaded images
    TODO: Remove image by id
    """
    # TODO: Detect referrer & return back?
    imageUtils.removeAllImages()
    #  removeImages.removeImages()
    return redirect('/')


# Tests...


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route('/user/<username>')
def profile(username):
    return 'User: %s' % username


# Upload image...

@app.route('/upload', methods=['POST'])
def upload():
    ip = request.environ['REMOTE_ADDR']
    file = request.files['file']
    result = uploadImage(ip, file)
    return jsonify(result)


# Errors processing...

@app.errorhandler(Exception)
def handle_error(e):
    #  errorType, errorValue, errorTraceback = sys.exc_info()
    #  @see https://docs.python.org/2/library/traceback.html
    errorTraceback = traceback.format_exc()
    error = str(e)
    errorRepr = e.__repr__()
    errorData = {
        'error': error,
        'repr': errorRepr,
        'traceback': str(errorTraceback)
    }
    DEBUG('server:Exception', errorData)
    #  return jsonify(errorData), getattr(e, 'code', 500)
    return render_template('error.html', error=error), getattr(e, 'code', 500)


if __name__ == '__main__':
    app.secret_key = 'hjAR5HUzijG04RJP3XIqUyy6M4IZhBrQ'
    app.logger.debug('test log')
    # app.debug = True
    app.run()
