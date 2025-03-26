# Import libraries
import requests
from bs4 import BeautifulSoup

# URL from which pdfs to be downloaded
url = "https://openaccess.thecvf.com/content_CVPR_2019/html/Deng_ArcFace_Additive_Angular_Margin_Loss_for_Deep_Face_Recognition_CVPR_2019_paper.html"

# Requests URL and get response object
response = requests.get(url)

# Parse text obtained
soup = BeautifulSoup(response.text, 'html.parser')

# Find all hyperlinks present on webpage
links = soup.find_all('a')

i = 0

# From all links check for pdf link and
# if present download file
for link in links:
	if ('.pdf' in link.get('href', [])):
		i += 1
		print("Downloading file: ", i)

		# Get response object for link
		response = requests.get(link.get('href'))

		# Write content in pdf file
		pdf = open("pdf"+str(i)+".pdf", 'wb')
		pdf.write(response.content)
		pdf.close()
		print("File ", i, " downloaded")

print("All PDF files downloaded")


import pymupdf

def pdf_to_text(pdf_path):
    text = ""
    try:
        pdf_document = pymupdf.open(pdf_path)
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            text += page.get_text("text")
        pdf_document.close()
    except Exception as e:
        print(f"An error occurred: {e}")
    return text

pdf_path = "your_pdf_file.pdf"
extracted_text = pdf_to_text(pdf_path)
print(extracted_text)
