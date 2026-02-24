from typing import List, Dict, Any, Optional
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from datetime import datetime

class VisualizationManager:
    """Handles data visualization for reporting."""

    def __init__(self, style: str = 'seaborn'):
        """Initialize visualization manager."""
        sns.set_style(style)
        plt.style.use(style)

    def plot_metrics_over_time(
        self,
        metrics_data: Dict[str, List[Any]],
        title: str = 'Metrics Over Time',
        filename: Optional[str] = None
    ) -> plt.Figure:
        """Plot metrics over time."""
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # Convert data to DataFrame for easier handling
        df = pd.DataFrame(metrics_data)
        
        # Handle different cases
        if 'timestamp' in df.columns:
            x_column = 'timestamp'
        elif len(df.columns) == 1:
            x_column = range(len(df))
        else:
            x_column = df.columns[0]
            df = df.set_index(x_column)
        
        # Plot each metric column
        for column in df.columns:
            if column != x_column:
                ax.plot(
                    df.index if x_column == 'timestamp' else df[x_column],
                    df[column],
                    label=column,
                    marker='o',
                    linestyle='-',
 