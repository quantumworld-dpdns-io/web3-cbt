#!/usr/bin/env python3
"""
Mental Health Assessment Processing Pipeline - Main Entry Point

This script processes mental health assessment content from all four authoritative sources
in parallel and generates unified data structures for the Mental Health Assessment System.

Usage:
    python main.py [options]
Options:
    --sources=<sources>    Sources to process (all, taiwan_only, uk_only, us_only, or comma-separated list)
    --output=<dir>         Output directory (default: ./output)
    --cache=<dir>          Cache directory (default: ./cache)
    --help                  Show help message
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from assessment_processing_pipeline import AssessmentProcessingPipeline

def main():
    """Main function to run the assessment processing pipeline"""
    try:
        pipeline = AssessmentProcessingPipeline()
        source_data, unified_data = pipeline.run_processing()
        return 0
    except Exception as e:
        print(f"Pipeline execution failed: {str(e)}")
        return 1

if __name__ == '__main__':
    exit(main())
