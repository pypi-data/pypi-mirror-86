# =============================================================================
# Minet Mediacloud API Client
# =============================================================================
#
# A unified mediacloud API client that can be used to keep an eye on the
# rate limit and the used token etc.
#
from minet.utils import create_pool
from minet.mediacloud.constants import MEDIACLOUD_DEFAULT_TIMEOUT

from minet.mediacloud.search import mediacloud_search
from minet.mediacloud.topic import mediacloud_topic_stories


class MediacloudClient(object):
    def __init__(self, token):
        self.token = token
        self.http = create_pool(timeout=MEDIACLOUD_DEFAULT_TIMEOUT)

    def count(self, query, **kwargs):
        return mediacloud_search(
            self.http,
            self.token,
            query,
            count=True,
            **kwargs
        )

    def search(self, query, **kwargs):
        return mediacloud_search(
            self.http,
            self.token,
            query,
            count=False,
            **kwargs
        )

    def topic_stories(self, topic_id, **kwargs):
        return mediacloud_topic_stories(
            self.http,
            self.token,
            topic_id,
            **kwargs
        )
