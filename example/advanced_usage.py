#!/usr/bin/env python3
"""
Advanced usage examples showing custom instances and performance optimization.
"""

import logging
from jyutping2characters import JyutpingTranscriber, warmup, transcribe

def logging_examples():
    """Show different logging configurations."""
    print("1. Default (silent) behavior:")
    result = transcribe("gam1jat6")
    print(f"   gam1jat6 → {result}")
    print()

    print("2. Enable info logging:")
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    result = transcribe("nei5hou2")
    print(f"   nei5hou2 → {result}")
    print()

def performance_examples():
    """Show warmup and performance optimization."""
    print("Performance optimization with warmup:")
    print("warmup()  # Pre-load data for production")
    warmup()
    print("Now all transcriptions are instant!")
    
    examples = ["ngo5", "oi3", "nei5", "gam1jat6"]
    for jyutping in examples:
        result = transcribe(jyutping)
        print(f"  {jyutping} → {result}")
    print()

def custom_transcriber_example():
    """Example of creating a custom transcriber instance."""
    print("Custom transcriber with limited vocabulary:")
    
    # Create custom data - (chinese, jyutping, frequency)
    custom_data = [
        ("你好", "nei5hou2", 1000),
        ("再見", "zoi3gin3", 800),
        ("謝謝", "ze6ze6", 600),
        ("你", "nei5", 2000),
        ("好", "hou2", 1500),
    ]
    
    custom_transcriber = JyutpingTranscriber(custom_data)
    
    test_inputs = ["nei5hou2", "nei5", "hou2", "zoi3gin3"]
    for jyutping in test_inputs:
        result = custom_transcriber.transcribe(jyutping)
        print(f"  {jyutping} → {result}")
    print()

if __name__ == "__main__":
    logging_examples()
    performance_examples()
    custom_transcriber_example()
