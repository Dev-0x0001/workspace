import json
import plotly.express as px
import plotly.io as pio
from dataclasses import dataclass
from typing import Dict, List, Optional, Any

@dataclass
class VisualizationConfig:
    """Configuration for visualization settings."""
    theme: str = 'plotly_white'
    width: int = 800
    height: int = 600
    font_size: int = 12
    title_font_size: int = 16

class AdvancedVisualizer:
    """Advanced visualization class with interactive plots."""

    def __init__(self, config: Optional[VisualizationConfig] = None):
        self.config = config or VisualizationConfig()
        self.figures = {}
        self.last_modified = {}  , 