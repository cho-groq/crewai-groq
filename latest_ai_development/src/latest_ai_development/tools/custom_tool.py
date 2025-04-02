from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from pypdf import PdfReader

class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    argument: str = Field(..., description="Description of the argument.")

class MyCustomTool(BaseTool):
    name: str = "Name of my tool"
    description: str = (
        "Clear description for what this tool is useful for, your agent will need this information to use it."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, argument: str) -> str:
        # Implementation goes here
        return "this is an example of a tool output, ignore it and move along."

class PDFTool(BaseTool):
    name: str = "PDFTool"
    description: str = (
        "Get all the text from a PDF file and put it into a txt file."
    )
    # file_path='./papers/1912.01703v1.pdf'
    args_schema: Type[BaseModel] = PDFTool

    def _run(self, file_path: str) -> str:
        # Load the PDF
        reader = PdfReader(file_path)

        # Extract text from all pages
        text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())

        # Save to a text file
        with open("output.txt", "w", encoding="utf-8") as file:
            file.write(text)

        print("Text extracted and saved to output.txt")

        return "this is an example of a tool output, ignore it and move along."

