from datetime import date

from requests import Response

from .exceptions import *
import shutil

HASHTAG_COLORS = {
    0: 'UNDERUSED',
    1: 'OVERUSED',
    2: 'LONG_LIFE',
    3: 'HOT_NOW',
    4: 'ONLY_ON_INSTAGRAM',
    5: 'BANNED_ON_INSTAGRAM',
}


class Hashtag:

    def __init__(self, json):
        self.__data = json

    @property
    def hashtag(self):
        # type: () -> str
        return self.__data['hashtag'] if 'hashtag' in self.__data else self.__data['tag']

    @property
    def tweets(self):
        # type: () -> int
        return self.__data['tweets']

    @property
    def exposure(self):
        # type: () -> int
        return self.__data['exposure']

    @property
    def retweets(self):
        # type: () -> int
        return self.__data['retweets']

    @property
    def images(self):
        # type: () -> float
        return self.__data['images'] if 'images' in self.__data else self.__data['photos']

    @property
    def links(self):
        # type: () -> float
        return self.__data['links']

    @property
    def mentions(self):
        # type: () -> float
        return self.__data['mentions']

    @property
    def color(self):
        # type: () -> int
        return self.__data['color']

    @property
    def color_verbose(self):
        # type: () -> str
        return HASHTAG_COLORS[self.color]

    @property
    def media_count(self):
        # type: () -> int
        return self.__data['mediaCount'] if 'mediaCount' in self.__data else None

    def __str__(self):
        # type: () -> str
        output_format = '==== Stats of #{} ====\ntweets: {}\nretweets: {}\nexposure: {}\n' \
                        'mentions: {}%\nlinks: {}%\nimages: {}%\ncolor: {}\nmedia count: {}\n'
        return output_format.format(
            self.hashtag,
            self.tweets,
            self.retweets,
            self.exposure,
            self.mentions * 100,
            self.links * 100,
            self.images * 100,
            self.color_verbose,
            self.media_count
        )


class HashtagHistory:

    def __init__(self, json):
        self.__data = json

    @property
    def hashtag(self):
        # type: () -> str
        return self.__data['tag']

    @property
    def date_str(self):
        # type: () -> str
        return self.__data['date']

    @property
    def date(self):
        # type: () -> date
        date_str = [int(x) for x in self.date_str.split(' ')[0].split('-')]
        return date(date_str[0], date_str[1], date_str[2])

    @property
    def tweets(self):
        # type: () -> int
        return self.__data['tweets']

    @property
    def retweets(self):
        # type: () -> int
        return self.__data['retweets']

    @property
    def links(self):
        # type: () -> float
        return self.__data['links']

    @property
    def images(self):
        # type: () -> float
        return self.__data['images']

    @property
    def mentions(self):
        # type: () -> float
        return self.__data['mentions']

    @property
    def color(self):
        # type: () -> int
        return self.__data['color']

    @property
    def color_verbose(self):
        # type: () -> str
        return HASHTAG_COLORS[self.color]

    @property
    def exposure(self):
        # type: () -> int
        return self.__data['exposure']

    def __str__(self):
        # type: () -> str
        output_format = '==== Stats of #{} ====\ndate: {}\ntweets: {}\nretweets: {}\nexposure: {}\n' \
                        'mentions: {}%\nlinks: {}%\nimages: {}%\ncolor: {}\n'
        return output_format.format(
            self.hashtag,
            self.date,
            self.tweets,
            self.retweets,
            self.exposure,
            self.mentions * 100,
            self.links * 100,
            self.images * 100,
            self.color_verbose
        )


class InstagramBannedHashtag:

    def __init__(self, post, banned_hashtag):
        # type: (str, [str]) -> InstagramBannedHashtag
        self.post = post
        self.banned_hashtags = banned_hashtag

    def __str__(self):
        # type: () -> str
        return '{} banned: {}'.format(self.post, ', '.join(self.banned_hashtags))


