# qudra
*Quantum Energy Management*
## Installation

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
git clone https://github.com/Q-Energy-2022/NYUAD-2022.git
cd qudra
pip install --upgrade .
```

If you also want to download the dependencies needed to run optional tutorials, please use `pip install --upgrade .[dev]` or `pip install --upgrade '.[dev]'` (for `zsh` users).


#### Installation for Devs

If you intend to contribute to this project, please install `qudra` in editable mode as follows:
```bash
git clone https://github.com/Q-Energy-2022/NYUAD-2022.git
cd qudra
pip install -e .[dev]
```
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

