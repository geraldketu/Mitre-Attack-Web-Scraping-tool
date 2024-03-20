from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import os

class mitre_attack_crawler(CrawlSpider):
    name = "Mitre_Attack_Crawler"
    allowed_domains = ["mitre.org"]
    start_urls = ["https://attack.mitre.org/"]

    rules = (
        Rule(LinkExtractor(allow=r'/techniques/T[0-9]+/$'), callback='parse_technique', follow=True),
    )

    def parse_technique(self, response):


        filename_with_subtechniques = 'mitre_techniques_with_subs.txt'
        filename_without_subtechniques = 'mitre_techniques_without_subs.txt'



        le_sub = LinkExtractor(allow=(r'/techniques/T[0-9]+/[0-9]+/$'))
        subtechniques = le_sub.extract_links(response)



        le = LinkExtractor(allow=(r'/techniques/T[0-9]+/$'), deny=(r'/versions/'))
        techniques = le.extract_links(response)



        techniques = [tech for tech in techniques if not any(sub.url.startswith(tech.url) for sub in subtechniques)]



        current_directory = os.getcwd()


        subtechniques_file_path = os.path.join(current_directory, filename_with_subtechniques)
        with open(subtechniques_file_path, 'a') as f_with_subs:
            for link in subtechniques:
                f_with_subs.write(f'{link.url}\n')

        # Write techniques without subtechniques to file
        techniques_file_path = os.path.join(current_directory, filename_without_subtechniques)
        with open(techniques_file_path, 'a') as f_without_subs:
            for link in techniques:
                f_without_subs.write(f'{link.url}\n')


        return {
            'techniques_with_subtechniques': [link.url for link in subtechniques],
            'techniques_without_subtechniques': [link.url for link in techniques]
        }
