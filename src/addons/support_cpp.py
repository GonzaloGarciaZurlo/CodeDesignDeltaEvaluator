"""
Support for C++ files to generate PlantUML files.
"""
import subprocess
import os
from pathlib import Path
from overrides import override
from src.cdde.addons_api import CddeAPI
from src.cdde.puml_generator import PumlGenerator
