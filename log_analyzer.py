# System Log Analyzer

import re
import json
from collections import defaultdict

class LogAnalyzer:
    def __init__(self, log_file):
        self.log_file = log_file
        self.cpu_pattern = re.compile(r'CPU(?:\s+Usage)?\s*:\s*(\d+)%')
        self.memory_pattern = re.compile(r'Mem:\s*(\d+)MB/\d+MB\s*\(|Swap:\s*(\d+)MB/\d+MB\)')
        self.error_pattern = re.compile(r'ERROR:\s*.+?\n', re.DOTALL)
        self.metrics = {
            'cpu': [],
            'memory': [],
            'errors': []
        }
        self.analyze()

    def analyze(self):
        try:
            with open(self.log_file, 'r') as f:
                for line in f:
                    cpu = self.cpu_pattern.search(line)
                    if cpu:
                        self.metrics['cpu'].append(int(cpu.group(1)))
                        
                    memory = self.memory_pattern.search(line)
                    if memory:
                        mem = memory.group(1)
                        swap = memory.group(2)
                        self.metrics['memory'].append(int(mem or 0))
                        if swap:
                            self.metrics['memory'].append(int(swap))
                        
                    error = self.error_pattern.search(line)
                    if error:
                        self.metrics['errors'].append(error.group(0).strip())
        except FileNotFoundError:
            print(f'Error: Log file {self.log_file} not found')
            return
        
    def get_metrics(self):
        return {
            'cpu_usage': self.metrics['cpu'],
            'memory_usage': self.metrics['memory'],
            'errors': self.metrics['errors']
        }

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: python log_analyzer.py <log_file>')
        sys.exit(1)
    analyzer = LogAnalyzer(sys.argv[1])
    print(json.dumps(analyzer.get_metrics(), indent=2))