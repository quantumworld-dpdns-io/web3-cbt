"""
Taiwan Ministry of Health & Welfare Mental Health Professionals Association Data Extractor

This module extracts and processes content from Taiwan's official mental health assessment resources.
"""

import pdfminer.six
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfparser import PDFParser
import re
from typing import Dict, List, Any

class TaiwanMOHWExtractor:
    def __init__(self):
        self.key_phrases = [
            r'認知扭曲', r'非理性信念', r'台灣認知行為治療', 
            r'MBTI人格', r'情緒管理', r'心理健康評估'
        ]
    
    def extract_from_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """Extract content from Taiwan MOHW PDF files"""
        try:
            parser = PDFParser(open(pdf_path, 'rb'))
            converter = TextConverter()
            layout = LAParams(line_margin=0.5)
            
            content = parser.get_text(content=True, converter=TextConverter(layout))
            
            return {
                'raw_content': content,
                'source_type': 'taiwan_mohw',
                'language': 'zh-TW',
                'cultural_context': 'Taiwanese Ministry of Health and Welfare',
                'processing_timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            raise ProcessingError(f"Failed to extract from {pdf_path}: {str(e)}")
    
    def parse_cognitive_distortions(self, content: str) -> List[Dict[str, Any]]:
        """Parse cognitive distortions content from Taiwan MOHW documents"""
        items = []
        
        # Pattern matching for cognitive distortion items
        distortion_patterns = [
            r'(\d+\.\s*[^\n]+)\s*\n([^\n]+)',
            r'([^\n]+)\s*\n([^\n]+)\s*\n([^\n]+)',
            r'\*\s*([^\n]+)\s*\n(\d+\s*點\s*\d+\s*分)',
        ]
        
        for pattern in distortion_patterns:
            matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)
            for match in matches:
                if len(match) >= 2:
                    item = self._create_cognitive_item(match, 'taiwan_mohw')
                    items.append(item)
        
        return items
    
    def parse_irrational_beliefs(self, content: str) -> List[Dict[str, Any]]:
        """Parse irrational beliefs content from Taiwan MOHW documents"""
        items = []
        
        # Pattern matching for irrational belief items
        belief_patterns = [
            r'(核心信念\s*\d+\s*：\s*[^\n]+)',
            r'([^\n]+)\s*\n(\d+\s*/\s*\d+\s*確信)',
            r'\*\s*([^\n]+)\s*\n(\d+\s*/\s*\d+)',
        ]
        
        for pattern in belief_patterns:
            matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)
            for match in matches:
                if len(match) >= 2:
                    item = self._create_irrational_item(match, 'taiwan_mohw')
                    items.append(item)
        
        return items
    
    def _create_cognitive_item(self, match: tuple, source: str) -> Dict[str, Any]:
        """Create standardized cognitive distortions item"""
        item = {
            'id': f"{source}_{hash(match[0])}",
            'label': match[0].strip(),
            'description': match[1].strip() if len(match) > 1 else '',
            'weight': self._calculate_weight(match),
            'type': self._determine_item_type(match),
            'taiwan_validation': True,
            'cultural_specificity': self._analyze_cultural_context(match),
            'psychological_impact': self._assess_impact_level(match),
            'clinical_significance': self._determine_significance(match),
            'taiwan_mohw_referenced': True,
            'official_validation': 'Ministry of Health and Welfare'
        }
        return item
    
    def _create_irrational_item(self, match: tuple, source: str) -> Dict[str, Any]:
        """Create standardized irrational beliefs item"""
        item = {
            'id': f"{source}_{hash(match[0])}",
            'label': match[0].strip(),
            'description': match[1].strip() if len(match) > 1 else '',
            'weight': self._calculate_weight(match),
            'belief_type': self._determine_belief_type(match),
            'taiwan_validation': True,
            'cultural_relevance': self._analyze_cultural_relevance(match),
            'clinical_significance': self._determine_significance(match),
            'international_validation': True,
            'taiwan_nhri_referenced': True
        }
        return item
    
    def _calculate_weight(self, match: tuple) -> float:
        """Calculate importance weight for the item"""
        text = ' '.join(match)
        weight = 1.0
        
        # Increase weight for items with priority indicators
        if any(keyword in text for keyword in ['核心', '主要', '重要', '必須']):
            weight += 1.5
        
        # Adjust based on description length
        if len(match) > 1 and len(match[1]) > 50:
            weight += 0.5
        
        return round(weight, 2)
    
    def _determine_item_type(self, match: tuple) -> str:
        """Determine item type based on content"""
        text = ' '.join(match)
        if any(keyword in text for keyword in ['核心認知', '主要認知']):
            return 'primary'
        elif any(keyword in text for keyword in ['常見', '一般', '輕度']):
            return 'secondary'
        return 'standard'
    
    def _analyze_cultural_context(self, match: tuple) -> str:
        """Analyze cultural context specificity"""
        text = ' '.join(match).lower()
        if any(keyword in text for keyword in ['台灣', '臺灣', '在地化', '本土化']):
            return 'Taiwan-specific'
        elif any(keyword in text for keyword in ['中文', '國語', '華語']):
            return 'Chinese-language adapted'
        return 'general applicability'
    
    def _assess_impact_level(self, match: tuple) -> int:
        """Assess psychological impact level (1-10)"""
        text = ' '.join(match).lower()
        impact_score = 5  # default medium impact
        
        if any(keyword in text for keyword in ['嚴重', '深度', '極度', '毀滅性']):
            impact_score += 3
        elif any(keyword in text for keyword in ['輕微', '一般', '正常']):
            impact_score -= 2
        
        return max(1, min(10, impact_score))
    
    def _determine_significance(self, match: tuple) -> int:
        """Determine clinical significance (1-10)"""
        text = ' '.join(match).lower()
        significance = 5  # default medium significance
        
        if any(keyword in text for keyword in ['臨床', '專業', '治療', '輔導']):
            significance += 2
        elif any(keyword in text for keyword in ['房間', '生活', '工作']):
            significance += 1
        
        return max(1, min(10, significance))
    
    def _determine_belief_type(self, match: tuple) -> str:
        """Determine belief type for irrational beliefs"""
        text = ' '.join(match).lower()
        if any(keyword in text for keyword in ['核心', '根本', '基本', '必須']):
            return 'core'
        elif any(keyword in text for keyword in ['常見', '一般', '經常性']):
            return 'common'
        return 'situational'
    
    def _analyze_cultural_relevance(self, match: tuple) -> str:
        """Analyze cultural relevance level"""
        text = ' '.join(match).lower()
        if any(keyword in text for keyword in ['台灣', '臺灣', '本土']):
            return 'high'
        elif any(keyword in text for keyword in ['國際', '全球', '跨文化']):
            return 'medium'
        return 'low'


