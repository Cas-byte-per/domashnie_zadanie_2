import json
import os
import subprocess
from pathlib import Path


class DependencyVisualizer:
    def __init__(self, config_path):
        # Загружаем конфигурацию
        self.config = self.load_config(config_path)
        self.visualizer_path = self.config['visualizer_path']
        self.package_path = Path(self.config['package_path'])
        self.output_path = self.config['output_path']
        self.repo_url = self.config['repository_url']
        self.graph = {}

    def load_config(self, config_path):
        # Чтение конфигурационного файла JSON
        with open(config_path, 'r') as f:
            return json.load(f)

    def parse_dependencies_from_pip(self):
        # Извлекаем зависимости из установленного пакета с помощью pip freeze
        dependencies = []
        try:
            result = subprocess.run(['pip', 'freeze'], capture_output=True, text=True, check=True)
            dependencies = result.stdout.splitlines()  # Разбиваем вывод на строки
        except subprocess.CalledProcessError as e:
            print(f"Error extracting dependencies: {e}")
        return dependencies

    def build_dependency_graph(self, package_name, dependencies):
        # Рекурсивное построение графа зависимостей
        if package_name in self.graph:
            return
        self.graph[package_name] = dependencies
        for dep in dependencies:
            dep_name = dep.split('==')[0]  # Извлекаем имя пакета (без версии)
            self.build_dependency_graph(dep_name, [])  # Пока без транзитивных зависимостей

    def generate_mermaid_graph(self):
        # Генерация текста графа в формате Mermaid
        lines = ["graph TD"]
        for pkg, deps in self.graph.items():
            for dep in deps:
                dep_name = dep.split('==')[0]
                lines.append(f"    {pkg} --> {dep_name}")
        return "\n".join(lines)

    def save_mermaid_graph(self, mermaid_graph, mermaid_file):
        # Создаем все промежуточные директории, если их не существует
        os.makedirs(os.path.dirname(mermaid_file), exist_ok=True)

        # Теперь можно записать граф в файл
        with open(mermaid_file, 'w') as f:
            f.write(mermaid_graph)

    def render_graph_to_png(self, mermaid_file):
        # Использование внешней программы для визуализации графа
        output_png = self.output_path + '.png'  # Указываем имя файла с расширением PNG
        subprocess.run([self.visualizer_path, "-i", mermaid_file, "-o", output_png])

    def visualize_dependencies(self):
        # Основной метод для визуализации зависимостей
        package_name = self.package_path.stem

        # Извлекаем зависимости из pip freeze
        initial_deps = self.parse_dependencies_from_pip()
        if not initial_deps:
            print("No dependencies found")

        self.build_dependency_graph(package_name, initial_deps)

        # Генерация Mermaid графа
        mermaid_graph = self.generate_mermaid_graph()

        # Используем абсолютный путь для сохранения файла
        mermaid_file = os.path.join(self.output_path, "dependency_graph.mmd")
        self.save_mermaid_graph(mermaid_graph, mermaid_file)

        # Генерация PNG файла с графом
        self.render_graph_to_png(mermaid_file)
        print("Graph generation completed successfully!")


# Запуск инструмента
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Visualize package dependencies as a graph.")
    parser.add_argument("config", help="Path to the JSON config file")
    args = parser.parse_args()

    visualizer = DependencyVisualizer(args.config)
    visualizer.visualize_dependencies()
