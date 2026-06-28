#!/usr/bin/env python3
"""
Mental Health Assessment System - Main Entry Point

This module serves as the primary entry point for running the assessment
processing pipeline.
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from assessment_processing_pipeline import main

if __name__ == "__main__":
    sys.exit(main())