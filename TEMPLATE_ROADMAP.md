# Template Roadmap

Planned Copier templates to implement. Ordered by priority within each tier.

Existing templates: `barebone`, `classification`, `flow_matching`, `rl`, `MNIST_wandb_image_logger`

Inspiration sources: `inspiration_code/lightning-bolts/`, `inspiration_code/lightning-flash/`

---

## Template Infrastructure

Architectural improvements to the repo itself — not new ML templates.

### Template Directory Layout

All templates — existing (✅) and planned — mapped to their final locations.

```
templates/
  barebone/                       # ✅ root — gold standard reference

  core/                           # standard supervised learning
    classification/               # ✅ MNIST image classification (MNISTDataModule + ClassificationModule)
    segmentation/                 # 🔲 Tier 1 — U-Net, Dice loss, mIoU
    object_detection/             # 🔲 Tier 2 — Faster R-CNN / RetinaNet, mAP
    regression/                   # 🔲 Tier 2 — MLP on tabular data, R²

  generative/                     # generative models
    flow_matching/                # ✅ ODE-based flow matching (UNet denoiser, EulerSolver)
    vae/                          # 🔲 Tier 1 — ELBO loss, reparameterization, KL annealing
    diffusion/                    # 🔲 Tier 2 — DDPM/DDIM, noise schedule, reverse process
    gan/                          # 🔲 Tier 3 — DCGAN, two-optimizer training, FID
    super_resolution/             # 🔲 Tier 3 — SRGAN, perceptual loss, PSNR/SSIM

  rl/                             # reinforcement learning
    sac/                          # 🔲 split from monolithic rl — continuous actions, twin critics
    td3/                          # 🔲 split from monolithic rl — continuous actions, delayed policy update
    ppo/                          # 🔲 split from monolithic rl — on-policy, discrete + continuous
    dqn/                          # 🔲 split from monolithic rl — discrete actions, experience replay

  self_supervised/                # self-supervised learning
    contrastive_ssl/              # 🔲 Tier 1 — SimCLR / BYOL / SimSiam, NT-Xent, linear probe

  nlp/                            # natural language processing
    text_classification/          # 🔲 Tier 1 — HuggingFace backbone, BERT/RoBERTa, F1
    nano_lm/                      # 🔲 Tier 2 — GPT from scratch, causal LM, BPE/char tokenizer

  time_series/                    # sequential data
    forecasting/                  # 🔲 Tier 2 — TCN/Transformer, sliding window, SMAPE

  audio/                          # audio processing
    classification/               # 🔲 Tier 3 — Mel spectrogram, CNN, torchaudio

  graph/                          # graph neural networks
    classification/               # 🔲 Tier 3 — GCN/GAT, PyTorch Geometric, graph pooling
```

**RL split note:** The monolithic `rl/` template currently lives at `templates/rl/`. When it is split into per-algorithm templates, the subdirectories will be created inside `templates/rl/` — no further top-level restructuring needed.

### Copier Migration — COMPLETE
All four base templates have been migrated to Copier. Extensions are applied as a second `copier copy` pass and can be independently updated with `copier update --answers-file .copier-answers.<name>.yml`.

### Extensions
Add-ons that layer on top of a generated project via `copier copy path/to/extension . --trust`.

Existing extensions:
- `templates/extensions/image_logger` — WandB image logging callback (classification)

Planned extensions:

Planned extensions (in rough priority order):

| Extension | Description | Base template |
|---|---|---|
| `wandb_image_logger` | Log prediction images to W&B every N batches | `classification` |
| `wandb_artifacts` | Log model checkpoints and datasets as W&B Artifacts | any |
| `gradio_app` | Interactive inference demo with Gradio | any |
| `huggingface_page` | Push model to HF Hub + model card | any |

---

## Tier 1 — High Priority

### `vae` — Variational Autoencoder
**Donor:** `flow_matching`
**Inspiration:** `lightning-bolts/src/pl_bolts/models/autoencoders/basic_vae/`

