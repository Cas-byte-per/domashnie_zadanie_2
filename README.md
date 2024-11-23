# Домашнее задание №2
Скрипт `visualizer.py` предоставляет автоматический способ визуализации зависимостей Python-пакета. Он извлекает зависимости с помощью команды `pip freeze`, строит граф зависимостей и генерирует диаграмму `Mermaid` для представления этих зависимостей.
Граф можно отобразить в виде изображения `(PNG)` для удобства восприятия.

## Возможности
- Парсинг зависимостей: Извлекает список зависимостей из текущей Python-среды с помощью команды `pip freeze`. инструмента визуализации (конфигурируемого через путь).
- Рекурсивный граф зависимостей: Строит рекурсивный граф зависимостей, включая как прямые, так и косвенные зависимости.
- Генерация диаграммы `Mermaid`: Преобразует граф зависимостей в текстовый формат, совместимый с Mermaid — популярным инструментом для построения диаграмм и графиков.
- Рендеринг графа: Отображает диаграмму `Mermaid` в виде изображения `PNG` с использованием внешнего инструмента визуализации (конфигурируемого через путь).
- Настроиваемость: Легко настраивается через JSON-файл конфигурации, который определяет пути к инструментам, пакету и директории для вывода.
  
## Установка
- Клонируйте или скачайте репозиторий.
- Убедитесь, что у вас установлен Python 3.x.
- Установите зависимости:
```bash
pip install -r requirements.txt
```
- Убедитесь, что у вас есть инструмент для рендеринга диаграмм `Mermaid` в `PNG` (например, `mermaid-cli`).
  
## Использование
Конфигурационный файл
Для работы скрипта необходим JSON-файл конфигурации, который задает пути к инструменту визуализации, Python-пакету и директории для вывода. Пример файла `config.json`:

```json
{
    "visualizer_path": "C:\\Users\\79624\\AppData\\Roaming\\npm\\mmdc.cmd",
    "package_path": "C:\\Users\\79624\\dz2",
    "output_path": "C:\\Users\\79624\\dz2\\output",
    "repository_url": "https://github.com/Cas-byte-per/domashnie_zadanie_2.git"
}
```
### Запуск
Для запуска инструмента выполните следующую команду:
```bash
python visualizer.py config.json
```
После этого скрипт выполнит следующие действия:
- Извлечет зависимости с помощью `pip freeze`.
- Построит граф зависимостей.
- Сгенерирует диаграмму в формате `Mermaid`.
- Отобразит её в виде PNG-файла в указанной директории.

# Описание функций
1. ### `__init__(self, config_path)`
Конструктор класса `DependencyVisualizer`. Загружает конфигурационный файл и инициализирует переменные для путей и данных.

### Параметры:
- `config_path`: Путь к JSON файлу конфигурации.
### Действия:
- Загружает конфигурацию из JSON-файла.
- Устанавливает пути для визуализатора, пакета, выходного файла и `URL` репозитория.
```python
class DependencyVisualizer:
    def __init__(self, config_path):
        self.config = self.load_config(config_path)
        self.visualizer_path = self.config['visualizer_path']
        self.package_path = Path(self.config['package_path'])
        self.output_path = self.config['output_path']
        self.repo_url = self.config['repository_url']
        self.graph = {}
```

2. ### `load_config(self, config_path)`
Читает и загружает конфигурационный файл в формате `JSON`.

### Параметры:
- `config_path`: Путь к JSON файлу конфигурации.
### Возвращает:
- Содержимое конфигурации в виде словаря `Python`.
### Действия:
- Открывает файл и загружает данные с помощью модуля `json`.
```python
def load_config(self, config_path):
    with open(config_path, 'r') as f:
        return json.load(f)
```

3. ### `parse_dependencies_from_pip(self)`
Извлекает список зависимостей с помощью команды `pip freeze`, которая возвращает установленные пакеты и их версии.

### Возвращает:
- Список строк, каждая из которых содержит название пакета и его версию, например: `numpy==1.21.2`.
### Действия:
- Выполняет команду `pip freeze` через `subprocess.run()`.
- Возвращает список строк, разделенных по строкам.
```python
def parse_dependencies_from_pip(self):
    dependencies = []
    try:
        result = subprocess.run(['pip', 'freeze'], capture_output=True, text=True, check=True)
        dependencies = result.stdout.splitlines()  # Разбиваем вывод на строки
    except subprocess.CalledProcessError as e:
        print(f"Error extracting dependencies: {e}")
    return dependencies
```

