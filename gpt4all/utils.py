import ast
import black



class Utils:
    @staticmethod
    def is_valid_python(source_code):
        return not bool(ast.parse(source_code, mode='exec'))

    @staticmethod
    def extract_code(message):
        code_pattern = re.compile(r'```python([\s\S]*?)```')
        match = code_pattern.search(message)
        if match:
            code = match.group(1).strip()
            try:
                ast.parse(code)
                formatted_code = black.format_str(code, mode=black.FileMode())
                return formatted_code
            except (SyntaxError, black.InvalidInput):
                return f"Extracted code has syntax errors or couldn't be formatted:\n\n{code}"
        else:
            return message
