import csv

input_file_path = 'extracted_links.txt'
without_subtechniques_file_path = 'techniques_without_subtechniques.csv'
with_subtechniques_file_path = 'techniques_with_subtechniques.csv'

def is_technique_url(url):
    # Checks if the URL is a valid technique or subtechnique URL
    parts = url.rstrip('/').split('/')
    if len(parts) >= 5 and parts[3] == 'techniques' and parts[4].startswith('T'):
        return True, len(parts) == 6 and parts[5].isdigit()
    return False, False

with open(input_file_path, 'r') as input_file, \
     open(without_subtechniques_file_path, 'w', newline='') as without_subtechniques_file, \
     open(with_subtechniques_file_path, 'w', newline='') as with_subtechniques_file:

    # Setting up CSV writers
    without_subtechniques_writer = csv.writer(without_subtechniques_file)
    with_subtechniques_writer = csv.writer(with_subtechniques_file)

    # Writing the header row
    without_subtechniques_writer.writerow(['URL'])
    with_subtechniques_writer.writerow(['URL'])

    for line in input_file:
        url = line.strip()
        is_technique, is_subtechnique = is_technique_url(url)

        if is_technique and not is_subtechnique:
            # This is a main technique URL
            without_subtechniques_writer.writerow([url])
        elif is_subtechnique:
            # This URL points to a subtechnique
            with_subtechniques_writer.writerow([url])

print('Processing complete. Check the output CSV files for results.')
