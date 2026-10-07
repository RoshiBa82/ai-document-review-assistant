import streamlit as st
import PyPDF2
import re

st.set_page_config(
    page_title="AI Document Review Assistant",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Document Review Assistant")
st.write(
    "A prototype for supporting the first review of documents. "
    "The tool highlights information that may need further review."
)

st.divider()

uploaded_file = st.file_uploader(
    "Upload a PDF document",
    type=["pdf"]
)

if uploaded_file is not None:

    st.success(f"Document uploaded: {uploaded_file.name}")

    # Read PDF
    reader = PyPDF2.PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    st.subheader("Document information")

    if not text.strip():
        st.warning(
            "No readable text was found in this PDF. "
            "The document may require OCR."
        )
        st.stop()

    # Basic checks
    checks = []

    # Name
    name_found = bool(
        re.search(r"\b(name|namn)\b", text, re.IGNORECASE)
    )

    checks.append(
        ("Name / Namn", name_found)
    )

    # Institution
    institution_found = bool(
        re.search(
            r"\b(university|universitet|college|institution)\b",
            text,
            re.IGNORECASE
        )
    )

    checks.append(
        ("Institution", institution_found)
    )

    # Date / Year
    date_found = bool(
        re.search(
            r"\b(19|20)\d{2}\b",
            text
        )
    )

    checks.append(
        ("Year / Date", date_found)
    )

    # Course
    course_found = bool(
        re.search(
            r"\b(course|kurs|subject|ämne)\b",
            text,
            re.IGNORECASE
        )
    )

    checks.append(
        ("Course / Subject", course_found)
    )

    # Display results
    st.subheader("Initial review")

    for label, found in checks:

        if found:
            st.success(f"✓ {label} found")

        else:
            st.warning(f"⚠ {label} may be missing")

    st.divider()

    st.subheader("Extracted text")

    with st.expander("Show document text"):
        st.text(text[:10000])

    st.divider()

    st.info(
        "This is a prototype. The result is only a support tool "
        "and must always be reviewed by a human."
    )