Generative model with encoder-decoder + reparameterization trick. LightningModule handles ELBO (KL + reconstruction loss). Natural sibling to `flow_matching` — validates whether the generative template pattern generalizes. Build this first.

**New concepts:** ELBO loss, KL annealing, reparameterization sampler
**Hydra injectables:** encoder, decoder, sampler, optimizer, beta (KL weight)
**Cookiecutter options:** `latent_dim`, `dataset` (MNIST/CIFAR/custom), `beta_vae` (bool)

---

### `segmentation` — Semantic Segmentation
**Donor:** `classification`
**Inspiration:** `lightning-bolts/src/pl_bolts/models/vision/unet.py`, `lightning-flash/src/flash/image/segmentation/`

U-Net with skip connections, Dice + cross-entropy loss, mIoU metric, W&B mask overlay logging callback.

**New concepts:** U-Net encoder-decoder, Dice loss, mIoU, per-pixel prediction
**Hydra injectables:** model, loss, optimizer, scheduler
**Cookiecutter options:** `num_classes`, `dataset` (Cityscapes/VOC/custom), `loss` (dice/ce/combined)

---

### `contrastive_ssl` — Self-Supervised Learning
**Donor:** `flow_matching`
**Inspiration:** `lightning-bolts/src/pl_bolts/models/self_supervised/simclr/`, `byol/`, `simsiam/`

Two-stage training: contrastive pretraining (NT-Xent or BYOL loss) then linear probe finetuning with frozen backbone. Online KNN evaluation callback during pretraining.

**New concepts:** NT-Xent / BYOL loss, momentum encoder, augmentation pipeline, linear probe
**Hydra injectables:** backbone, projection_head, augmentation, loss, optimizer, scheduler
**Cookiecutter options:** `ssl_method` (simclr/byol/simsiam), `dataset`, `backbone` (resnet18/50/vit_s)

---

### `text_classification` — NLP Text Classification
**Donor:** `classification`
**Inspiration:** `lightning-flash/src/flash/text/classification/`

HuggingFace transformer backbone (BERT/RoBERTa/DistilBERT) with a classification head. Tokenization pipeline wired into the datamodule. F1 and accuracy metrics.

**New concepts:** HuggingFace tokenizer, transformer fine-tuning, token classification head
**Hydra injectables:** backbone (model name string), classifier_head, optimizer, scheduler
**Cookiecutter options:** `backbone` (bert-base/roberta-base/distilbert), `dataset` (csv/HF hub), `num_classes`
**Note:** Introduces HuggingFace dependency — keep the environment separate from vision templates.

---

## Tier 2 — Medium Priority

### `nano_lm` — Small Language Model Training
**Donor:** `flow_matching` (sequential generation pattern)
**Inspiration:** Andrej Karpathy's nanoGPT / nanoChat — *inspiration code not yet added*

Character-level or BPE GPT trained from scratch on a small corpus. Causal LM objective, gradient accumulation, learning rate warmup + cosine decay. A focused template for understanding transformer training fundamentals, not fine-tuning.

**New concepts:** causal attention, autoregressive training, text tokenization, generation sampling (temperature, top-k)
**Hydra injectables:** model (GPT config), tokenizer, optimizer, scheduler, sampler
**Cookiecutter options:** `tokenizer` (char/bpe), `dataset` (shakespeare/openwebtext/custom), `model_size` (nano/small/medium)
**Status:** Waiting on inspiration code — add nanoGPT to `inspiration_code/` before starting.

---

### `diffusion` — Diffusion Model
**Donor:** `flow_matching` (score-based generative model pattern)
**Inspiration:** *Not yet identified — find DDPM/DDIM reference implementation*

DDPM or DDIM with a U-Net denoiser, noise schedule, and reverse-process sampler. Closely related to `flow_matching` but uses discrete timestep noise schedules instead of ODE solvers.

