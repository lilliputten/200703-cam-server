# -*- coding:utf-8 -*-
# @module server
# @since 2019.03.28, 21:32
# @changed 2020.10.28, 01:59

import os
from os import path
import datetime
import yaml

from config import config

from app import app
from logger import DEBUG
import errors

UPLOAD_FOLDER = path.join(config['uploadPath'])
mimeTypes = {
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'png': 'image/png',
    'gif': 'image/gif',
    #  'test': 'image/test',
}
mimeExtensions = mimeTypes.keys()  # {'aaa'}  # 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def uploadImage(ip, file):
    filename = file.filename
    name, extension = path.splitext(filename)
    ext = extension[1:].lower()

    now = datetime.datetime.now()
    timestamp = now.strftime(config['shortDateFormat'])
    #  timestamp = now.strftime(config['preciseDateFormat'])
    id = ip + '-' + now.strftime(config['dateTagPreciseFormat'])

    data = {
        'ip': ip,
        'filename': filename,
        'name': name,
        'ext': ext,
        'timestamp': timestamp,
    }

    if ext not in mimeExtensions:
        error = 'Unexpected extension (' + ext + ')'
        DEBUG('uploadImage: error: ' + error, data)
        return {'error': error}

    data['mimeType'] = mimeTypes[ext]

    DEBUG('uploadImage: data', data)

    uploadPath = config['uploadPath']

    try:
        if not os.path.exists(uploadPath):
            os.makedirs(uploadPath)
        # Save image...
        imageFilePath = os.path.join(uploadPath, id + config['imageExt'])
        file.save(imageFilePath)
        # Save yaml...
        yamlFilePath = os.path.join(uploadPath, id + '.yaml')
        yaml.safe_dump(data, open(yamlFilePath, 'wb'), encoding='utf-8', allow_unicode=True)
        # Update index file...
        indexFilePath = os.path.join(uploadPath, config['imagesIndex'])
        with open(indexFilePath, 'ab') as indexFile:
            indexFile.write(id + '\t' + ip + '\t' + timestamp + '\n')
    except Exception, error:
        DEBUG('uploadImage: error catched', {
            'error': errors.toBlockString(error),
        })
        return {'error': 'Upload file error (see server log)'}
    finally:
        return {'status': 'success', 'timestamp': timestamp, 'id': id, 'ip': ip}


__all__ = [  # Exporting objects...
    'uploadImage',
]
