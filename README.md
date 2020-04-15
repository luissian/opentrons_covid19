# Introduction
This is a collaboration repository originated with the work of [covidWarriors](https://www.covidwarriors.org/) in the implementation of [Opentrons](https://opentrons.com/) robots for the automatization of RT-PCR diagnostics of covid19.

In this repo a bunch of hospitals/insitutions collaborate sharing their protocols:
- **S2:** [BU-ISCIII](https://github.com/BU-ISCIII) is in charge of the setup, calibration, configuration, maintenance and protocol development for [OT-2 robots](https://opentrons.com/ot-2) in [Instituto de Salud Carlos III](https://www.isciii.es/Paginas/Inicio.aspx). These robots have been deployed to automate COVID-19 diagnostics, and once the pandemic is over they will be repurposed to suit new challenges.
- **Add remaining collaborators**

This repo is a copy of [opentrons'](https://github.com/Opentrons/opentrons) repo for covid19. 

In this repo you will find:

* The scripts that run on the robots, written with the [OT-2 Python Protocol API](https://docs.opentrons.com/v2/).
* [Labware definition](https://support.opentrons.com/en/articles/3136501-what-is-a-labware-definition) files.
* Some of our experimental notes and reports.

We're actively developing and testing these protocols, so things might be a little messy.  We're publishing our works in progress here so that other labs might benefit from them as quickly as possible.

# How to prepare the robots
- [OT-2 installation](doc/S3/01_OT2_installation.md)
- [Custom labware configuration](doc/S3/02_custom_labware.md)

# Reagent preparation and handling

Instructions for the manual part of this protocol (how to prepare reagents, how to set up labware, and so on) are hosted [on protocols.io](https://www.protocols.io/groups/opentrons-covid19-testing/publications).

# Protocols

We're automating a RT-qPCR based diagnostic protocol.  We split it into 3 parts, intended to be run on 3 separate robots:

* **Station A:** Sample intake
* **Station B:** RNA extraction
* **Station C:** qPCR setup

See [the Python files](protocols) for more details.

# Directory structure

* `/experiments` contains the exact Python scripts that were used for certain validation experiments, so we don't get confused about which experimental results correspond to which versions of our Python code.
* `/labware` contains the custom labware definitions necessary to run these protocols.  After cloning this repository, you should configure the Opentrons App to look in this directory. (Go to **More** > **Custom Labware** > **Labware Management** > **Custom Labware Definitions Folder**.)
* `/notebooks` is for stashing random Jupyter Notebooks that we're using for developing and debugging.
* `/protocols` is for the uploadable protocols themselves.

# Where to ask questions

If you have a question about what you see in this repository, please [post it as a GitHub issue](https://github.com/BU-ISCIII/covid19/tree/isciii/issues/new).
