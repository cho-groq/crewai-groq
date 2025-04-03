from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from pypdf import PdfReader

class PDFToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    file_path: str

class PDFTool(BaseTool):
    name: str = "PDFTool"
    description: str = (
        "Get all the text from a PDF file and put it into a txt file."
    )
    # args_schema: Type[BaseModel] = PDFToolInput
    args_schema: type[BaseModel] = PDFToolInput

    def _run(self, file_path: str) -> str:
        print(f"DEBUG: Processing PDF at {file_path}")  # Debugging
        # Load the PDF
        print(file_path)
        # if file_path is None:
        #     file_path = '1912.01703v1.pdf'
        reader = PdfReader(file_path)
        
        # Extract text from all pages
        text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
        print("Text extracted and returned")
        print(text)
        return text

# class MyCustomTool(BaseTool):
#     name: str = "Name of my tool"
#     description: str = (
#         "Clear description for what this tool is useful for, your agent will need this information to use it."
#     )
#     args_schema: Type[BaseModel] = MyCustomToolInput

#     def _run(self, argument: str) -> str:
#         # Implementation goes here
#         return "this is an example of a tool output, ignore it and move along."
