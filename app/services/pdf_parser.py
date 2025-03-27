import pdfplumber
from pathlib import Path
from typing import Union


class PDFParserService:
    def __init__(self, file_path: Union[str, Path]):
        self.file_path = Path(file_path)

        if not self.file_path.exists():
            raise FileNotFoundError(f"File {self.file_path} not found.")

    def extract_text(self) -> str:
        full_text = []

        try:
            with pdfplumber.open(self.file_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        full_text.append(text)
        except Exception as e:
            raise RuntimeError(f"Error in parsing: {e}")

        return "\n".join(full_text)
