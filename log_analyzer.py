# System Log Analyzer

import re
import json
from collections import defaultdict

class LogAnalyzer:
    def __init__(self, log_file):
        self.log_file = log_file
        self.cpu_pattern = re.compile(r'CPU(?:\s+Usage)?\s*:\s*(\d+)%')
        self.memory_pattern = re.compile(r'Mem:\s*(\d+)MB/\d+MB\s*\(|Swap:\s*(\d+)MB/\d+MB\)')
        self.error_patterns = [
            re.compile(r'ERROR:\s*.+?\n', re.DOTALL),
            re.compile(r'Exception:\s*.+?\n', re.DOTALL),
            re.compile(r'Traceback:\s*.+?\n', re.DOTALL)
        ]
        self.metrics = {
            'cpu': [],
            'memory': [],
            'errors': [],
            'log_format': 'text'
        }
        self.analyze()

    def analyze(self):
        try:
            with open(self.log_file, 'r') as f:
                # Detect JSON format by testing first line
                first_line = f.readline().strip()
                try:
                    json.loads(first_line)
                    self.metrics['log_format'] = 'json'
                    f.seek(0)  # Reset file pointer
                    for line in f:
                        try:
                            json_line = json.loads(line)
                            self.parse_json_line(json_line)
                        except json.JSONDecodeError:
                            continue
                except json.JSONDecodeError:
                    self.metrics['log_format'] = 'text'
                    f.seek(0)  # Reset file pointer
                    for line in f:
                        self.parse_text_line(line)
        except FileNotFoundError:
            print(f'Error: Log file {self.log_file} not found')
            return

    def parse_text_line(self, line):
        cpu = self.cpu_pattern.search(line)
        if cpu:
            self.metrics['cpu'].append(int(cpu.group(1)))
            return
        
        memory = self.memory_pattern.search(line)
        if memory:
            mem = memory.group(1)
            swap = memory.group(2)
            if mem:
                self.metrics['memory'].append(int(mem))
            if swap:
                self.metrics['memory'].append(int(swap))
            return
        
        for error_pattern in self.error_patterns:
            error = error_pattern.search(line)
            if error:
                self.metrics['errors'].append(error.group(0).strip())
                return
        
    def parse_json_line(self, json_line):
        if 'cpu_usage' in json_line:
            self.metrics['cpu'].append(json_line['cpu_usage'])
        if 'memory_usage' in json_line:
            self.metrics['memory'].append(json_line['memory_usage'])
        if 'error' in json_line and json_line['error']:
            self.metrics['errors'].append(json_line['error'])

    def get_metrics(self):
        return {
            'cpu_usage': self.metrics['cpu'],
            'memory_usage': self.metrics['memory'],
            'errors': self.metrics['errors'],
            'log_format': self.metrics['log_format']
        }

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: python log_analyzer.py <log_file>')
        sys.exit(1)
    analyzer = LogAnalyzer(sys.argv[1])
    print(json.dumps(analyzer.get_metrics(), indent=2, default=str))}