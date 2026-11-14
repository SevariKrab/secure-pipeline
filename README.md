ecure CI/CD Pipeline

Автоматизированный конвейер безопасности для проверки dockerfile и Docker-образов.

# Вся суть пайплайна
1.Custom Security Auditor (Python): проверяет `dockerfile` на опасные паттерны 
2.AI-агент: дополнительный слой LLM-проверки. Отправляет `dockerfile` в нейросеть через API для поиска логических ошибок и неочевидных уязвимостей
3.Build Docker Image: собирает образ из `dockerfile`
4.Trivy Scanner: проверяет собранный образ на уязвимости (CVE) уровня CRITICAL.
5.Fail-Safe: если аудитор или Trivy находят критическую проблему, пайплайн падает (красный крест), и код не пропускается дальше.

# Стек
* Языки и окружение: Python 3, YAML, Linux (Debian/Gentoo)
* Контейнеризация: Docker
* CI/CD: GitHub Actions, GitHub Secrets
* Безопасность: Trivy (SCA), Custom Python SAST, LLM

# Безопасность
Проект настроен на блокировку только критических уязвимостей (CRITICAL), чтобы не замедлять процесс разработки. Уязвимости более низкого ранга опасности (HIGH,MEDIUM,LOW) отфильтрованы. Для работы AI-агента требуется ключ `AI_API_KEY` (хранится в GitHub Secrets). Без ключа AI-проверка безопасно пропускается

# Тест (Скриншоты)

1. Пайплайн упал (Fail-Safe сработал)
Аудитор на Python нашел небезопасную команду, ИИ обнаружил логическую ошибку в dockerfile. Сборка была заблокирована
<img width="1559" height="749" alt="pipeline-failed" src="https://github.com/user-attachments/assets/b75b6a2d-a038-4c4c-af6d-a2a55782556b" />


2. Пайплайн прошел успешно (Все проверки пройдены)
Docker-образ успешно собран, Trivy не нашел критических уязвимостей. Нейросеть провела аудит и дала рекомендации по усилению безопасности (например, использование `distroless` образов и фиксация UID)
<img width="1565" height="745" alt="pipeline-success" src="https://github.com/user-attachments/assets/be47a0c9-6059-420f-b272-7195057790f9" />
