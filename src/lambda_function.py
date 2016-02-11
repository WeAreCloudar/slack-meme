from urlparse import parse_qs
import logging

from models import Memeifier, Memegen, parse_text_into_params

EXPECTED_TOKEN = "jya1AnM8fsgEMjJNqwBTn5sW"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    req_body = event['body']
    params = parse_qs(req_body)
    logger.info(params)
    token = params['token'][0]
    if token != EXPECTED_TOKEN:
        logger.error("Request token (%s) does not match exptected", token)
        raise Exception("Invalid request token")

    memegen = Memegen()
    memeifier = Memeifier()

    try:
        text = params['text'][0]
    except KeyError:
        return {'text': memegen.error()}

    if text.strip() == "":
        return {'text': memegen.error()}

    if text[:9] == "templates":
        return {'text': memegen.list_templates()}

    preview = True if text[:7] == "preview" else False
    text = text.replace("preview", "", 1) if preview else text

    template, top, bottom = parse_text_into_params(text)

    valid_templates = [x[0] for x in memegen.get_templates()]

    if template in valid_templates:
        meme_url = memegen.build_url(template, top, bottom)
    elif memeifier.image_exists(template):
        meme_url = memeifier.build_url(template, top, bottom)
    else:
        return { 'text': memegen.error()}

    if preview:
        response_type = 'ephemeral'
    else:
        response_type = 'in_channel'

    return {
        "response_type": response_type,
        "text": "",
        "attachments": [
            {
                "image_url": meme_url,
                "fallback": meme_url
            }
        ]
    }