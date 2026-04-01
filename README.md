# Dashcode

Dashcode is a specialized Python library for the programmatic generation of Geometry Dash levels (compatible with version 2.2+). It allows developers to build complex level structures, triggers, and gameplay mechanics entirely through code.

## Key Features

* **Class-Based Architecture**: All functionality is encapsulated within the `Dashcode` class for a clean developer experience.
* **Full Trigger Support**: Easily manage Group IDs, Alpha, Toggle, Rotate, and Camera Zoom parameters.
* **Verified Mapping**: Includes corrected IDs for critical items like the Checkpoint (2063) and TouchTrigger logic.
* **Extensible Logic**: Fully customizable object and parameter dictionaries via `setobjects()` and `setparams()`.
* **Direct GMD Export**: Encode and package your level data into a ready-to-import .gmd file format.

## Installation

```bash
pip install dashcode
