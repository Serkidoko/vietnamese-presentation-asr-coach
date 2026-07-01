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
conda create -y -n asr_coach python=3.11 pip
conda activate asr_coach
python -m pip install --upgrade pip
python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
pip install -r requirements.txt
```

Lenh tren tao conda env `asr_coach` va cai PyTorch CUDA wheel rieng cho NVIDIA GPU. Khong can cai CUDA Toolkit he thong de chay demo nay, mien la `nvidia-smi` nhan GPU va driver du moi.

Kiem tra GPU:

```powershell
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU')"
```

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
