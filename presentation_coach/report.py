from __future__ import annotations

from presentation_coach.analysis import SpeechMetrics, build_speech_metrics
from presentation_coach.evaluation import cer, wer


def build_feedback(metrics: SpeechMetrics, wer_value: float | None = None) -> list[str]:
    feedback: list[str] = []

    if metrics.word_count == 0:
        return ["Chua co transcript de phan tich."]

    if metrics.pace_label == "hoi cham":
        feedback.append("Toc do noi hoi cham, co the tang nhip o cac doan giai thich.")
    elif metrics.pace_label == "hoi nhanh":
        feedback.append("Toc do noi hoi nhanh, nen giam nhip de nguoi nghe theo kip.")
    else:
        feedback.append("Toc do noi dang o muc on dinh cho bai thuyet trinh.")

    if metrics.filler_total == 0:
        feedback.append("Gan nhu khong co filler word trong transcript.")
    elif metrics.filler_per_minute <= 3:
        feedback.append("Co mot vai filler word, nhung tan suat van chap nhan duoc.")
    else:
        feedback.append("Filler words xuat hien kha nhieu, nen luyen noi cham va ngat y ro hon.")

    if wer_value is not None:
        if wer_value <= 0.15:
            feedback.append("Ket qua ASR gan voi transcript chuan.")
        elif wer_value <= 0.35:
            feedback.append("Ket qua ASR co sai khac vua phai so voi transcript chuan.")
        else:
            feedback.append("Ket qua ASR sai khac nhieu, can kiem tra chat luong audio hoac noi ro hon.")

    return feedback


def build_report(
    transcript: str,
    duration_seconds: float,
    reference_text: str | None = None,
) -> dict[str, object]:
    metrics = build_speech_metrics(transcript, duration_seconds)
    has_reference = bool(reference_text and reference_text.strip())
    wer_value = wer(reference_text, transcript) if has_reference else None
    cer_value = cer(reference_text, transcript) if has_reference else None

    return {
        "metrics": metrics,
        "wer": wer_value,
        "cer": cer_value,
        "feedback": build_feedback(metrics, wer_value),
    }

