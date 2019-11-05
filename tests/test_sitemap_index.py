import pytest
from lxml import etree
from io import BytesIO
from sitemapper.sitemap_index import SitemapIndex
from sitemapper.sitemap import Sitemap


class TestSitemapIndex:
    def setup(self):
        sitemap_index_data = open('tests/sitemap_index_data.xml', 'rb').read()
        utf8_parser = etree.XMLParser(encoding='utf-8')
        self.sitemap_index_xml_root = etree.parse(BytesIO(sitemap_index_data), parser=utf8_parser).getroot()
        self.sitemap_index_element_xml = self.sitemap_index_xml_root[0]

        print("self.sitemap_index_element_xml {}".format(self.sitemap_index_element_xml))

    def test_sitemap_from_sitemap_element(self):
        sm = SitemapIndex.sitemap_from_sitemap_element(self.sitemap_index_element_xml)
        assert isinstance(sm, Sitemap)
        assert sm.loc == 'http://www.example.com/sitemap_a.xml'
        assert sm.lastmod == '2004-10-01T18:23:17+00:00'

    def test_sitemaps_from_sitemap_index_element(self):
        si = SitemapIndex.sitemaps_from_sitemap_index_element(self.sitemap_index_xml_root)
        assert len(list(si)) == 2

    def test_init(self):
        smi = SitemapIndex(self.sitemap_index_xml_root)
        assert len(list(smi.sitemaps)) == 2