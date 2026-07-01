from pathlib import Path
import tempfile

import streamlit as st

from presentation_coach.asr import DEFAULT_MODEL_ID, transcribe_audio
from presentation_coach.audio import get_audio_duration_seconds
from presentation_coach.report import build_report


st.set_page_config(
    page_title="Vietnamese Presentation ASR Coach",
    layout="wide",
)

st.title("Vietnamese Presentation ASR Coach")
st.caption(f"ASR model: {DEFAULT_MODEL_ID}")

uploaded_audio = st.file_uploader(
    "Audio file",
    type=["wav", "mp3", "m4a", "flac", "ogg"],
)
reference_text = st.text_area(
    "Transcript chuan (tuy chon)",
    height=140,
)


def save_upload_to_temp(uploaded_file) -> Path:
    suffix = Path(uploaded_file.name).suffix or ".wav"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_file.write(uploaded_file.getbuffer())
        return Path(temp_file.name)


if st.button("Phan tich", type="primary", disabled=uploaded_audio is None):
    temp_audio_path = save_upload_to_temp(uploaded_audio)

    try:
        with st.spinner("Dang chay PhoWhisper-base..."):
            duration_seconds = get_audio_duration_seconds(temp_audio_path)
            transcript = transcribe_audio(temp_audio_path)
            report = build_report(
                transcript=transcript,
                duration_seconds=duration_seconds,
                reference_text=reference_text,
            )

        metrics = report["metrics"]
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Thoi luong", f"{metrics.duration_seconds:.1f}s")
        col2.metric("So tu", metrics.word_count)
        col3.metric("WPM", f"{metrics.wpm:.1f}")
        col4.metric("Filler", metrics.filler_total)

        if report["wer"] is not None and report["cer"] is not None:
            col5, col6 = st.columns(2)
            col5.metric("WER", f"{report['wer'] * 100:.2f}%")
            col6.metric("CER", f"{report['cer'] * 100:.2f}%")

        st.subheader("Transcript")
        st.write(transcript or "_Khong co transcript._")

        st.subheader("Filler words")
        if metrics.filler_counts:
            st.table(
                [
                    {"filler": filler, "count": count}
                    for filler, count in metrics.filler_counts.items()
                ]
            )
        else:
            st.write("Khong phat hien filler word.")

        st.subheader("Feedback")
        for item in report["feedback"]:
            st.write(f"- {item}")
    finally:
        temp_audio_path.unlink(missing_ok=True)

