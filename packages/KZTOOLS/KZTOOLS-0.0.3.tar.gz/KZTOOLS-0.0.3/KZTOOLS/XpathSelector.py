# coding: utf-8
# Author：KZ

from lxml import etree


class Selector():
    def __init__(self, text):
        self.sel = etree.HTML(text)

    def xpath(self, xpath):
        sel = self.sel

        class KZ():
            @property
            def get(self):
                re_data = sel.xpath(xpath)
                data = re_data[0] if re_data else None
                return data

            @property
            def getall(self):
                data = sel.xpath(xpath)
                return data

        kz = KZ()
        return kz


if __name__ == '__main__':
    with open('HTML.txt', 'r', encoding='utf-8') as f:
        response = f.read()
    sel = Selector(text=response)
    img = sel.xpath('//div[@class="image"]//img/@data-lazy-load-src')
    print(img.get)
