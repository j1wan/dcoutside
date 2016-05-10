from datetime import datetime
from .parser import *
import requests

COMMENTS_PER_PAGE = 40

class DCInsideCrawler:

    def __init__(self, markup='lxml', timeout=5, include_comments=False):
        self._session = requests.Session()
        self._timeout = timeout
        self._markup = markup
        self._view_url = 'http://gall.dcinside.com/board/view'
        self._strainer = SoupStrainer('div', attrs={'class': [
            're_gall_top_1',    # 제목, 글쓴이, 작성시각
            'btn_recommend',    # 추천, 비추천
            'gallery_re_title', # 댓글
            's_write',          # 본문
        ]})
        self._include_comments=include_comments

    def get_post(self, gall_id, post_no):
        try:
            r = self._session.get('%s/?id=%s&no=%d' % (self._view_url, gall_id, post_no), timeout=self._timeout)
            post = parse_post(r.text, 'lxml', self._strainer)
            post['gall_id'] = gall_id
            post['post_no'] = post_no
            post['crawled_at'] = datetime.now().isoformat()
            if self._include_comments and post.get('comment_cnt'):
                post['comments'] = self.get_all_comments(gall_id, post_no, post['comment_cnt'])
            return post

        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout):
            # if timeout occurs, retry
            return self.get_post(gall_id, post_no)

        except NoSuchGalleryError:
            return self.get_post(gall_id, post_no)


    def get_all_comments(self, gall_id, post_no, comment_cnt):
        comment_page_cnt = (comment_cnt - 1) // COMMENTS_PER_PAGE + 1
        comments = []
        headers = {'X-Requested-With': 'XMLHttpRequest'}
        data = {'ci_t': self._session.cookies['ci_c'], 'id': gall_id, 'no': post_no}

        for i in range(comment_page_cnt):
            data['comment_page'] = i + 1

            r = self._session.post('http://gall.dcinside.com/comment/view', headers=headers, data=data)
            batch = parse_comments(r.text)
            if not batch:
                break
            comments = batch + comments

        return comments