class Image:

    def __init__(self, content_type, content):
        self.content_type = content_type
        self.content = content
        self.ext = self.get_ext()

    def save(self, target_directory, filename_without_ext):
        # type: (str, str) -> str
        path = '{}/{}.{}'.format(target_directory, filename_without_ext, self.ext)
        with open(path, 'wb') as out_file:
            shutil.copyfileobj(self.content, out_file)
        return path

    def get_ext(self):
        ct = self.content_type
        if ct == 'image/png':
            return 'png'
        elif ct in ['image/jpg', 'image/jpeg']:
            return 'jpg'
        elif ct == 'image/gif':
            return 'gif'

        raise ImageFormatException('Unknown image format')


class Cta:

    def __init__(self, json):
        self.__data = json

    @property
    def id(self):
        # type: () -> int
        return self.__data['id']

    @property
    def name(self):
        # type: () -> str
        return self.__data['name']

    def __str__(self):
        # type: () -> str
        return '{} id:{}'.format(self.name, self.id)


class Link:

    def __init__(self, url, original, service, cta_id):
        # type: (str, str, str, int) -> Link
        self.url = url
        self.original = original
        self.service = service
        self.cta_id = cta_id

    def __str__(self):
        # type: () -> str
        return '{} ({}) service: {}, cta: {}'.format(self.url, self.original, self.service, self.cta_id)


class Parser:
    @staticmethod
    def _handle_error_message(json):
        # type: (dict) -> None
        if not json['result']:
            raise RiteTagException(json['message'])

    @staticmethod
    def hashtag_list(json, key):
        # type: (dict, str) -> [Hashtag]
        Parser._handle_error_message(json)
        return [Hashtag(x) for x in json[key]]

    @staticmethod
    def get_text(json, key):
        # type: (dict, str) -> str
        Parser._handle_error_message(json)
        return json[key]

    @staticmethod
    def history(json):
        # type: (dict) -> [HashtagHistory]
        Parser._handle_error_message(json)
        return [HashtagHistory(x) for x in json['data']]

    @staticmethod
    def banned_instagram_hashtags(json):
        # type: (dict) -> InstagramBannedHashtag
        Parser._handle_error_message(json)
        return InstagramBannedHashtag(json['post'], json['bannedHashtags'])

    @staticmethod
    def emoji(json):
        # type: (dict) -> str
        Parser._handle_error_message(json)
        return json['emojis']

    @staticmethod
    def image(response, external=False):
        # type: (Response, bool) -> Image
        try:
            return Image(response.headers['Content-Type'], response.raw)
        except ImageFormatException:
            if external:
                raise ImageFormatException
            json = response.json()
            raise RiteTagException(json['message'])

    @staticmethod
    def cta_list(json):
        # type: (dict) -> [Cta]
        Parser._handle_error_message(json)
        return [Cta(v) for k,v in json['list'].items()]

    @staticmethod
    def link(json):
        # type: (dict) -> Link
        Parser._handle_error_message(json)
        return Link(json['url'], json['original'], json['service'], json['ctaId'])

    @staticmethod
    def url_from_image(json):
        # type: (dict) -> str
        Parser._handle_error_message(json)
        return json['url']

    @staticmethod
    def free_mail_detection(json):
        # type: (dict) -> bool
        return json['freemail']

    @staticmethod
    def disposable_email_detection(json):
        # type: (dict) -> bool
        return json['disposable']

    @staticmethod
    def email_typo(json):
        # type: (dict) -> [str]
        return json['suggestions']

    @staticmethod
    def company_logo(json):
        # type: (dict) -> [str]
        return json['url']

    @staticmethod
    def name_from_email_address(json):
        # type: (dict) -> str
        return json['info']


class Limit:

    def __init__(self, limit, used, reset):
        self.limit = int(limit)
        self. used = int(used)
        reset_date = [int(x) for x in reset.split(' ')[0].split('-')]
        self.reset = date(reset_date[0], reset_date[1], reset_date[2])

    @property
    def usage(self):
        # type: () -> float
        return round((float(self.used) / self.limit) * 100, 2)

    def __str__(self):
        # type: () -> str
        return 'Used {}% of API credits. The limit resets on {}.'.format(self.usage, self.reset)


