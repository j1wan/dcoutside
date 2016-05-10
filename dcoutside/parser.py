from bs4 import BeautifulSoup, SoupStrainer


def parse_post(markup, parser, strainer: SoupStrainer) -> dict:
    soup = BeautifulSoup(markup, parser, parse_only=strainer)

    if not str(soup):
        soup = BeautifulSoup(markup, parser)

        if '/error/deleted/' in str(soup):
            return {'deleted': True}
        elif '해당 갤러리는 존재하지 않습니다' in str(soup):
            raise NoSuchGalleryError
        else:
            pass

    temp_info = soup.find(attrs={'class': 'w_top_right'})
    timestamp = temp_info.find('b').getText()

    user_info = soup.find(attrs={'class': 'user_layer'})
    user_id = user_info['user_id']
    user_ip = '' if user_id else temp_info.find(attrs={'class': 'li_ip'}).string
    nickname = user_info['user_name']

    title = soup.find('dl', attrs={'class': 'wt_subject'}).find('dd').getText()
    view_cnt = int(soup.find('dd', attrs={'class': 'dd_num'}).string)
    view_up = int(soup.find(id='recommend_view_up').string)
    view_dn = int(soup.find(id='recommend_view_down').string)
    comment_cnt = int(soup.find(id='re_count').string)
    body = str(soup.find('div', attrs={'class': 's_write'}).find('td'))

    post = {
        'user_id': user_id,
        'user_ip': user_ip,
        'nickname': nickname,

        'title': title,
        'written_at': timestamp,

        'view_up': view_up,
        'view_dn': view_dn,
        'view_cnt': view_cnt,
        'comment_cnt': comment_cnt,
        'body': body,
    }

    return post


def parse_comments(text: str) -> list:

    comments = []
    soup = BeautifulSoup(text, 'lxml')
    comment_elements = soup.find_all('tr', class_='reply_line')

    for element in comment_elements:
        user_layer = element.find('td', class_='user_layer')
        nickname = user_layer['user_name']
        user_id = user_layer['user_id']
        body = element.find('td', class_='reply')
        user_ip = '' if user_id else body.find('span').extract().text
        timestamp = element.find('td', class_='retime').text

        comment = {
            'user_id': user_id,
            'user_ip': user_ip,
            'nickname': nickname,
            'written_at': timestamp,
            'body': body.text.strip()
        }

        comments.append(comment)

    return comments


class NoSuchGalleryError(Exception):
    pass
