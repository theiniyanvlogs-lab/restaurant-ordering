import os
from PyPDF2 import PdfReader


def read_all_pdfs():
    """
    Reads all PDF files inside the knowledge folder
    and returns their combined text.
    """

    knowledge_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "knowledge"
    )

    all_text = ""

    if not os.path.exists(knowledge_path):
        return ""

    for filename in os.listdir(knowledge_path):

        if filename.lower().endswith(".pdf"):

            pdf_path = os.path.join(knowledge_path, filename)

            try:

                reader = PdfReader(pdf_path)

                all_text += f"\n\n========== {filename} ==========\n\n"

                for page in reader.pages:

                    text = page.extract_text()

                    if text:
                        all_text += text + "\n"

            except Exception as e:

                all_text += f"\nError reading {filename}: {e}\n"

    return all_text