**New concepts:** DDPM forward/reverse process, noise schedule (linear/cosine), DDIM sampling
**Hydra injectables:** denoiser (U-Net), noise_schedule, sampler (DDPM/DDIM), optimizer
**Cookiecutter options:** `schedule` (linear/cosine), `sampler` (ddpm/ddim), `dataset`
**Status:** Waiting on inspiration code — find a clean DDPM reference before starting.

---

### `object_detection` — Object Detection
**Donor:** `classification`
**Inspiration:** `lightning-bolts/src/pl_bolts/models/detection/faster_rcnn/`, `lightning-flash/src/flash/image/detection/`

Faster R-CNN or RetinaNet via torchvision detection API. mAP metric, bounding box W&B logging callback. Torchvision handles much of the loss computation internally.

**New concepts:** mAP, bbox logging, torchvision detection API, region proposal network
**Hydra injectables:** backbone, detector_head, optimizer, scheduler
**Cookiecutter options:** `detector` (faster_rcnn/retinanet), `dataset` (COCO/VOC/custom), `pretrained` (bool)

---

### `regression` — Tabular Regression
**Donor:** `barebone`
**Inspiration:** `lightning-bolts/src/pl_bolts/models/regression/`, `lightning-flash/src/flash/tabular/regression/`

MLP on structured/tabular data with MSE/MAE/Huber loss and R² metric. Simplest template after `barebone` — good entry point for newcomers and non-vision tasks.

**New concepts:** tabular datamodule, feature normalization, R² metric
**Hydra injectables:** model, loss, optimizer, normalizer
**Cookiecutter options:** `target_type` (single/multi), `loss` (mse/mae/huber), `input_format` (csv/numpy)

---

### `time_series` — Time Series Forecasting
**Donor:** `flow_matching`
**Inspiration:** `lightning-flash/src/flash/tabular/forecasting/`

Sliding-window dataset with Temporal Convolutional Network or Transformer backbone. Multi-step ahead forecasting with SMAPE/MAE metrics.

**New concepts:** sliding window dataset, multi-step forecasting, SMAPE, temporal normalization
**Hydra injectables:** model, loss, optimizer, scheduler, scaler
**Cookiecutter options:** `model_type` (tcn/transformer/lstm), `horizon`, `lookback`, `dataset` (etth/ettm/custom)

---

## Tier 3 — Lower Priority

### `super_resolution` — Image Super-Resolution (SRGAN)
**Donor:** `vae` or `gan` (once built)
**Inspiration:** `lightning-bolts/src/pl_bolts/models/gans/srgan/`

Perceptual loss (VGG features) + optional adversarial loss. Self-supervised pairs generated by random downsampling. PSNR/SSIM metrics.

**Cookiecutter options:** `scale_factor` (2/4/8), `loss` (perceptual/mse/combined), `dataset`

---

### `audio_classification` — Audio Classification
**Donor:** `classification`
**Inspiration:** `lightning-flash/src/flash/audio/classification/`

Waveform → Mel spectrogram → CNN classifier. Introduces `torchaudio` dependency and a non-trivial data preprocessing pipeline.

**Cookiecutter options:** `dataset` (ESC-50/UrbanSound/custom), `backbone` (cnn/efficientnet)

---

### `graph_classification` — Graph Neural Networks
**Donor:** `classification`
**Inspiration:** `lightning-flash/src/flash/graph/classification/`

GCN or GAT with PyTorch Geometric DataLoaders, graph-level classification pooling.

**Note:** PyTorch Geometric is a heavy dependency with platform-specific wheels. Narrow target audience.

---

### `gan` — Generative Adversarial Network (DCGAN)
**Donor:** `flow_matching`
**Inspiration:** `lightning-bolts/src/pl_bolts/models/gans/dcgan/`

DCGAN with two-optimizer adversarial training loop, FID metric callback, W&B image generation logging.

**Note:** Deprioritized — diffusion models and flow matching have largely superseded GANs for image generation. Still architecturally interesting for the two-optimizer LightningModule pattern but not a priority.

**Cookiecutter options:** `image_size`, `latent_dim`, `dataset`, `gan_type` (basic/dcgan/wgan)
