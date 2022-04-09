# qudra | قُدرة
*Quantum Energy Management*

[![License](https://img.shields.io/github/license/qcenergy/qudra.svg?style=popout-square)](https://opensource.org/licenses/Apache-2.0)
[![](https://img.shields.io/github/release/qcenergy/qudra.svg?style=popout-square)](https://github.com/qcenergy/qudra/releases)
[![](https://img.shields.io/pypi/dm/qudra.svg?style=popout-square)](https://pypi.org/project/qudra/)


## Motivation

**qudra**:  power, capacity, ability

Leveraging quantum advantage to optimize distributed grids for energy security and sustainability.

*Please check out these slides for more [information](https://www.canva.com/design/DAE8k9ZTusE/yADryUs2shHHs5LKuvO9pQ/view).*
## Installation

Our team's contribution is supposed to go into the `qudra` folder. So move there
```console
cd qudra
```

*Conda users, please make sure to `conda install pip` before running any pip installation if you want to install `qudra` into your conda environment.*

`qudra` is published on PyPI. So, to install, simply run:

```bash
pip install qudra
```
If you also want to download the dependencies needed to run optional tutorials, please use `pip install qudra[dev]` or `pip install 'qudra[dev]'` (for `zsh` users).


To check if the installation was successful, run:

```python
>>> import qudra
```

## Building from source

To build `qudra` from source, pip install using:

```bash
git clone https://github.com/qcenergy/qudra.git
cd qudra
pip install --upgrade .
```

If you also want to download the dependencies needed to run optional tutorials, please use `pip install --upgrade .[dev]` or `pip install --upgrade '.[dev]'` (for `zsh` users).


#### Installation for Devs

If you intend to contribute to this project, please install `qudra` in editable mode as follows:
```bash
git clone https://github.com/qcenergy/qudra.git
cd qudra
pip install -e .[dev]
```

python3 -m venv venv
. venv/bin/activate
Please use `pip install -e '.[dev]'` if you are a `zsh` user.

#### Building documentation locally

Set yourself up to use the `[dev]` dependencies. Then, from the command line run:
```bash
mkdocs build
```

Then, when you're ready to deploy, run:
```bash
mkdocs gh-deploy
```

## Acknowledgements

**Core Devs:** [Asil Qraini](https://github.com/AsilQ), [Fouad Afiouni](https://github.com/fo-ui), [Gargi Chandrakar](https://github.com/gargi2718), [Nurgazy Seidaliev](https://github.com/nursei7), [Sahar Ben Rached](https://github.com/saharbenrached), [Salem Al Haddad](https://github.com/salemalhaddad), [Sarthak Prasad Malla](https://github.com/SarthakMalla1154)

**Mentors:** [Akash Kant](https://github.com/akashkthkr), [Shantanu Jha](https://github.com/Phionx)

This project was created at the [2022 NYUAD Hackathon](https://nyuad.nyu.edu/en/events/2022/march/nyuad-hackathon-event.html) for Social Good in the Arab World: Focusing on Quantum Computing (QC). 

