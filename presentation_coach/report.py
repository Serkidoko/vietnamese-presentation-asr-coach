from __future__ import annotations

from presentation_coach.analysis import SpeechMetrics, build_speech_metrics
from presentation_coach.evaluation import cer, wer


def _top_filler(metrics: SpeechMetrics) -> str | None:
    if not metrics.filler_counts:
        return None
    return max(metrics.filler_counts.items(), key=lambda item: item[1])[0]


def build_feedback(metrics: SpeechMetrics, wer_value: float | None = None) -> list[str]:
    feedback: list[str] = []

    if metrics.word_count == 0:
        return [
            "Chua co transcript de phan tich. Hay thu record lai mot doan ngan 20-30 giay, noi ro tung y va de micro gan hon mot chut."
        ]

    feedback.append(
        f"Tong quan: ban noi {metrics.word_count} tu trong {metrics.duration_seconds:.1f} giay, toc do khoang {metrics.wpm:.0f} WPM. Minh se tap trung vao nhip noi, filler words va do ro cua transcript."
    )

    if metrics.pace_label == "hoi cham":
        feedback.append(
            "Nhip noi: hoi cham. Diem tot la nguoi nghe co thoi gian theo doi, nhung neu keo dai ca bai thi bai thuyet trinh co the bi mat nang luong. Lan sau hay thu tang nhip o cac cau giai thich va giu pause cho nhung y quan trong."
        )
    elif metrics.pace_label == "hoi nhanh":
        feedback.append(
            "Nhip noi: hoi nhanh. Noi nhanh giup bai co nang luong, nhung nguoi nghe co the bo lo y chinh. Hay chen pause 1 giay sau moi cau chot va giam toc o cac doan co thuat ngu."
        )
    else:
        feedback.append(
            "Nhip noi: dang on dinh cho mot bai thuyet trinh. Hay giu nhip nay, nhung chu y them nhung khoang dung ngan sau cac y chinh de cau noi co diem nhan hon."
        )

    if metrics.filler_total == 0:
        feedback.append(
            "Filler words: rat sach, he thong khong phat hien filler word nao. Day la diem manh vi bai noi nghe gon va tu tin hon."
        )
    elif metrics.filler_per_minute <= 3:
        feedback.append(
            f"Filler words: co {metrics.filler_total} lan, khoang {metrics.filler_per_minute:.1f} lan/phut. Muc nay van on; lan sau thu thay filler bang mot khoang dung rat ngan de nghe tu nhien hon."
        )
    else:
        top_filler = _top_filler(metrics)
        filler_note = f" Tu xuat hien nhieu nhat la '{top_filler}'." if top_filler else ""
        feedback.append(
            f"Filler words: dang xuat hien kha nhieu, {metrics.filler_total} lan, khoang {metrics.filler_per_minute:.1f} lan/phut.{filler_note} Lan tap tiep theo, chi can tap trung giam mot filler pho bien nhat truoc."
        )

    if wer_value is not None:
        if wer_value <= 0.15:
            feedback.append(
                "Do ro transcript: ASR gan voi transcript chuan, cho thay audio va cach phat am dang kha tot."
            )
        elif wer_value <= 0.35:
            feedback.append(
                "Do ro transcript: ASR co sai khac vua phai so voi transcript chuan. Hay xem lai nhung tu bi nhan sai, thuong do la do noi nhanh, am cuoi khong ro hoac thuat ngu tieng Anh."
            )
        else:
            feedback.append(
                "Do ro transcript: ASR sai khac nhieu so voi transcript chuan. Nen thu record trong moi truong yen tinh hon, noi gan micro hon va tach cau dai thanh cac cum ngan."
            )
    else:
        feedback.append(
            "Do ro transcript: neu muon danh gia chinh xac hon, hay nhap transcript chuan de he thong tinh WER/CER va chi ra muc sai khac cua ASR."
        )

    if metrics.pace_label == "hoi nhanh":
        feedback.append(
            "Bai tap tiep theo: doc lai cung doan nay, moi khi het mot y hay dung 1 giay roi moi noi tiep."
        )
    elif metrics.filler_per_minute > 3:
        feedback.append(
            "Bai tap tiep theo: record lai mot lan nua va co y thay filler bang im lang ngan. Muc tieu la giam filler xuong duoi 3 lan/phut."
        )
    else:
        feedback.append(
            "Bai tap tiep theo: record them mot ban 60 giay, giu nhip hien tai va tap nhan manh ro hon o cau mo dau va cau ket."
        )

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
