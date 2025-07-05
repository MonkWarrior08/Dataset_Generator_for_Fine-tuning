"""
File handling utilities for reading text and PDF files.
"""

import streamlit as st
import PyPDF2
from typing import Union


class FileHandler:
    """Handles reading of various file types."""
    
    @staticmethod
    def read_text_file(uploaded_file) -> str:
        """Read uploaded text file."""
        try:
            return str(uploaded_file.read(), "utf-8")
        except Exception as e:
            st.error(f"Error reading text file: {e}")
            return ""
    
    @staticmethod
    def read_pdf_file(uploaded_file) -> str:
        """Read uploaded PDF file."""
        try:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            st.error(f"Error reading PDF file: {e}")
            return ""
    
    @staticmethod
    def read_file(uploaded_file) -> str:
        """Read file based on type."""
        if uploaded_file.type == "text/plain":
            return FileHandler.read_text_file(uploaded_file)
        elif uploaded_file.type == "application/pdf":
            return FileHandler.read_pdf_file(uploaded_file)
        else:
            st.error(f"Unsupported file type: {uploaded_file.type}")
            return "" 