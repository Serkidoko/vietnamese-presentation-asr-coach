# Vietnamese Presentation ASR Coach

He thong ho tro luyen thuyet trinh tieng Viet dua tren nhan dang tieng noi tu dong, su dung `vinai/PhoWhisper-base`.

## Scope

- Upload audio bai thuyet trinh.
- Chuyen speech to text bang PhoWhisper-base.
- Hien thi transcript.
- Tinh thoi luong, so tu, WPM va filler words tieng Viet.
- Tinh WER/CER neu co transcript chuan.
- Tao feedback tong ket don gian.

## Tech stack

- Python
- Streamlit
- Hugging Face Transformers
- PyTorch
- Librosa/SoundFile

## Cai dat

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Neu PyTorch khong nhan GPU, cai lai PyTorch theo cau hinh CUDA tu trang chinh thuc cua PyTorch, sau do chay lai app.

Tren mot so moi truong Windows co the gap loi OpenMP trung `libiomp5md.dll` khi import PyTorch/Transformers. App dat `KMP_DUPLICATE_LIB_OK=TRUE` trong process de phuc vu demo local; neu lam ban nop chinh thuc, nen cai PyTorch/NumPy/Librosa trong mot virtual environment moi.

## Chay app

```powershell
streamlit run app.py
```

Lan dau chay, model `vinai/PhoWhisper-base` se duoc tai ve tu Hugging Face va cache tren may.

## Chay test nhanh

```powershell
python -m unittest discover
```

## Cau truc

```text
app.py
presentation_coach/
  asr.py
  audio.py
  analysis.py
  evaluation.py
  report.py
tests/
  test_analysis.py
  test_evaluation.py
```
