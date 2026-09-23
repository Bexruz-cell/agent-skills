# Awesome Agentic Stack (Top 50 Open-Source Repositories)

> Курируемый каталог 50 лучших open-source библиотек, фреймворков и инструментов для создания надежных, автономных и ресурсоэффективных AI-агентов.

---

## Навигация

1. [Экономия токенов и сжатие контекста (10)](#1-экономия-токенов-и-сжатие-контекста)
2. [Агентные протоколы и стандарты (10)](#2-агентные-протоколы-и-стандарты)
3. [Долгосрочная память и стейт (5)](#3-долгосрочная-память-и-стейт)
4. [Аудит безопасности и верификация кода (10)](#4-аудит-безопасности-и-верификация-кода)
5. [Оркестрация мультиагентных систем (5)](#5-оркестрация-мультиагентных-систем)
6. [Быстрые локальные утилиты и AST-рантайм (5)](#6-быстрые-локальные-утилиты-и-ast-рантайм)
7. [Тестирование, валидация и трейсинг LLM (5)](#7-тестирование-валидация-и-трейсинг-llm)

---

## 1. Экономия токенов и сжатие контекста

1. **[microsoft/LLMLingua](https://github.com/microsoft/LLMLingua)** — Сжатие промптов до 20x без потери семантики и ключевого контекста задачи.
2. **[chroma-core/chroma](https://github.com/chroma-core/chroma)** — Локальная встраиваемая векторная БД для селективного контекста и снижения нагрузки на контекстное окно.
3. **[turboderp/exllamav2](https://github.com/turboderp/exllamav2)** — Сверхбыстрый локальный инференс квантованных LLM и эффективный менеджмент KV-кэша.
4. **[ggerganov/llama.cpp](https://github.com/ggerganov/llama.cpp)** — Легковесный C/C++ рантайм для локального исполнения моделей на CPU и GPU без тяжелых зависимостей.
5. **[guidance-ai/guidance](https://github.com/guidance-ai/guidance)** — Управление процессом генерации и строгий структурированный вывод без генерации мусорных токенов.
6. **[outlines-dev/outlines](https://github.com/outlines-dev/outlines)** — Строгая генерация по regex и JSON Schema для гарантированного формата и исключения ретраев.
7. **[stanford-crfm/dspy](https://github.com/stanford-crfm/dspy)** — Программный компилятор и оптимизатор промптов для минимизации токенов и роста точности.
8. **[BerriAI/litellm](https://github.com/BerriAI/litellm)** — Унифицированный прокси для кэширования, маршрутизации и контроля бюджета токенов между 100+ LLM.
9. **[vllm-project/vllm](https://github.com/vllm-project/vllm)** — Технология PagedAttention для высокопроизводительного обслуживания LLM с минимальной фрагментацией памяти.
10. **[huggingface/text-generation-inference](https://github.com/huggingface/text-generation-inference)** — Оптимизированный сервер для инференса LLM с тензорным параллелизмом и динамическим батчингом.

---

## 2. Агентные протоколы и стандарты

11. **[modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)** — Эталонные серверы Model Context Protocol (MCP) от Anthropic для стандартизации доступа агентов к инструментам и данным.
12. **[anthropics/anthropic-quickstarts](https://github.com/anthropics/anthropic-quickstarts)** — Эталонные архитектурные паттерны реализации computer use, работы с API и agentic tools.
13. **[run-llama/llama_index](https://github.com/run-llama/llama_index)** — Продвинутый фреймворк для структурирования, индексации и подключения внешних данных и кодовой базы к агентам.
14. **[langchain-ai/langchain](https://github.com/langchain-ai/langchain)** — Комплексная библиотека примитивов и абстракций для интеграции цепочек вызовов и инструментов.
15. **[langchain-ai/langgraph](https://github.com/langchain-ai/langgraph)** — Циклическая оркестрация отказоустойчивых агентов с явным контролем графа состояний и human-in-the-loop.
16. **[Significant-Gravitas/AutoGPT](https://github.com/Significant-Gravitas/AutoGPT)** — Индустриальный полигон, бенчмарки и архитектурные наработки автономных систем.
17. **[open-interpreter/open-interpreter](https://github.com/open-interpreter/open-interpreter)** — Локальное выполнение кода на Bash, Python и JavaScript под управлением LLM.
18. **[e2b-dev/E2B](https://github.com/e2b-dev/E2B)** — Изолированные облачные песочницы (microVM) для безопасного выполнения пользовательского и агентного кода.
19. **[All-Hands-AI/OpenHands](https://github.com/All-Hands-AI/OpenHands)** — Полнофункциональная агентная платформа для автономного написания кода, отладки и работы с терминалом.
20. **[cline/cline](https://github.com/cline/cline)** — Автономный агент для VS Code с обязательным human-in-the-loop подтверждением рискованных действий.

---

## 3. Долгосрочная память и стейт

21. **[mem0ai/mem0](https://github.com/mem0ai/mem0)** — Графовый слой персонализированной долговременной памяти для сохранения контекста между сессиями.
22. **[letta-ai/letta](https://github.com/letta-ai/letta)** — Управление виртуальной контекстной памятью в стиле операционной системы (бывший MemGPT).
23. **[qdrant/qdrant](https://github.com/qdrant/qdrant)** — Векторная база данных на Rust с богатой фильтрацией метаданных для быстрого семантического поиска по коду.
24. **[milvus-io/milvus](https://github.com/milvus-io/milvus)** — Распределённая облачная векторная база данных для масштабных корпоративных RAG-систем.
25. **[pgvector/pgvector](https://github.com/pgvector/pgvector)** — Векторный поиск поверх классической базы PostgreSQL без необходимости внедрения отдельного хранилища.

---

## 4. Аудит безопасности и верификация кода

26. **[PyCQA/bandit](https://github.com/PyCQA/bandit)** — Статический анализатор безопасности Python-кода на основе обхода AST для выявления уязвимостей.
27. **[semgrep/semgrep](https://github.com/semgrep/semgrep)** — Скоростной синтаксический сканер архитектурных антипаттернов и уязвимостей по декларативным правилам.
28. **[returntocorp/semgrep-rules](https://github.com/returntocorp/semgrep-rules)** — Официальная открытая база правил безопасности, лучших практик и проверок OWASP.
29. **[gitleaks/gitleaks](https://github.com/gitleaks/gitleaks)** — Быстрый детектор жестко закодированных секретов, паролей и API-токенов в git-истории и репозитории.
30. **[trufflesecurity/trufflehog](https://github.com/trufflesecurity/trufflehog)** — Поиск утекших ключей с энтропийным анализом и верификацией актуальности найденных секретов.
31. **[facebook/pyre-check](https://github.com/facebook/pyre-check)** — Высокопроизводительный тайп-чекер с глубоким анализом потоков данных (taint analysis) для поиска утечек.
32. **[google/atheris](https://github.com/google/atheris)** — Движок coverage-guided фаззинг-тестирования на основе LibFuzzer для поиска скрытых сбоев.
33. **[trailofbits/algo](https://github.com/trailofbits/algo)** — Скрипты и стандарты настройки защищенных сред, криптографии и аудита безопасности.
34. **[aquasecurity/trivy](https://github.com/aquasecurity/trivy)** — Универсальный сканер CVE в контейнерах, конфигурациях, файловых системах и зависимостях.
35. **[dependabot/dependabot-core](https://github.com/dependabot/dependabot-core)** — Движок автоматического мониторинга и обновления уязвимых пакетов в экосистемах Python, JS, Go и др.

---

## 5. Оркестрация мультиагентных систем

36. **[microsoft/autogen](https://github.com/microsoft/autogen)** — Фреймворк для диалогового взаимодействия и кооперации ансамбля специализированных агентов.
37. **[joaomdmoura/crewAI](https://github.com/joaomdmoura/crewAI)** — Фреймворк ролевого распределения задач между агентами (Product Manager, Backend Developer, QA Engineer).
38. **[geekan/MetaGPT](https://github.com/geekan/MetaGPT)** — Мультиагентная симуляция программной компании для генерации полноценных проектов по ТЗ.
39. **[princeton-nlp/SWE-bench](https://github.com/princeton-nlp/SWE-bench)** — Индустриальный бенчмарк для объективной оценки способности агентов автономно решать реальные задачи с GitHub.
40. **[BerriAI/litellm-proxy](https://github.com/BerriAI/litellm)** — Отказоустойчивый балансировщик нагрузки между LLM API с поддержкой ретраев, фолбэков и лимитов.

---

## 6. Быстрые локальные утилиты и AST-рантайм

41. **[astral-sh/ruff](https://github.com/astral-sh/ruff)** — Сверхбыстрый линтер и форматтер Python на Rust для поддержания чистоты кода без накладных расходов.
42. **[astral-sh/uv](https://github.com/astral-sh/uv)** — Мгновенный пакетный менеджер и рантайм на Rust для ускорения CI/CD и изоляции зависимостей.
43. **[pytest-dev/pytest](https://github.com/pytest-dev/pytest)** — Фундамент verification gates для автоматической проверки поведения и функционала кода.
44. **[pre-commit/pre-commit](https://github.com/pre-commit/pre-commit)** — Фреймворк запуска хуков валидации перед каждым коммитом для гарантии качества.
45. **[textualize/rich](https://github.com/textualize/rich)** — Форматирование информативного структурированного вывода и таблиц в терминале без лишнего спама.

---

## 7. Тестирование, валидация и трейсинг LLM

46. **[truera/trulens](https://github.com/truera/trulens)** — Инструментарий для оценки триады качества RAG, корректности ответов и защиты от галлюцинаций.
47. **[confident-ai/deepeval](https://github.com/confident-ai/deepeval)** — Юнит-тесты и метрики качества (G-Eval, Hallucination, Relevance) для агентных пайплайнов.
48. **[explodinggradients/ragas](https://github.com/explodinggradients/ragas)** — Фреймворк независимой оценки качества RAG-конвейеров по метрикам верности и релевантности.
49. **[Arize-ai/phoenix](https://github.com/Arize-ai/phoenix)** — Визуализация трейсов, оценка вызовов инструментов и отладка сложных многошаговых агентов.
50. **[Promptfoo/promptfoo](https://github.com/promptfoo/promptfoo)** — CLI-инструмент для фаззинга, тестирования безопасности и регрессионного анализа промптов.
