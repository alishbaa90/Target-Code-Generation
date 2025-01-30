import re

class Transpiler:
    def __init__(self):
        # Define tokens and patterns for punctuators, keywords, and other constructs
        self.tokens = [
            ('COMMENT', r'#.*'),                          # Python comments
            ('STRING', r'\".*?\"|\'.*?\''),               # String literals
            ('NUMBER', r'\b\d+(\.\d+)?\b'),               # Numbers
            ('IDENTIFIER', r'\b[A-Za-z_][A-Za-z0-9_]*\b'),# Identifiers
            ('ASSIGN', r'='),                             # Assignment operator
            ('ARITH_OP', r'[\+\-\*/%]'),                  # Arithmetic operators
            ('PAREN', r'[()]'),                           # Parentheses
            ('BRACE', r'[{}]'),                           # Braces
            ('COMMA', r','),                              # Comma
            ('COLON', r':'),                              # Colon
            ('NEWLINE', r'\n'),                           # Newline
            ('SPACE', r'[ \t]+'),                         # Whitespace
        ]

        # Compile token patterns
        self.token_regex = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.tokens))

        # Supported languages and corresponding templates
        self.supported_languages = {
            'python': self.transpile_python_to_cpp,
            'javascript': self.transpile_javascript_to_cpp,
            'java': self.transpile_java_to_cpp
        }

    def tokenize(self, code):
        """Tokenize the input source code."""
        tokens = []
        for match in self.token_regex.finditer(code):
            token_type = match.lastgroup
            value = match.group(token_type)
            if token_type != 'SPACE' and token_type != 'COMMENT':  # Skip whitespace and comments
                tokens.append((token_type, value))
        return tokens

    def transpile_python_to_cpp(self, code):
        """Transpile Python code to C++."""
        cpp_code = ["#include <iostream>", "#include <string>", "using namespace std;", "int main() {"]
        lines = code.split('\n')

        for line in lines:
            line = line.strip()
            if line.startswith('#'):
                cpp_code.append(f"    // {line[1:].strip()}")  # Convert Python comments to C++
            elif 'print' in line:
                # Handle print statements
                content = re.search(r'print\((.*)\)', line).group(1)
                cpp_code.append(f"    cout << {content.replace('.format(', ' + ').replace(')', '')} << endl;")
            elif '=' in line and '==' not in line:
                cpp_code.append(f"    auto {line};")  # Declare variables with `auto`
            elif line:
                cpp_code.append(f"    {line};")

        cpp_code.append("    return 0;")
        cpp_code.append("}")
        return '\n'.join(cpp_code)

    def transpile_javascript_to_cpp(self, code):
        """Transpile JavaScript code to C++."""
        cpp_code = ["#include <iostream>", "#include <string>", "using namespace std;", "int main() {"]
        lines = code.split('\n')

        for line in lines:
            line = line.strip()
            if line.startswith('//'):
                cpp_code.append(f"    {line}")  # JavaScript comments remain the same
            elif 'console.log' in line:
                # Handle console.log statements
                content = re.search(r'console\.log\((.*)\)', line).group(1)
                cpp_code.append(f"    cout << {content} << endl;")
            elif 'let ' in line or 'var ' in line or 'const ' in line:
                line = line.replace('let ', 'auto ').replace('var ', 'auto ').replace('const ', 'auto ')
                cpp_code.append(f"    {line};")
            elif line:
                cpp_code.append(f"    {line};")

        cpp_code.append("    return 0;")
        cpp_code.append("}")
        return '\n'.join(cpp_code)

    def transpile_java_to_cpp(self, code):
        """Transpile Java code to C++."""
        cpp_code = ["#include <iostream>", "#include <string>", "using namespace std;"]
        lines = code.split('\n')

        for line in lines:
            line = line.strip()
            if line.startswith('//'):
                cpp_code.append(f"    {line}")  # Java comments remain the same
            elif line.startswith('System.out.println'):
                # Handle System.out.println statements
                content = re.search(r'System\.out\.println\((.*)\)', line).group(1)
                cpp_code.append(f"    cout << {content} << endl;")
            elif 'int ' in line or 'double ' in line or 'String ' in line:
                cpp_code.append(f"    {line};")
            elif line:
                cpp_code.append(f"    {line};")

        cpp_code.append("    return 0;")
        cpp_code.append("}")
        return '\n'.join(cpp_code)

    def transpile(self, language, source_code):
        """Main transpiler function."""
        language = language.lower()
        if language not in self.supported_languages:
            raise ValueError(f"Unsupported language: {language}")

        transpile_function = self.supported_languages[language]
        return transpile_function(source_code)


# Main execution
if __name__ == "__main__":
    print("Welcome to the Language-to-C++ Transpiler!")
    print("This tool allows you to convert code written in Python, JavaScript, or Java into equivalent C++ code.")
    print("Supported languages: Python, JavaScript, Java.")

    while True:
        input_language = input("Enter the input language (or type 'exit' to quit): ").strip()
        if input_language.lower() == 'exit':
            break

        print("\nEnter the source code in the given language (end with an empty line):")
        source_code = []
        while True:
            line = input()
            if line.strip() == "":
                break
            source_code.append(line)

        source_code = "\n".join(source_code)

        try:
            transpiler = Transpiler()
            generated_cpp_code = transpiler.transpile(input_language, source_code)
            print("\nGenerated C++ Code:\n")
            print(generated_cpp_code)
        except Exception as e:
            print(f"\nError: {e}")

    print("\nThank you for using the Language-to-C++ Transpiler! Have a great day! 😊")
