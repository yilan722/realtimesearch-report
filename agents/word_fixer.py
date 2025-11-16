"""
单词修复器 - 使用字典直接修复被拆分的单词
这是一个全新的、更直接的方法，不依赖复杂的正则表达式
"""
import re
from typing import Dict


class WordFixer:
    """直接修复被拆分的单词"""
    
    # 完整的被拆分单词字典（按长度排序，长单词优先）
    SPLIT_WORDS_DICT: Dict[str, str] = {
        # 用户报告的问题单词（最高优先级）
        'R are': 'Rare',
        'r are': 'rare',
        'Mag net': 'Magnet',
        'mag net': 'magnet',
        'a dditional': 'additional',
        'A dditional': 'Additional',
        'a dditionally': 'additionally',
        'A dditionally': 'Additionally',
        'Ch in a': 'China',
        'ch in a': 'china',
        'Ch ina': 'China',
        'ch ina': 'china',
        'a nd': 'and',
        'A nd': 'And',
        
        # 其他常见拆分
        'a djusted': 'adjusted',
        'A djusted': 'Adjusted',
        'a nalyst': 'analyst',
        'A nalyst': 'Analyst',
        'a nticipated': 'anticipated',
        'A nticipated': 'Anticipated',
        'o perational': 'operational',
        'O perational': 'Operational',
        'p rior': 'prior',
        'P rior': 'Prior',
        'v alidates': 'validates',
        'V alidates': 'Validates',
        'e bitda': 'ebitda',
        'E bitda': 'EBITDA',
        'e ps': 'eps',
        'E ps': 'EPS',
        'E B I T D A': 'EBITDA',
        'E P S': 'EPS',
        'be at': 'beat',
        'Be at': 'Beat',
        
        # 更多常见拆分模式
        'Th e': 'The',
        'th e': 'the',
        'Th is': 'This',
        'th is': 'this',
        'Th at': 'That',
        'th at': 'that',
        'Co mpany': 'Company',
        'co mpany': 'company',
        'Re venue': 'Revenue',
        're venue': 'revenue',
        'Ma terial': 'Material',
        'ma terial': 'material',
        'Ma terials': 'Materials',
        'ma terials': 'materials',
        
        # 完全拆分的单词
        'o f t h e': 'of the',
        'o f': 'of',
        't h e': 'the',
        'i n': 'in',
        'a t': 'at',
        'i s': 'is',
        'o n': 'on',
        'b y': 'by',
        't o': 'to',
        'f o r': 'for',
        'a n d': 'and',
    }
    
    @staticmethod
    def fix_split_words(text: str) -> str:
        """
        直接修复被拆分的单词
        
        这个方法使用简单的字符串替换，按长度排序（长单词优先），
        确保所有被拆分的单词都能被正确修复。
        """
        if not text:
            return text
        
        # 按长度排序（长单词优先，避免部分匹配）
        sorted_words = sorted(
            WordFixer.SPLIT_WORDS_DICT.items(),
            key=lambda x: len(x[0]),
            reverse=True
        )
        
        # 逐个替换
        for split_word, correct_word in sorted_words:
            # 使用单词边界确保精确匹配
            # 但也要处理在句子中间的情况
            pattern = r'\b' + re.escape(split_word) + r'\b'
            text = re.sub(pattern, correct_word, text, flags=re.IGNORECASE)
            
            # 也处理不在单词边界的情况（如 "R are earth"）
            text = text.replace(split_word, correct_word)
        
        return text
    
    @staticmethod
    def fix_all_issues(text: str) -> str:
        """
        修复所有单词拆分问题（最终清理）
        
        这个方法会在所有其他清理之后调用，确保没有遗漏。
        """
        if not text:
            return text
        
        # 先移除markdown标记
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
        text = re.sub(r'__([^_]+)__', r'\1', text)
        text = text.replace('*', '').replace('_', '')
        
        # 修复被拆分的单词
        text = WordFixer.fix_split_words(text)
        
        # 规范化空格
        text = re.sub(r' {2,}', ' ', text)
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
        
        return text.strip()

