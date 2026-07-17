from services.pdf_reader import read_all_pdfs

print("Loading PDFs...\n")

text = read_all_pdfs()

print(text)