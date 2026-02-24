from datetime import datetime, timedelta
import json
from typing import Dict, Any, List, Optional

class BaselineMeasurement:
    """Capture and analyze system baseline metrics"""

    def __init__(self):
        self.metrics = {
            'timestamp': datetime.now().isoformat(),
            'system': {},
            'memory': {},
            'swap': {},
            'filesystem': [],
            'processes': [],
            'cpu': {}
        }

    def capture_initial_state(self) -> 'BaselineMeasurement':
        """Capture comprehensive system baseline"""
        self.metrics['timestamp'] = datetime.now().isoformat()

        # CPU metrics
        with open('/proc/stat', 'r') as f:
            cpu_stats = f.readline().split()
            self.metrics['cpu'] = {
                'user': int(cpu_stats[1]),
                'nice': int(cpu_stats[2]),
                'system': int(cpu_stats[3]),
                'idle': int(cpu_stats[4]),
                'iowait': int(cpu_stats[5]),
                'irq': int(cpu_stats[6]),
                'softirq': int(cpu_stats[7])
            }

        # Processes
        with open('/proc/processes', 'r') as f:
            self.metrics['processes'] = [{'pid': int(line.split()[0]), 'name': line.split()[1]} for line in f]

        # Memory
        with open('/proc/meminfo', 'r') as f:
            mem_data = f.read().split('
')
            self.metrics['memory'] = {
                'total': int(mem_data[0].split()[1]),
                'free': int(mem_data[1].split()[1]),
                'buffers': int(mem_data[2].split()[1]),
                'cached': int(mem_data[3].split()[1]),
                'available': int(mem_data[17].split()[1])
            }

        # Swap
        self.metrics['swap'] = {
            'total': int(open('/proc/swaps', 'r').read().split('
')[1].split()[2]),
            'free': int(open('/proc/swaps', 'r').read().split('
')[1].split()[3]),
            'used': int(open('/proc/swaps', 'r').read().split('
')[1].split()[4])
        }

        # Filesystems
        with open('/proc/mounts', 'r') as f:
            mounted_filesystems = [line.split()[0] for line in f if line.split()[1] == 'ext4']

        for fs in mounted_filesystems:
            fs_metrics = self._get_filesystem_stats(fs)
            if fs_metrics:
                self.metrics['filesystem'].append(fs_metrics)

        return self

    def _get_filesystem_stats(self, mountpoint: str) -> Optional[Dict[str, Any]]:
        """Get stats for a specific filesystem"""
        try:
            with open(f'/sys/fs/ext4/{mountpoint}/super_blocks', 'r') as f:
                stats = f.read().split('
')
                return {
                    'mountpoint': mountpoint,
                    'total_blocks': int(stats[0].split(':')[1].strip()),
                    'free_blocks': int(stats[1].split(':')[1].strip()),
                    'used_blocks': int(stats[2].split(':')[1].strip()),
                    'block_size': int(stats[3].split(':')[1].strip())
                }
        except Exception:
            return None

    def to_json(self) -> str:
        """Convert metrics to JSON string"""
        return json.dumps(self.metrics, indent=4)

    def save(self, filename: str) -> None:
        """Save metrics to file"""
        with open(filename, 'w') as f:
            f.write(self.to_json())