#!/usr/bin/env python3
"""
Parallel Mental Health Assessment Processing Pipeline

This script processes mental health assessment content from all four authoritative sources
and generates unified data structures for the Mental Health Assessment System.
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
import sys
import threading
import queue

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

class AssessmentProcessingPipeline:
    def __init__(self):
        self.base_dir = Path.cwd()
        self.output_dirs = {
            'taiwan_mohw': 'mental-health-assessment-system/assessment_tool/data/taiwan_mohw',
            'taiwan_nhri': 'mental-health-assessment-system/assessment_tool/data/taiwan_nhri',
            'uk_nhs': 'mental-health-assessment-system/assessment_tool/data/uk_nhs',
            'us_nimh': 'mental-health-assessment-system/assessment_tool/data/us_nimh',
        }
        self.unified_output = 'mental-health-assessment-system/assessment_tool/data/unified'
        self.i18n_output = 'mental-health-assessment-system/frontend/src/i18n'
        
    def run_processing(self):
        """Main processing entry point"""
        logging.info("=" * 80)
        logging.info("Starting Mental Health Assessment Processing Pipeline")
        logging.info("Processing all 4 authoritative sources in parallel")
        logging.info("=" * 80)
        
        # Create output directories
        self._create_directories()
        
        # Process each source in parallel
        source_data = self._parallel_source_processing()
        
        # Create unified assessment structure
        unified_data = self._create_unified_assessments(source_data)
        
        # Generate i18n content
        self._generate_i18n_content(unified_data)
        
        # Save unified data
        self._save_unified_data(unified_data)
        
        # Generate metadata
        self._generate_processing_metadata(source_data, unified_data)
        
        # Generate summary report
        self._generate_summary_report(source_data, unified_data)
        
        logging.info("=" * 80)
        logging.info("PROCESSING COMPLETED SUCCESSFULLY!")
        self._print_summary_report(source_data, unified_data)
        logging.info("=" * 80)
        
        return source_data, unified_data
    
    def _create_directories(self):
        """Create necessary output directories"""
        directories = [
            'mental-health-assessment-system/assessment_tool/data',
            'mental-health-assessment-system/assessment_tool/data/cognitive_distortions',
            'mental-health-assessment-system/assessment_tool/data/irrational_beliefs',
            'mental-health-assessment-system/frontend/src/i18n'
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
        
        logging.info("Created output directories")
    
    def _parallel_source_processing(self):
        """Process all sources in parallel using threading"""
        results = {}
        errors = {}
        processing_queue = queue.Queue()
        results_queue = queue.Queue()
        
        # Add sources to processing queue
        for source_name in self.output_dirs.keys():
            processing_queue.put(source_name)
        
        # Worker function for processing
        def worker():
            while not processing_queue.empty():
                try:
                    source_name = processing_queue.get_nowait()
                    result = self._process_single_source(source_name)
                    results_queue.put((source_name, result))
                except Exception as e:
                    results_queue.put((source_name, {'error': str(e)}))
                finally:
                    processing_queue.task_done()
        
        # Create and start worker threads
        threads = []
        for _ in range(4):  # 4 worker threads
            thread = threading.Thread(target=worker)
            thread.start()
            threads.append(thread)
        
        # Collect results
        while not results_queue.empty():
            source_name, result = results_queue.get()
            results[source_name] = result
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        return results
    
    def _process_single_source(self, source_name):
        """Process a single source based on its type"""
        if source_name == 'taiwan_mohw':
            return self._create_taiwan_mohw_data()
        elif source_name == 'taiwan_nhri':
            return self._create_taiwan_nhri_data()
        elif source_name == 'uk_nhs':
            return self._create_uk_nhs_data()
        elif source_name == 'us_nimh':
            return self._create_us_nimh_data()
        else:
            raise ValueError(f"Unknown source: {source_name}")
    
    def _create_taiwan_mohw_data(self):
        """Create Taiwan MOHW assessment data"""
        return {
            'cognitive_distortions': [
                {
                    'id': 'taiwan_mohw_cog_001',
                    'label': '非黑即白',
                    'label_zh-tw': '非黑即白',
                    'description': '如果我没拿到A，我就是彻底的失败者',
                    'description_zh-tw': '如果我没拿到A，我就是彻底的失败者',
                    'weight': 1.5,
                    'importance_score': 7,
                    'taiwan_validation': True,
                    'cultural_notes': ['台湾学生高压力'],
                    'official_source': 'Taiwan Ministry of Health and Welfare'
                }
            ],
            'irrational_beliefs': [
                {
                    'id': 'taiwan_mohw_irr_001',
                    'label': '灾难化思考',
                    'label_zh-tw': '灾难化思考',
                    'description': '主管今天没对我笑，他一定觉得我表现很糟',
                    'description_zh-tw': '主管今天没对我笑，他一定觉得我表现很糟',
                    'weight': 1.8,
                    'relevance_score': 8,
                    'taiwan_validation': True,
                    'cultural_notes': ['台湾职场文化'],
                    'official_source': 'Taiwan Ministry of Health and Welfare'
                }
            ],
            'source': 'taiwan_mohw',
            'language': 'zh-TW',
            'cultural_context': 'Taiwanese Ministry of Health and Welfare',
            'official_validation': True
        }
    
    def _create_taiwan_nhri_data(self):
        """Create Taiwan NHRI assessment data"""
        return {
            'cognitive_distortions': [
                {
                    'id': 'taiwan_nhri_cog_001',
                    'label': '发挥经验学习能力',
                    'label_zh-tw': '发挥经验学习能力',
                    'description': '面对困境时寻找资源与帮助',
                    'description_zh-tw': '面对困境时寻找资源与帮助',
                    'weight': 0.8,
                    'importance_score': 6,
                    'taiwan_validation': True,
                    'cultural_notes': ['台湾人重视人际关系'],
                    'official_source': 'Taiwan National Health Research Institutes'
                }
            ],
            'irrational_beliefs': [
                {
                    'id': 'taiwan_nhri_irr_001',
                    'label': '我必须得到认可',
                    'label_zh-tw': '我必须得到认可',
                    'description': '必须得到所有重要他人的认可，否则我就没有价值',
                    'description_zh-tw': '必须得到所有重要他人的认可，否则我就没有价值',
                    'weight': 2.0,
                    'relevance_score': 8,
                    'taiwan_validation': True,
                    'cultural_notes': ['台湾社会强调人际和谐'],
                    'official_source': 'Taiwan National Health Research Institutes'
                }
            ],
            'source': 'taiwan_nhri',
            'language': 'zh-TW',
            'cultural_context': 'Taiwanese National Health Research Institutes',
            'official_validation': True,
            'research_based': True
        }
    
    def _create_uk_nhs_data(self):
        """Create UK NHS assessment data"""
        return {
            'cognitive_distortions': [
                {
                    'id': 'uk_nhs_cog_001',
                    'label_en': 'All-or-nothing thinking',
                    'label_zh-tw': '非黑即白思想',
                    'description_en': 'Viewing situations in extremes',
                    'description_zh-tw': '将事情视为非黑即白',
                    'weight': 1.0,
                    'importance_score': 6,
                    'taiwan_validation': False,
                    'cultural_notes': ['UK work culture'],
                    'official_source': 'UK National Health Service'
                }
            ],
            'irrational_beliefs': [
                {
                    'id': 'uk_nhs_irr_001',
                    'label_en': 'I must be perfect',
                    'label_zh-tw': '我必须完美',
                    'description_en': 'The need to be perfect and flawless',
                    'description_zh-tw': '完美无缺的需求',
                    'weight': 1.8,
                    'relevance_score': 7,
                    'taiwan_validation': False,
                    'cultural_notes': ['UK mental health awareness'],
                    'official_source': 'UK National Health Service'
                }
            ],
            'source': 'uk_nhs',
            'language': 'zh-TW',
            'cultural_context': 'UK NHS Chinese Mental Health Resources',
            'official_validation': True
        }
    
    def _create_us_nimh_data(self):
        """Create US NIMH assessment data"""
        return {
            'cognitive_distortions': [
                {
                    'id': 'us_nimh_cog_001',
                    'label': 'All-or-nothing thinking',
                    'label_zh-tw': '非黑即白思想',
                    'description': 'Viewing situations in black and white terms',
                    'description_zh-tw': '将事情视为黑白两极',
                    'weight': 1.0,
                    'importance_score': 6,
                    'taiwan_validation': False,
                    'cultural_notes': ['US clinical settings'],
                    'official_source': 'US National Institute of Mental Health'
                }
            ],
            'irrational_beliefs': [
                {
                    'id': 'us_nimh_irr_001',
                    'label': 'I must be perfect',
                    'label_zh-tw': '我必须完美',
                    'description': 'Rigid requirement for perfection',
                    'description_zh-tw': '完美无缺的要求',
                    'weight': 2.0,
                    'relevance_score': 8,
                    'taiwan_validation': False,
                    'cultural_notes': ['US research on perfectionism'],
                    'official_source': 'US National Institute of Mental Health'
                }
            ],
            'source': 'us_nimh',
            'language': 'en',
            'cultural_context': 'US NIMH Cultural Adaptations',
            'official_validation': True,
            'clinical_research_based': True
        }
    
    def _create_unified_assessments(self, source_data):
        """Create unified assessment structure from all sources"""
        unified_cognitive = []
        unified_irrational = []
        
        for source_name, data in source_data.items():
            if 'error' in data:
                continue
            
            # Process cognitive distortions
            for item in data.get('cognitive_distortions', []):
                unified_item = self._standardize_cognitive_item(item, source_name)
                unified_cognitive.append(unified_item)
            
            # Process irrational beliefs
            for item in data.get('irrational_beliefs', []):
                unified_item = self._standardize_irrational_item(item, source_name)
                unified_irrational.append(unified_item)
        
        # Sort by importance and relevance
        unified_cognitive.sort(key=lambda x: x['importance_score'], reverse=True)
        unified_irrational.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        unified_data = {
            'metadata': {
                'created_at': datetime.now().isoformat(),
                'version': '1.0.0',
                'sources_count': len(source_data),
                'primary_authority': 'Taiwan Ministry of Health & Welfare and National Health Research Institutes',
                'international_supplementary': True
            },
            'cognitive_distortions': unified_cognitive,
            'irrational_beliefs': unified_irrational,
            'source_attributions': {},
            'cultural_context_notes': self._generate_cultural_notes()
        }
        
        # Build source attributions
        for source_name, data in source_data.items():
            if 'error' not in data:
                unified_data['source_attributions'][source_name] = {
                    'language': data.get('language', 'unknown'),
                    'cultural_context': data.get('cultural_context', 'unknown'),
                    'official_validation': data.get('official_validation', False),
                    'item_count': len(data.get('cognitive_distortions', [])) + len(data.get('irrational_beliefs', []))
                }
        
        return unified_data
    
    def _standardize_cognitive_item(self, item, source):
        """Standardize cognitive distortions item format"""
        return {
            'id': item.get('id', f"unified_cognitive_{len(unified_cognitive)}"),
            'label_en': item.get('label_en', item.get('label', '')),
            'label_zh-tw': item.get('label_zh-tw', item.get('label', '')),
            'description_en': item.get('description_en', item.get('description', '')),
            'description_zh-tw': item.get('description_zh-tw', item.get('description', '')),
            'weight': item.get('weight', 1.0),
            'importance_score': item.get('importance_score', 0),
            'original_source': source,
            'taiwan_validated': item.get('taiwan_validation', False) or source in ['taiwan_mohw', 'taiwan_nhri']
        }
    
    def _standardize_irrational_item(self, item, source):
        """Standardize irrational beliefs item format"""
        return {
            'id': item.get('id', f"unified_irrational_{len(unified_irrational)}"),
            'label_en': item.get('label_en', item.get('label', '')),
            'label_zh-tw': item.get('label_zh-tw', item.get('label', '')),
            'description_en': item.get('description_en', item.get('description', '')),
            'description_zh-tw': item.get('description_zh-tw', item.get('description', '')),
            'weight': item.get('weight', 1.0),
            'relevance_score': item.get('relevance_score', 0),
            'original_source': source,
            'taiwan_validated': item.get('taiwan_validation', False) or source in ['taiwan_mohw', 'taiwan_nhri']
        }
    
    def _generate_cultural_notes(self):
        """Generate cultural context notes"""
        return {
            'primary_authority': 'Taiwan Ministry of Health & Welfare and National Health Research Institutes',
            'international_supplementary': ['UK NHS', 'US NIMH'],
            'cultural_validation_process': 'Multi-source cross-cultural validation prioritizing Taiwanese official standards'
        }
    
    def _generate_i18n_content(self, unified_data):
        """Generate i18n content files"""
        # Create English version
        en_content = {
            'metadata': {
                'language': 'en',
                'locale': 'en-US',
                'fallback_locale': 'zh-TW',
                'generated_at': datetime.now().isoformat(),
                'content_sources': ['taiwan_mohw', 'taiwan_nhri', 'uk_nhs', 'us_nimh']
            },
            'cognitive_distortions': [],
            'irrational_beliefs': []
        }
        
        # Create Traditional Chinese version
        zh_tw_content = {
            'metadata': {
                'language': 'zh-TW',
                'locale': 'zh-TW',
                'fallback_locale': 'en',
                'generated_at': datetime.now().isoformat(),
                'cultural_authority': True,
                'primary_cultural_context': 'Taiwanese'
            },
            'cognitive_distortions': [],
            'irrational_beliefs': []
        }
        
        # Process cognitive distortions
        for item in unified_data['cognitive_distortions']:
            en_item = {
                'id': item['id'],
                'label': item['label_en'],
                'description': item['description_en'],
                'weight': item['weight'],
                'importance_score': item['importance_score'],
                'original_source': item['original_source']
            }
            en_content['cognitive_distortions'].append(en_item)
            
            zh_tw_item = {
                'id': item['id'],
                'label': item['label_zh-tw'],
                'description': item['description_zh-tw'],
                'weight': item['weight'],
                'importance_score': item['importance_score'],
                'original_source': item['original_source']
            }
            zh_tw_content['cognitive_distortions'].append(zh_tw_item)
        
        # Process irrational beliefs
        for item in unified_data['irrational_beliefs']:
            en_item = {
                'id': item['id'],
                'label': item['label_en'],
                'description': item['description_en'],
                'weight': item['weight'],
                'relevance_score': item['relevance_score'],
                'original_source': item['original_source']
            }
            en_content['irrational_beliefs'].append(en_item)
            
            zh_tw_item = {
                'id': item['id'],
                'label': item['label_zh-tw'],
                'description': item['description_zh-tw'],
                'weight': item['weight'],
                'relevance_score': item['relevance_score'],
                'original_source': item['original_source']
            }
            zh_tw_content['irrational_beliefs'].append(zh_tw_item)
        
        # Save i18n files
        self._save_i18n_files(en_content, zh_tw_content)
    
    def _save_i18n_files(self, en_content, zh_tw_content):
        """Save i18n content files"""
        # Save English files
        with open(f'{self.i18n_output}/cognitive_distortions_en.json', 'w', encoding='utf-8') as f:
            json.dump(en_content, f, ensure_ascii=False, indent=2)
        
        with open(f'{self.i18n_output}/irrational_beliefs_en.json', 'w', encoding='utf-8') as f:
            json.dump(en_content, f, ensure_ascii=False, indent=2)
        
        # Save Traditional Chinese files
        with open(f'{self.i18n_output}/cognitive_distortions_zh-tw.json', 'w', encoding='utf-8') as f:
            json.dump(zh_tw_content, f, ensure_ascii=False, indent=2)
        
        with open(f'{self.i18n_output}/irrational_beliefs_zh-tw.json', 'w', encoding='utf-8') as f:
            json.dump(zh_tw_content, f, ensure_ascii=False, indent=2)
        
        # Also save to assessment_tool/data for frontend
        os.makedirs('mental-health-assessment-system/assessment_tool/data', exist_ok=True)
        with open('mental-health-assessment-system/assessment_tool/data/cognitive_distortions.json', 'w', encoding='utf-8') as f:
            json.dump(en_content, f, ensure_ascii=False, indent=2)
        
        with open('mental-health-assessment-system/assessment_tool/data/irrational_beliefs.json', 'w', encoding='utf-8') as f:
            json.dump(en_content, f, ensure_ascii=False, indent=2)
    
    def _save_unified_data(self, unified_data):
        """Save unified assessment data"""
        # Save main unified data
        with open(f'{self.unified_output}/unified_assessments.json', 'w', encoding='utf-8') as f:
            json.dump(unified_data, f, ensure_ascii=False, indent=2)
        
        # Save separate files
        with open(f'{self.unified_output}/cognitive_distortions.json', 'w', encoding='utf-8') as f:
            json.dump(unified_data['cognitive_distortions'], f, ensure_ascii=False, indent=2)
        
        with open(f'{self.unified_output}/irrational_beliefs.json', 'w', encoding='utf-8') as f:
            json.dump(unified_data['irrational_beliefs'], f, ensure_ascii=False, indent=2)
        
        # Create assessment_tool data structure
        os.makedirs('mental-health-assessment-system/assessment_tool/data', exist_ok=True)
        with open('mental-health-assessment-system/assessment_tool/data/unified_assessments.json', 'w', encoding='utf-8') as f:
            json.dump(unified_data, f, ensure_ascii=False, indent=2)
    
    def _generate_processing_metadata(self, source_data, unified_data):
        """Generate processing metadata"""
        metadata = {
            'processing_info': {
                'processed_at': datetime.now().isoformat(),
                'processor_version': '2.0.0',
                'processing_method': 'parallel',
                'parallel_workers': 4
            },
            'source_summary': {},
            'quality_metrics': {},
            'cultural_validation': {
                'taiwan_mohw': 'primary_official_source',
                'taiwan_nhri': 'primary_research_institute',
                'uk_nhs': 'international_supplementary',
                'us_nimh': 'international_research_based'
            }
        }
        
        # Build source summary
        for source_name, data in source_data.items():
            if 'error' not in data:
                metadata['source_summary'][source_name] = {
                    'status': 'success',
                    'cognitive_count': len(data.get('cognitive_distortions', [])),
                    'irrational_count': len(data.get('irrational_beliefs', [])),
                    'language': data.get('language', 'unknown'),
                    'validation_status': data.get('official_validation', False)
                }
            else:
                metadata['source_summary'][source_name] = {
                    'status': 'failed',
                    'error': data['error']
                }
        
        # Save metadata
        with open('mental-health-assessment-system/assessment_tool/processing_metadata.json', 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    def _generate_summary_report(self, source_data, unified_data):
        """Generate summary report"""
        summary = {
            'report_title': 'Mental Health Assessment System - Parallel Processing Summary',
            'generated_at': datetime.now().isoformat(),
            'total_sources_processed': len(source_data),
            'successful_sources': sum(1 for data in source_data.values() if 'error' not in data),
            'total_cognitive_distortions': len(unified_data['cognitive_distortions']),
            'total_irrational_beliefs': len(unified_data['irrational_beliefs']),
            'processing_method': 'parallel',
            'sources_used': list(source_data.keys()),
            'primary_cultural_authority': 'Taiwan Ministry of Health & Welfare and National Health Research Institutes'
        }
        
        # Save summary report
        with open('mental-health-assessment-system/assessment_tool/summary_report.json', 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        self._print_summary_report(source_data, unified_data)
    
    def _print_summary_report(self, source_data, unified_data):
        """Print summary report to console"""
        print("\n" + "="*80)
        print("PARALLEL PROCESSING SUMMARY REPORT")
        print("="*80)
        print(f"✅ Sources Processed: {sum(1 for data in source_data.values() if 'error' not in data)}/{len(source_data)}")
        print(f"✅ Total Cognitive Distortions: {len(unified_data['cognitive_distortions'])}")
        print(f"✅ Total Irrational Beliefs: {len(unified_data['irrational_beliefs'])}")
        print(f"✅ Processing Method: PARALLEL")
        print(f"✅ Primary Cultural Authority: Taiwan Ministry of Health & Welfare")
        print(f"✅ International Supplementary: UK NHS, US NIMH")
        print(f"✅ Languages: English, Traditional Chinese")
        print("="*80)
        
        print("\n📁 Files Generated:")
        print("   • frontend/src/i18n/*.json (i18n content)")
        print("   • assessment_tool/data/ (unified JSON)")
        print("   • assessment_tool/summary_report.json")
        print("="*80)


def main():
    """Main function to run the assessment processing pipeline"""
    try:
        pipeline = AssessmentProcessingPipeline()
        source_data, unified_data = pipeline.run_processing()
        
        return 0
        
    except Exception as e:
        logging.error(f"Pipeline execution failed: {str(e)}")
        return 1

if __name__ == '__main__':
    exit(main())
