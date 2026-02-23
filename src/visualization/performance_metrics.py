import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from datetime import datetime

class VisualizationTools:
    """Collection of visualization methods for system analysis."""

    @staticmethod
    def plot_performance_metrics(metrics_data: dict, filename: str = 'performance_metrics.png'):
        """Plot performance metrics over time."""
        df = pd.DataFrame(metrics_data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        
        plt.figure(figsize=(14, 8))
        sns.lineplot(data=df.set_index('timestamp'), markers=True)
        plt.title('System Performance Metrics Over Time', fontsize=16)
        plt.xlabel('Timestamp', fontsize=12)
        plt.ylabel('Metrics', fontsize=12)
        plt.legend(title='Metrics')
        plt.grid(True)
        plt.savefig(filename)
        plt.close()

    @staticmethod
    def generate_compliance_report(compliance_data: dict, filename: str = 'compliance_report.html'):
        """Generate an HTML compliance report."""
        df = pd.DataFrame.from_dict(compliance_data, orient='index', columns=['value'])
        df['metric'] = df.index
        df['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        html = f""\