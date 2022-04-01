# NYUAD Hackathon for Social Good in the Arab World: Focusing on Quantum Computing (QC)

Our presentation link:
https://docs.google.com/presentation/d/1pV2jfIs-yF5SothISY-DPKJWXnUjSzNg_J6nmrlOq9U/edit#slide=id.g12101b9c8ea_0_37
https://nyuad.nyu.edu/en/events/2022/march/nyuad-hackathon-event.html

March 30 - April 1, 2022

# MedQure

With the recent surging concern over privacy, the use of secure algorithms that
assure the safety of user data has become more crucial than ever. The _MedQure_
team proposes a tumour classification system that completely secures the data of
clients through the use of Blind Quantum Computing. Since healthcare data is one
of the most private and sensitives data a user worries about, we were motivated
to utilize the power of quantum computing to make sure that users can go through
their medical tests with a clear mind and no concern about the security of their
data.

## Blind Quantum Computing

Quantum computers will tackle problems in different fields such as medical
research and finance, where the protection of sensitive data is a must. But
quantum computers on the cloud can be threaten for security, particulary when
delegating a potential data to such computers. Clients, with limited
computational ability, will want to use the services offered by quantum
computation and communication protocols, in a way that their privacy is
guaranteed.

In traditional (quantum/classical) cryptography, the server needs to decrypt the
data before doing any further computation. This can cause a problem if the
client's data is sensitive and the quantum computer is not trusted. This problem
can be solved using Blind Quantum Computing which enables arbitrary computation
on encrypted data without decryption. Blind Quantum Computing (BQC) allows
clients with limited computational ability to delegated computations to
untrusted quantum servers securely.

## Using Groover's algorithm for Tumour detection

In our system, Quantum computing isn't only used to secure the data of the user,
it is also used to efficiently detect brain tumors in MRI data through the use
of Grover's quantum search algorithm.

# Setup

1. Make sure you're using a conda environment with pythone 3.8.

2. If you don't have one, run this code in your terminal: 'conda create --name
   myenv'

3. 'pip install -r requirements.txt'

4. Run the Image Processing.ipynb notebook for a step by step runthrough of our
   method.
