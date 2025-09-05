#!/usr/bin/env python3
"""
Command-line interface examples for jyutping2characters.

This file demonstrates the various CLI commands available.
Run these commands in your terminal after installing the package.
"""

def cli_examples():
    """
    Examples of using the command-line interface.
    Copy and paste these commands into your terminal.
    """
    
    print("jyutping2characters CLI Examples")
    print("=" * 40)
    print()
    
    print("1. Basic transcription:")
    print("   jyutping2characters transcribe 'ngo5oi3nei5'")
    print("   # Output: 我愛你")
    print()
    
    print("2. Transcribe longer phrases:")
    print("   jyutping2characters transcribe 'gam1jat6hou2leng3'")
    print("   # Output: 今日好靚")
    print()
    
    print("3. Get information about the transcriber:")
    print("   jyutping2characters info")
    print("   # Shows version, cache status, and data statistics")
    print()
    
    print("4. Pre-warm for faster performance:")
    print("   jyutping2characters warmup")
    print("   # Pre-loads data into memory")
    print()
    
    print("5. Rebuild data cache with latest online data:")
    print("   jyutping2characters build-data")
    print("   # Downloads fresh data from GitHub sources")
    print()
    
    print("6. Clear cached data:")
    print("   jyutping2characters clear-cache")
    print("   # Next transcription will rebuild data")
    print()
    
    print("7. Get help:")
    print("   jyutping2characters --help")
    print("   jyutping2characters transcribe --help")
    print()

if __name__ == "__main__":
    cli_examples()