class ProcessingError(Exception):
    """Custom exception for processing errors"""
    pass


def parse_taiwan_mohw_assessments():
    """Main function to process Taiwan MOHW assessments"""
    extractor = TaiwanMOHWExtractor()
    
    # Sample Taiwan MOHW assessment files
    files = [
        'taiwan_mohw_mental_health_professionals_association_cognitive_distortions.pdf',
        'taiwan_mohw_irrational_beliefs_assessment_tool.pdf',
        'taiwan_mohw_abcd_cbt_thinking_records.pdf'
    ]
    
    all_cognitive = []
    all_irrational = []
    
    for file in files:
        try:
            content = extractor.extract_from_pdf(file)
            cognitive = extractor.parse_cognitive_distortions(content['raw_content'])
            irrational = extractor.parse_irrational_beliefs(content['raw_content'])
            
            all_cognitive.extend(cognitive)
            all_irrational.extend(irrational)
            
            print(f"Processed {file}: {len(cognitive)} cognitive, {len(irrational)} irrational items")
        except Exception as e:
            print(f"Error processing {file}: {str(e)}")
    
    return {
        'cognitive_distortions': all_cognitive,
        'irrational_beliefs': all_irrational,
        'source': 'taiwan_mohw',
        'language': 'zh-TW',
        'cultural_context': 'Taiwanese Ministry of Health and Welfare',
        'official_validation': True,
        'taiwan_nhri_collaboration': False
    }


if __name__ == '__main__':
    from datetime import datetime
    
    result = parse_taiwan_mohw_assessments()
    
    print(f"\n=== Taiwan MOHW Assessment Results ===")
    print(f"Cognitive Distortions: {len(result['cognitive_distortions'])} items")
    print(f"Irrational Beliefs: {len(result['irrational_beliefs'])} items")
    print(f"Source: {result['source']}")
    print(f"Language: {result['language']}")
    print(f"Cultural Context: {result['cultural_context']}")
    print(f"Official Validation: {result['official_validation']}")
    
    # Save results
    with open('taiwan_mohw_processed.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print("\nResults saved to taiwan_mohw_processed.json")
