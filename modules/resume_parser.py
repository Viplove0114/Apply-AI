"""
resume_parser.py — Extracts text from uploaded PDF resumes or raw text input.

Supports:
  - PDF files via PyPDF2
  - Plain text passthrough with cleanup
"""

import io
import PyPDF2


def parse_pdf(uploaded_file) -> str:
    """
    Extract text content from an uploaded PDF file.

    Args:
        uploaded_file: A Streamlit UploadedFile object (or any file-like with .read()).

    Returns:
        Extracted text joined across all pages.

    Raises:
        ValueError: If the PDF is empty or unreadable.
    """
    try:
        pdf_bytes = uploaded_file.read()
        reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))

        pages_text = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                pages_text.append(text.strip())

        if not pages_text:
            raise ValueError(
                "Could not extract any text from the PDF. "
                "The file may be scanned/image-based. "
                "Please paste your resume as text instead."
            )

        return "\n\n".join(pages_text)

    except ValueError:
        raise
    except Exception as e:
        raise ValueError(
            f"Failed to read PDF: {e}\n"
            "Please make sure the file is a valid PDF."
        ) from e


def parse_text(text: str) -> str:
    """
    Clean up raw resume text input.

    Args:
        text: Raw text pasted by the user.

    Returns:
        Cleaned text with normalized whitespace.
    """
    if not text or not text.strip():
        raise ValueError("Resume text is empty. Please provide your resume content.")

    # Normalize whitespace: collapse multiple blank lines into one
    lines = text.strip().splitlines()
    cleaned = []
    prev_blank = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if not prev_blank:
                cleaned.append("")
                prev_blank = True
        else:
            cleaned.append(stripped)
            prev_blank = False

    return "\n".join(cleaned)
