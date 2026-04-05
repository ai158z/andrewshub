class PythonTemplate:
    def render(self, template, context):
        import re
        
        if context is None:
            context = {}
        
        # Find all placeholders in the template
        placeholders = re.findall(r'\{\{([^}]+)\}\}', template)
        
        # Replace each placeholder with its value from context
        result = template
        for placeholder in placeholders:
            # Handle nested dictionary access
            keys = placeholder.split('.')
            value = context
            try:
                for key in keys:
                    if isinstance(value, dict) and key in value:
                        value = value[key]
                    else:
                        value = ""
                        break
                # If we found a valid value, use it, otherwise use empty string
                if value is None or value == "":
                    replacement = str(value)
                else:
                    replacement = str(value) if value is not None else ""
                result = result.replace("{{" + placeholder + "}}", replacement)
            except:
                result = result.replace("{{" + placeholder + "}}", "")
        
        # Handle any remaining placeholders that weren't replaced
        result = re.sub(r'\{\{[^}]+\}\}', '', result)
        
        return result