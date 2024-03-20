from scrapy.spiders import Spider
from scrapy import Request
import os
import csv

class MitreAttackTableScraper(Spider):
    name = "mitre_attack_table_scraper"
    allowed_domains = ["mitre.org"]

    def start_requests(self):
        """Initiates requests from URLs listed in specified text files."""
        files_to_read = ['techniques_without_subtechniques.txt', 'techniques_with_subtechniques.txt']
        for file_name in files_to_read:
            file_path = os.path.join(os.getcwd(), file_name)
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    for url in file.readlines():
                        url = url.strip()
                        if url:  # Check if URL is not empty
                            yield Request(url, callback=self.parse_table_data)

    def parse_table_data(self, response):
        """Extracts and saves table data from the response page."""
        tables = response.xpath('//table[@class="table table-bordered table-alternate mt-2"]')
        output_file_name = 'data.csv'
        with open(output_file_name, 'a', newline='', encoding='utf-8') as outfile:
            csv_writer = csv.writer(outfile)
            for table in tables:
                rows = table.xpath('.//tr')
                for row in rows[1:]:
                    # Extracting text from cells. Assuming cell order matches your requirements
                    cells_text = [cell.xpath('.//descendant::text()').getall() for cell in row.xpath('.//td')]
                    cleaned_cells_text = [' '.join(cell).strip() for cell in cells_text]

                    if all(cleaned_cells_text):  # Ensure row is not empty
                        csv_writer.writerow(cleaned_cells_text)

