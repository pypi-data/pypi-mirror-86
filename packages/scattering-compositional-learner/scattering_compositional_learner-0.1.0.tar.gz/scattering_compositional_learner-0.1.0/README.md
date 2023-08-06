![image](scl.png)

# Scattering Compositional Learner
PyTorch implementation of Scattering Compositional Learner [1] for solving Raven's Progressive Matrices.

## Setup
```bash
$ pip install scattering_compositional_learner
```

## Usage
```python
import torch

from scattering_compositional_learner import ScatteringCompositionalLearner

x = torch.rand(4, 16, 160, 160)
scl = ScatteringCompositionalLearner(image_size=160)
logits = scl(x)
y_hat = logits.log_softmax(dim=-1)
y_hat  # torch.Tensor with shape (4, 8)
```

## Unit tests
```bash
$ python -m pytest tests
```

## Alternative implementations
The same model was additionally implemented by:
- [paper authors](https://github.com/dhh1995/SCL)
- [lucidrains](https://github.com/lucidrains/scattering-compositional-learner)

## Bibliography
[1] Wu, Yuhuai, et al. "The Scattering Compositional Learner: Discovering Objects, Attributes, Relationships in Analogical Reasoning." arXiv preprint arXiv:2007.04212 (2020).

## Citations
```bibtex
@article{wu2020scattering,
  title={The Scattering Compositional Learner: Discovering Objects, Attributes, Relationships in Analogical Reasoning},
  author={Wu, Yuhuai and Dong, Honghua and Grosse, Roger and Ba, Jimmy},
  journal={arXiv preprint arXiv:2007.04212},
  year={2020}
}
```
