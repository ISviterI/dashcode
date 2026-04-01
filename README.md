# Dashcode

[![Discord](https://img.shields.io/discord/1488880281376260186?color=7289da&label=discord&logo=discord&logoColor=white)](https://discord.gg/MXv3KTFmPE)

Dashcode is a specialized Python library for the programmatic generation of Geometry Dash levels (compatible with version 2.2+). It allows developers to build complex level structures, triggers, and gameplay mechanics entirely through code.

## Key Features

* **Class-Based Architecture**: All functionality is encapsulated within the `Dashcode` class for a clean developer experience.
* **Full Trigger Support**: Easily manage Group IDs, Alpha, Toggle, Rotate, and Camera Zoom parameters.
* **Verified Mapping**: Includes corrected IDs for critical items like the Checkpoint (2063) and TouchTrigger logic.
* **Extensible Logic**: Fully customizable object and parameter dictionaries via `setobjects()` and `setparams()`.
* **Direct GMD Export**: Encode and package your level data into a ready-to-import .gmd file format.
* **Timelines**: You can make a list of actions and objects like spawn or create to build easier using `build_timeline()`

## Examples
Check the `/examples` directory for advanced usage:
* `spikes_and_orbs.py` - Basic object placement.
* `prefabs.py` - Placing objects using prefabs
* `timeline_demo.py` - Using `build_timeline()` for synced events.


## Installation

```bash
pip install dashcode
