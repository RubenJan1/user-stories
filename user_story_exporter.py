import streamlit as st
from docx import Document
from io import BytesIO

st.set_page_config(page_title="User Stories Generator", layout="centered")

st.title("📘 User Stories Generator")

st.write("Maak hier eenvoudig user stories en exporteer ze naar Word.")

# Selectie voor type document
doc_type = st.radio("Kies type document:", ["Voor klant", "Voor interview"])

# Input velden
story_id = st.text_input("User Story ID", placeholder="Bijv. US-001")
als_input = st.text_area("Als...", placeholder="Bijv. een klant")
wil_input = st.text_area("Wil ik...", placeholder="Bijv. mijn bestelling volgen")
zodat_input = st.text_area("Zodat...", placeholder="Bijv. ik weet wanneer mijn pakket aankomt")

# Button voor toevoegen
if "stories" not in st.session_state:
    st.session_state["stories"] = []

if st.button("➕ Voeg user story toe"):
    if story_id and als_input and wil_input and zodat_input:
        st.session_state.stories.append({
            "id": story_id,
            "als": als_input,
            "wil": wil_input,
            "zodat": zodat_input
        })
        st.success(f"✅ User story {story_id} toegevoegd!")
    else:
        st.warning("⚠️ Vul alle velden in voordat je toevoegt.")

# Overzicht tonen
if st.session_state.stories:
    st.subheader("📋 Overzicht user stories")
    for story in st.session_state.stories:
        st.markdown(f"**{story['id']}**")
        st.write(f"- **Als** {story['als']}")
        st.write(f"- **Wil ik** {story['wil']}")
        st.write(f"- **Zodat** {story['zodat']}")
        st.markdown("---")

    # Export naar Word
    if st.button("💾 Exporteer naar Word"):
        doc = Document()
        doc.add_heading(f"User Stories - {doc_type}", level=1)
        
        for story in st.session_state.stories:
            doc.add_heading(story["id"], level=2)
            doc.add_paragraph(f"Als {story['als']}")
            doc.add_paragraph(f"Wil ik {story['wil']}")
            doc.add_paragraph(f"Zodat {story['zodat']}")
            doc.add_paragraph("---")

        # Opslaan in memory
        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)

        st.download_button(
            label="⬇️ Download Word-document",
            data=buffer,
            file_name=f"user_stories_{doc_type.replace(' ', '_')}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
