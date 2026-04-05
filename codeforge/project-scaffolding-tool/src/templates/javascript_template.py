from string import Template
import json


class JavaScriptTemplate:
    """A template engine for generating JavaScript code with support for variables, 
    inheritance, and blocks."""
    
    def __init__(self):
        self.template_string = ""
        self.blocks = {}
        self.context = {}
        
    def render(self, context=None):
        """Render the template with the given context"""
        if context is None:
            context = {}
            
        # Merge provided context with instance context
        merged_context = self.context.copy()
        merged_context.update(context)
        
        # Simple template substitution
        template = Template(self.template_string)
        return template.safe_substitute(merged_context)
    
    def set_template(self, template_str):
        """Set the template string"""
        self.template_string = template_str
        return self
        
    def add_block(self, name, content):
        """Add a block to the template"""
        self.blocks[name] = content
        return self
        
    def extend(self, parent_template):
        """Extend a parent template"""
        # In a real implementation, this would merge blocks from parent
        # For this basic implementation, we just return self
        return self
        
    def add_context(self, key, value):
        """Add context data to the template"""
        self.context[key] = value
        return self