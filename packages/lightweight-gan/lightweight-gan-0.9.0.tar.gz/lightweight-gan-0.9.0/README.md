<img src="./sample.jpg" width="600px"></img>

*512x512 flowers after a day of training*

## 'Lightweight' GAN

[![PyPI version](https://badge.fury.io/py/lightweight-gan.svg)](https://badge.fury.io/py/lightweight-gan)

Implementation of <a href="https://openreview.net/forum?id=1Fqg133qRaI">'lightweight' GAN</a> proposed in ICLR 2021, in Pytorch. The main contributions of the paper is a skip-layer excitation in the generator, paired with autoencoding self-supervised learning in the discriminator. Quoting the one-line summary "converge on single gpu with few hours' training, on 1024 resolution sub-hundred images".

## Install

```bash
$ pip install lightweight-gan
```

## Usage

```bash
$ lightweight_gan --data ./path/to/images --image-size 512 --aug-prob 0.2
```

## Citations

```bibtex
@inproceedings{
    anonymous2021towards,
    title={Towards Faster and Stabilized {\{}GAN{\}} Training for High-fidelity Few-shot Image Synthesis},
    author={Anonymous},
    booktitle={Submitted to International Conference on Learning Representations},
    year={2021},
    url={https://openreview.net/forum?id=1Fqg133qRaI},
    note={under review}
}
```

```bibtex
@inproceedings{
    anonymous2021is,
    title={Is Attention Better Than Matrix Decomposition?},
    author={Anonymous},
    booktitle={Submitted to International Conference on Learning Representations},
    year={2021},
    url={https://openreview.net/forum?id=1FvkSpWosOl},
    note={under review}
}
```

```bibtex
@misc{woo2018cbam,
    title={CBAM: Convolutional Block Attention Module}, 
    author={Sanghyun Woo and Jongchan Park and Joon-Young Lee and In So Kweon},
    year={2018},
    eprint={1807.06521},
    archivePrefix={arXiv},
    primaryClass={cs.CV}
}
```

```bibtex
@misc{sinha2020topk,
    title={Top-k Training of GANs: Improving GAN Performance by Throwing Away Bad Samples},
    author={Samarth Sinha and Zhengli Zhao and Anirudh Goyal and Colin Raffel and Augustus Odena},
    year={2020},
    eprint={2002.06224},
    archivePrefix={arXiv},
    primaryClass={stat.ML}
}
```
