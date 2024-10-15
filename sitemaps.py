from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class IndexSitemap(Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return ['index', 'contact', 'about', 'services', 'menu']

    def location(self, item):
        return reverse(item)

sitemaps = {
    'index': IndexSitemap,
}