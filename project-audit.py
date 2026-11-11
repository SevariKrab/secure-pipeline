import sys
import re
import os

COLORS = {
    "RED": "\033[91m",
    "ORANGE": "\033[93m",
    "GREEN": "\033[92m",
    "RESET": "\033[0m",
    "CYAN": "\033[96m"
}

DANGEROUS_PATTERNS = {
    r"USER\s+root": {
        "msg": "КРИТИЧНО: Контейнер запускается от имени root",
        "color": COLORS["RED"]
    },
    r"ENV\s+.*(PASSWORD|TOKEN|SECRET|KEY)=": {
        "msg": "ВНИМАНИЕ: Возможная утечка секретных данных",
        "color": COLORS["ORANGE"]
    },
    r"ADD\s+": {
        "msg": "ВНИМАНИЕ: Использование ADD вместо COPY небезопасно",
        "color": COLORS["ORANGE"]
    },
    r"FROM\s+.*:latest": {
        "msg": "ВНИМАНИЕ: Тег 'latest' непредсказуем",
        "color": COLORS["ORANGE"]
    }
}

def audit_dockerfile(filepath):
    print(f"[*] Анализ файла: {filepath}")
    issues_found = 0
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"{COLORS['RED']}[-] Ошибка: Файл {filepath} не найден{COLORS['RESET']}")
        return False

    for line_num, line in enumerate(lines, 1):
        clean_line = line.strip()
        if clean_line.startswith('#'):
            continue
            
        for pattern, data in DANGEROUS_PATTERNS.items():
            if re.search(pattern, clean_line, re.IGNORECASE):
                color = data["color"]
                message = data["msg"]
                print(f"  [СТРОКА {line_num}] {color}{message}{COLORS['RESET']}")
                print(f"    -> {clean_line}")
                issues_found += 1

    if issues_found == 0:
        print(f"{COLORS['GREEN']}[+] Проблем не найдено. Конфигурация выглядит безопасной{COLORS['RESET']}")
        return True
    else:
        print(f"{COLORS['RED']}[-] Найдено проблем: {issues_found}{COLORS['RESET']}")
        return False

def ai_audit(file_content):
    api_key = os.environ.get("AI_API_KEY")

    if not api_key:
         print(f"\n{COLORS['CYAN']}[AI] Проверка пропущена: переменная AI_API_KEY не найдена{COLORS['RESET']}")
         return

    print(f"\n{COLORS['CYAN']}[AI] Ключ найден. Анализ dockerfile от ИИ{COLORS['RESET']}")

    try:
        from gigachat import GigaChat
        
        prompt = f"""Ты — эксперт по безопасности Docker. Проанализируй этот Dockerfile и найди потенциальные уязвимости или плохие практики. Ответь кратко, списком, только если есть реальные проблемы:

         {filecontent}"""

        with GigaChat(credentials=api_key, verify_ssl_certs=False, model="GigaChat-3-Ultra") as client:
            response = client.chat(prompt)
            print(f"{COLORS['CYAN']}[AI] Ответ GigaChat:{COLORS['RESET']}")
            print(response.choices[0].message.content)
            
    except Exception as e:
        print(f"{COLORS['ORANGE']}[AI] Ошибка при запросе к ИИ: {e}{COLORS['RESET']}")
        print(f"{COLORS['ORANGE']}[AI] ИИ-проерка пропущена, чтобы не ломать сборку{COLORS['RESET']}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python3 project-audit.py <путь_к_файлу>")
        sys.exit(1)
        
    target_file = sys.argv[1]
    is_secure = audit_dockerfile(target_file)

    try:
        with open(target_file, 'r', encoding='utf-8') as f:
            file_content = f.read()
        ai_audit(file_content)
    except FileNotFoundError:
        pass
    
    if not is_secure:
        sys.exit(1)