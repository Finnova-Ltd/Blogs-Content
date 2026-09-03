import re

def sync_widget():
    widget_path = "cloudflare/chat-agent/public/widget.js"
    index_path = "cloudflare/chat-agent/src/index.ts"

    with open(widget_path, "r", encoding="utf-8") as f:
        widget_code = f.read()

    # Escape backticks and ${} for insertion into TypeScript template literal
    escaped_widget = widget_code.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")

    with open(index_path, "r", encoding="utf-8") as f:
        index_code = f.read()

    pattern = r"(const WIDGET_SCRIPT = `)[\s\S]*?(`;\s*\n// Centralized Standalone Cookie Consent)"
    
    match = re.search(pattern, index_code)
    if not match:
        print("Pattern match failed!")
        return False

    new_index_code = index_code[:match.start(1)] + "const WIDGET_SCRIPT = `" + escaped_widget + index_code[match.end(1) + (match.end() - match.end(1) - len(match.group(2))):]
    # More robust replacement using regex sub
    def repl(m):
        return m.group(1) + escaped_widget + m.group(2)

    new_index_code, count = re.subn(pattern, repl, index_code)
    if count != 1:
        print(f"Failed to replace exactly once, replaced {count} times")
        return False

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(new_index_code)

    print("Successfully synchronized WIDGET_SCRIPT into index.ts!")
    return True

if __name__ == "__main__":
    sync_widget()
