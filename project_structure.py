import ast
import fnmatch
from pathlib import Path
from typing import Dict, Set


class ProjectStructureGenerator:
    """A class for generating a markdown representation of a project's structure.

    with code analysis.
    """

    def __init__(self, root_path: str, output_file: str = "PROJECT_STRUCTURE.md"):
        """Initialize the ProjectStructureGenerator.

        Args:
        ----
            root_path: The root directory path of the project
            output_file: The output markdown file name
        """
        self.root_path = Path(root_path)
        self.output_file = output_file
        self.gitignore_patterns = self._read_gitignore()
        # Base patterns to always ignore
        self.base_ignore_patterns = {
            ".*",  # All hidden files and directories
            "__pycache__",
            "*.pyc",
            "*.pyo",
            "*.pyd",
            "*.so",
            "*.egg",
            "*.egg-info",
            "dist",
            "build",
            ".git",
            ".pytest_cache",
            ".mypy_cache",
            ".ruff_cache",
            "lightning_logs",
            "wandb",
            "outputs/",  # Explicitly ignore outputs directory
        }

    def _read_gitignore(self) -> Set[str]:
        """Read patterns from .gitignore file."""
        gitignore_path = self.root_path / ".gitignore"
        patterns = set()
        if gitignore_path.exists():
            with open(gitignore_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        # Handle directory patterns properly
                        if line.endswith("/"):
                            patterns.add(line)
                            patterns.add(line[:-1])  # Add without trailing slash too
                        else:
                            patterns.add(line)
                            patterns.add(f"{line}/")  # Add with trailing slash too
        return patterns

    def should_ignore(self, path: Path) -> bool:
        """Check if the path should be ignored based on gitignore and base patterns."""
        # Convert path to string for pattern matching
        path_str = str(path)

        # Get relative path from root
        try:
            rel_path = path.relative_to(self.root_path)
        except ValueError:
            rel_path = path

        rel_path_str = str(rel_path)

        # Check base ignore patterns
        for pattern in self.base_ignore_patterns:
            if fnmatch.fnmatch(path.name, pattern) or fnmatch.fnmatch(rel_path_str, pattern):
                return True

        # Check gitignore patterns
        for pattern in self.gitignore_patterns:
            # Handle both absolute and relative paths
            if fnmatch.fnmatch(path_str, pattern) or fnmatch.fnmatch(rel_path_str, pattern):
                return True
            # Handle directory matching
            if pattern.endswith("/") and (
                rel_path_str.startswith(pattern) or path_str.startswith(pattern)
            ):
                return True

        return False

    def parse_python_file(self, file_path: str) -> Dict:
        """Parse a Python file and extract classes and functions with their docstrings."""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                tree = ast.parse(file.read())

            classes = []
            functions = []

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    docstring = ast.get_docstring(node) or "No description"
                    classes.append({"name": node.name, "docstring": docstring.strip()})
                elif isinstance(node, ast.FunctionDef):
                    if not node.name.startswith("_"):  # Skip private functions
                        docstring = ast.get_docstring(node) or "No description"
                        functions.append({"name": node.name, "docstring": docstring.strip()})

            return {"classes": classes, "functions": functions}
        except Exception as e:
            return {"error": str(e)}

    def generate_structure(self) -> str:
        """Generate the project structure with code analysis."""
        output = ["# Project Structure\n\n"]

        def add_to_output(path: Path, prefix: str = "") -> None:
            """Recursively add directory contents to output with proper indentation."""
            if self.should_ignore(path):
                return

            if path.is_file():
                output.append(f"{prefix}📄 {path.name}\n")
                if path.suffix == ".py":
                    analysis = self.parse_python_file(str(path))
                    if analysis.get("classes"):
                        output.append(f"{prefix}    Classes:\n")
                        for cls in analysis["classes"]:
                            output.append(f"{prefix}     • {cls['name']}\n")
                            if cls["docstring"]:
                                docstring_lines = cls["docstring"].strip().split("\n")
                                for line in docstring_lines:
                                    if not line.strip():
                                        output.append(f"{prefix}      \n")
                                    else:
                                        output.append(f"{prefix}      {line.strip()}\n")
                                output.append("\n")
                    if analysis.get("functions"):
                        output.append(f"{prefix}    Functions:\n")
                        for func in analysis["functions"]:
                            output.append(f"{prefix}     • {func['name']}\n")
                            if func["docstring"]:
                                docstring_lines = func["docstring"].strip().split("\n")
                                for line in docstring_lines:
                                    if not line.strip():
                                        output.append(f"{prefix}      \n")
                                    else:
                                        output.append(f"{prefix}      {line.strip()}\n")
                                output.append("\n")
            else:
                output.append(f"{prefix}📁 {path.name}/\n")
                # Sort directories first, then files
                items = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
                next_prefix = prefix + "  "
                for item in items:
                    if not self.should_ignore(item):
                        add_to_output(item, next_prefix)

        # Start from root
        output.append("## Directory Structure and Code Analysis\n\n")
        output.append("📁 Project Root\n")
        items = sorted(self.root_path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
        for item in items:
            if not self.should_ignore(item):
                add_to_output(item, "  ")

        return "".join(output)

    def save_structure(self) -> None:
        """Generate and save the project structure to a markdown file."""
        structure = self.generate_structure()
        output_path = self.root_path / self.output_file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(structure)
        print(f"Project structure has been saved to {output_path}")


if __name__ == "__main__":
    generator = ProjectStructureGenerator(".")
    generator.save_structure()
