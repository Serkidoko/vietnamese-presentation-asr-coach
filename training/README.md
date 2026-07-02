# Quick LoRA Fine-tune on VietSuperSpeech

Muc tieu: fine-tune nhe `vinai/PhoWhisper-base` bang LoRA tren mot sample nho cua `thanhnew2001/VietSuperSpeech`.

Huong nay dung de co mot phan training that trong bao cao mon ASR, nhung van du nhe de chay nhanh tren Google Colab GPU.

## Dataset

Dataset: `thanhnew2001/VietSuperSpeech`

Theo dataset card tren Hugging Face, VietSuperSpeech la dataset ASR tieng Viet dang hoi thoai, co cac cot:

- `audio`: duong dan audio `.wav`
- `text`: transcript
- `duration`: thoi luong
- `source`: file nguon

Script chi lay mot sample nho va download tung file audio can dung qua Hugging Face Hub, khong can tai toan bo dataset.

## Chay Tren Colab

1. Mo notebook:

```text
notebooks/finetune_phowhisper_lora_vietsuperspeech.ipynb
```

2. Chon GPU:

```text
Runtime -> Change runtime type -> T4 GPU
```

3. Chay cac cell theo thu tu.

Neu GitHub repo dang de private, cell clone repo trong notebook can `GITHUB_TOKEN` read-only. Cach don gian hon la doi repo sang public trong luc demo Colab.

Neu gap loi:

```text
ImportError: Found an incompatible version of torchao
```

Hay chay:

```bash
pip uninstall -y torchao
```

Sau do chay lai cell fine-tune. Notebook da co san buoc nay trong cell cai dependencies.

Lenh train mac dinh trong notebook:

```bash
python training/finetune_lora_vietsuperspeech.py \
  --train-samples 300 \
  --eval-samples 60 \
  --max-steps 100 \
  --batch-size 2 \
  --gradient-accumulation-steps 8
```

Output adapter:

```text
training_outputs/phowhisper-vss-lora
```

## Tang/Giam Do Nang

Nhanh hon:

```bash
--train-samples 120 --eval-samples 30 --max-steps 50
```

Dep hon cho bao cao:

```bash
--train-samples 800 --eval-samples 120 --max-steps 200
```

## Nen Bao Cao Gi

- Model goc: `vinai/PhoWhisper-base`
- Fine-tune method: LoRA
- Dataset: sample nho tu VietSuperSpeech
- Metric: WER tren validation sample
- Muc tieu: domain adaptation cho tieng Viet hoi thoai/thuyet trinh tu nhien

Vi dataset co transcript pseudo-label, ket qua nen duoc trinh bay la fine-tune thu nghiem quy mo nho, khong phai model production.
