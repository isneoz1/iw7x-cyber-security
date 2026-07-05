"""
Complete Catalog Loader - Load all 15,000+ cybersecurity tools
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional

class CatalogLoader:
    """Load and manage the complete cybersecurity tools catalog"""
    
    def __init__(self, catalog_path: Optional[str] = None):
        """Initialize catalog loader"""
        if catalog_path is None:
            # Try to find catalog in current directory or parent
            catalog_path = Path(__file__).parent.parent / 'catalog_complete.json'
        
        self.catalog_path = catalog_path
        self.catalog = None
        self.tools_cache = {}
        self.load_catalog()
    
    def load_catalog(self) -> bool:
        """Load catalog from JSON file"""
        try:
            with open(self.catalog_path, 'r') as f:
                self.catalog = json.load(f)
            print(f"✓ Catalog loaded: {self.get_tool_count()} tools in {self.get_category_count()} categories")
            return True
        except FileNotFoundError:
            print(f"✗ Catalog not found at {self.catalog_path}")
            return False
        except json.JSONDecodeError as e:
            print(f"✗ Invalid JSON in catalog: {e}")
            return False
    
    def get_category_count(self) -> int:
        """Get number of categories"""
        if not self.catalog:
            return 0
        return len(self.catalog.get('categories', []))
    
    def get_tool_count(self) -> int:
        """Get total number of tools"""
        if not self.catalog:
            return 0
        total = 0
        for category in self.catalog.get('categories', []):
            total += len(category.get('tools', []))
        return total
    
    def list_categories(self) -> List[str]:
        """List all category IDs"""
        if not self.catalog:
            return []
        return [cat['id'] for cat in self.catalog.get('categories', [])]
    
    def get_category(self, category_id: str) -> Optional[Dict[str, Any]]:
        """Get category by ID"""
        if not self.catalog:
            return None
        for category in self.catalog.get('categories', []):
            if category['id'] == category_id:
                return category
        return None
    
    def search_tools(self, query: str) -> List[Dict[str, Any]]:
        """Search tools by title or description"""
        if not self.catalog:
            return []
        
        results = []
        query_lower = query.lower()
        
        for category in self.catalog.get('categories', []):
            for tool in category.get('tools', []):
                title = tool.get('title', '').lower()
                desc = tool.get('description', '').lower()
                
                if query_lower in title or query_lower in desc:
                    results.append({
                        'tool': tool,
                        'category': category['id'],
                        'category_title': category['title']
                    })
        
        return results
    
    def get_tools_by_tag(self, tag: str) -> List[Dict[str, Any]]:
        """Get tools by tag"""
        if not self.catalog:
            return []
        
        results = []
        
        for category in self.catalog.get('categories', []):
            for tool in category.get('tools', []):
                tags = tool.get('tags', [])
                if tag in tags:
                    results.append({
                        'tool': tool,
                        'category': category['id'],
                        'category_title': category['title']
                    })
        
        return results
    
    def get_tools_by_os(self, os_type: str) -> List[Dict[str, Any]]:
        """Get tools for specific OS"""
        if not self.catalog:
            return []
        
        results = []
        os_type_lower = os_type.lower()
        
        for category in self.catalog.get('categories', []):
            for tool in category.get('tools', []):
                supported_os = [o.lower() for o in tool.get('os', [])]
                if os_type_lower in supported_os:
                    results.append({
                        'tool': tool,
                        'category': category['id'],
                        'category_title': category['title']
                    })
        
        return results
    
    def get_tools_by_category(self, category_id: str) -> List[Dict[str, Any]]:
        """Get all tools in a category"""
        category = self.get_category(category_id)
        if not category:
            return []
        
        return [
            {'tool': tool, 'category_id': category_id}
            for tool in category.get('tools', [])
        ]
    
    def get_essential_tools(self) -> List[Dict[str, Any]]:
        """Get essential/must-have tools"""
        if not self.catalog:
            return []
        
        results = []
        
        for category in self.catalog.get('categories', []):
            for tool in category.get('tools', []):
                tags = tool.get('tags', [])
                if 'essential' in tags:
                    results.append({
                        'tool': tool,
                        'category': category['id'],
                        'category_title': category['title']
                    })
        
        return results
    
    def export_category_list(self) -> str:
        """Export formatted category list"""
        if not self.catalog:
            return "No catalog loaded"
        
        lines = ["=== Cybersecurity Tools Catalog ===\n"]
        
        for category in self.catalog.get('categories', []):
            tool_count = len(category.get('tools', []))
            lines.append(f"📂 {category['title']} ({tool_count} tools)")
            lines.append(f"   ID: {category['id']}")
            lines.append(f"   {category.get('full_title', '')}\n")
        
        return "\n".join(lines)
    
    def get_tools_installable_on_kali(self) -> List[Dict[str, Any]]:
        """Get tools that can be installed on Kali Linux"""
        return self.get_tools_by_os('linux')
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get catalog statistics"""
        if not self.catalog:
            return {}
        
        stats = {
            'total_categories': self.get_category_count(),
            'total_tools': self.get_tool_count(),
            'meta': self.catalog.get('meta', {}),
            'supported_os': set(),
            'popular_tags': {}
        }
        
        # Collect OS and tag statistics
        for category in self.catalog.get('categories', []):
            for tool in category.get('tools', []):
                # OS stats
                for os in tool.get('os', []):
                    stats['supported_os'].add(os)
                
                # Tag stats
                for tag in tool.get('tags', []):
                    stats['popular_tags'][tag] = stats['popular_tags'].get(tag, 0) + 1
        
        stats['supported_os'] = list(stats['supported_os'])
        return stats


class ToolInstaller:
    """Install tools from catalog"""
    
    def __init__(self, catalog: CatalogLoader):
        self.catalog = catalog
        self.installation_log = []
    
    def install_category(self, category_id: str) -> Dict[str, Any]:
        """Install all tools in a category"""
        tools = self.catalog.get_tools_by_category(category_id)
        results = {
            'category': category_id,
            'total': len(tools),
            'success': 0,
            'failed': 0,
            'details': []
        }
        
        for item in tools:
            tool = item['tool']
            # This would normally call install logic
            results['details'].append({
                'tool': tool['title'],
                'status': 'pending'
            })
        
        return results


class CatalogStatistics:
    """Generate statistics from catalog"""
    
    @staticmethod
    def get_tools_by_difficulty(catalog: CatalogLoader) -> Dict[str, List[str]]:
        """Categorize tools by difficulty level"""
        difficulty_map = {
            'beginner': ['nmap', 'wireshark', 'sqlmap', 'nikto'],
            'intermediate': ['metasploit', 'burpsuite', 'ghidra', 'aircrack-ng'],
            'advanced': ['frida', 'radare2', 'yara', 'volatility']
        }
        return difficulty_map
    
    @staticmethod
    def get_framework_overview(catalog: CatalogLoader) -> Dict[str, int]:
        """Count tools by framework type"""
        frameworks = {}
        
        for category in catalog.catalog.get('categories', []):
            for tool in category.get('tools', []):
                tags = tool.get('tags', [])
                if 'framework' in tags:
                    framework_name = tool['title']
                    frameworks[framework_name] = frameworks.get(framework_name, 0) + 1
        
        return frameworks