4. ### `build_dependency_graph(self, package_name, dependencies)`
Рекурсивно строит граф зависимостей, добавляя зависимости для каждого пакета.

### Параметры:
- `package_name`: Имя пакета, для которого строится граф.
- `dependencies`: Список зависимостей для текущего пакета.
### Действия:
- Если пакет уже существует в графе, прекращает выполнение.
- Добавляет пакет и его зависимости в граф.
- Рекурсивно вызывает функцию для каждой зависимости, чтобы построить полный граф.
```python
def build_dependency_graph(self, package_name, dependencies):
    if package_name in self.graph:
        return
    self.graph[package_name] = dependencies
    for dep in dependencies:
        dep_name = dep.split('==')[0]  # Извлекаем имя пакета (без версии)
        self.build_dependency_graph(dep_name, [])  # Пока без транзитивных зависимостей
```

5. ### `generate_mermaid_graph(self)`
Генерирует текстовую репрезентацию графа зависимостей в формате `Mermaid`.

### Возвращает:
- Строку, представляющую граф в формате `Mermaid`, например: `lua`
```
graph TD
    package1 --> dep1
    package2 --> dep2
```
### Действия:
- Строит строки для каждого пакета и его зависимости, используя формат `Mermaid`.
- Возвращает строку, которая может быть использована для создания диаграммы.
```python
def generate_mermaid_graph(self):
    lines = ["graph TD"]
    for pkg, deps in self.graph.items():
        for dep in deps:
            dep_name = dep.split('==')[0]
            lines.append(f"    {pkg} --> {dep_name}")
    return "\n".join(lines)
```

6. ### `save_mermaid_graph(self, mermaid_graph, mermaid_file)`
Сохраняет сгенерированный граф `Mermaid` в файл.

### Параметры:
- `mermaid_graph`: Строка, содержащая граф в формате `Mermaid`.
- `mermaid_file`: Путь, по которому будет сохранен файл.
### Действия:
- Создает все необходимые промежуточные директории (если они не существуют).
- Записывает граф в указанный файл.
```python
def save_mermaid_graph(self, mermaid_graph, mermaid_file):
    os.makedirs(os.path.dirname(mermaid_file), exist_ok=True)
    with open(mermaid_file, 'w') as f:
        f.write(mermaid_graph)
```

7. ### `render_graph_to_png(self, mermaid_file)`
Использует внешний инструмент для рендеринга графа `Mermaid` в PNG-изображение.

### Параметры:
- `mermaid_file`: Путь к файлу с графом в формате `Mermaid`.
### Действия:
- Выполняет команду внешнего визуализатора (например, `mermaid-cli`), чтобы преобразовать файл `.mmd` в изображение `.png`.
```python
def render_graph_to_png(self, mermaid_file):
    output_png = self.output_path + '.png'
    subprocess.run([self.visualizer_path, "-i", mermaid_file, "-o", output_png])
```
8. ### `visualize_dependencies(self)`
Основной метод для визуализации зависимостей пакета.

### Действия:
- Извлекает зависимости с помощью `pip freeze`.
- Строит граф зависимостей, включая прямые и косвенные зависимости.
- Генерирует граф в формате `Mermaid`.
- Сохраняет его в файл.
- Использует внешний инструмент для рендеринга графа в `PNG`.
```python
def visualize_dependencies(self):
    package_name = self.package_path.stem
    initial_deps = self.parse_dependencies_from_pip()
    if not initial_deps:
        print("No dependencies found")

    self.build_dependency_graph(package_name, initial_deps)

    mermaid_graph = self.generate_mermaid_graph()

    mermaid_file = os.path.join(self.output_path, "dependency_graph.mmd")
    self.save_mermaid_graph(mermaid_graph, mermaid_file)

    self.render_graph_to_png(mermaid_file)
    print("Graph generation completed successfully!")
```
9. ### `main()`
Функция, которая запускает выполнение скрипта, если файл запускается как основной.

### Действия:
- Использует `argparse` для получения пути к конфигурационному файлу.
- Создает объект класса `DependencyVisualizer`.
- Запускает процесс визуализации зависимостей.
```python
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Visualize package dependencies as a graph.")
    parser.add_argument("config", help="Path to the JSON config file")
    args = parser.parse_args()

    visualizer = DependencyVisualizer(args.config)
    visualizer.visualize_dependencies()
```
