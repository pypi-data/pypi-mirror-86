from bs4 import BeautifulSoup

def bs_result(result_size=1):
    def wrapped(func):
        def wrapper(*args, **kwargs):
            ret = func(*args, **kwargs)
            ret = [] if not ret else ret
            if len(ret) != result_size and result_size != -1:
                raise Exception(
                    'Wrong amount of result: %d, expected amount: %d' % (
                        len(ret), result_size)
                )
            return ret if result_size == -1 else ret.pop()
        return wrapper
    return wrapped


class EsliteMovieCrawler:
    def __init__(self, html):
        self._bs = BeautifulSoup(html, 'html.parser')

    @bs_result(result_size=1)
    def _main_page(self):
        return self._bs.find_all('div', class_='film_time_tablePage')

    @bs_result(result_size=1)
    def _update_date(self):
        return self._main_page().find_all('div', class_='film_waring')

    @bs_result(result_size=1)
    def _list_page(self):
        return self._main_page().find_all('div', class_='film_list')

    @bs_result(result_size=1)
    def _movie_title_info(self, parent):
        return parent.find_all('div', class_='left')

    @bs_result(result_size=1)
    def _movie_details_page(self, parent):
        return parent.find_all('div', class_='right')
    
    @bs_result(result_size=-1)
    def _movie_details(self, parent):
        return self._movie_details_page(parent).find_all('li')

    @bs_result(result_size=-1)
    def _movie_time_page(self, parent):
        return parent.find_all('div', class_='swiper-slide')

    def _movie_info(self, parent):
        ret = dict()
        data = self._movie_title_info(parent)
        ret['title'] = data.p.text
        ret['url'] = None if not data.a else data.a.get('href')
        data = self._movie_details(parent)
        if data:
            ret['content_rank'], ret['length'], ret['subtitle'] = map(
                lambda d: d.text, data)

        dates = self._movie_time_page(parent)
        date_result = {}
        for d in dates:
            date = dict()
            date_result[d.p.text] = list(
                map(lambda x: x.text, d.find_all('li'))
            )

        ret['time'] = date_result
        return ret

    def updated_date(self):
        return self._update_date().span.text

    def movie_list(self):
        return list(
            map(
                lambda s: self._movie_info(s),
                self._list_page().find_all('div', class_='box')    
            )
        )
