import logging
import os
import subprocess
import tempfile
from io import BytesIO
from pathlib import Path
# use Bytes throughout because that's how lxml says XML should be used
from urllib.parse import urlparse

import requests
from lxml import etree


def download_uri_data(uri):
    """
    returns file object
    """
    logger = logging.getLogger(__name__)
    logger.info('Requesting data from: {}'.format(uri))
    # using requests to follow any redirects that happen
    r = requests.get(uri)
    # ensure it's the decompressed content
    r.raw.decode_content = True
    try:
        a = urlparse(uri)
        file = tempfile.mktemp(prefix="archive-", suffix=os.path.basename(a.path))
        folder = tempfile.mkdtemp('convrs-result')
        Path(file).write_bytes(r.content)
        cmd = ['7z', 'e', file, '-o' + folder+'/']
        sp = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        sp.wait(60000)

        items = os.listdir(folder)
        if len(items) > 0:
            return Path(os.path.join(folder, items[0])).read_text('utf-8')
    except Exception as e:
        print(e)

    logger.debug("Request content: {}".format(r.content))
    return r.content


def data_to_element(data):
    """
    data parameter should be bytes
    """
    logger = logging.getLogger(__name__)
    content = BytesIO(data)
    root = None
    try:
        utf8_parser = etree.XMLParser(encoding='utf-8')
        downloaded_xml = etree.parse(content, parser=utf8_parser)
        logger.debug("Downloaded: {}".format(downloaded_xml))
        root = downloaded_xml.getroot()
        logger.debug("Downloaded root {}".format(root))
    except SyntaxError as err:
        logger.warning("Parsing failed {}".format(err))
        raise err
    return root
