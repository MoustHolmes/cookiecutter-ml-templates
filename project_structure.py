import ast
import fnmatch
from pathlib import Path
from typing import Any


class ProjectStructureGenerator:
    """A class for generating a markdown representation of a project's structure.

    with code analysis.
    """

    def __init__(self: "ProjectStructureGenerator", root_path: str, output_file: str = "PROJECT_STRUCTURE.md") -> None:
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

    def _read_gitignore(self: "ProjectStructureGenerator") -> set[str]:
        """Read patterns from .gitignore file."""
        gitignore_path = self.root_path / ".gitignore"
        patterns: set[str] = set()
        if gitignore_path.exists():
            with gitignore_path.open() as f:
                for git_line in f:
                    clean_line = git_line.strip()
                    if clean_line and not clean_line.startswith("#"):
                        # Handle directory patterns properly
                        if clean_line.endswith("/"):
                            patterns.add(clean_line)
                            patterns.add(clean_line[:-1])  # Add without trailing slash too
                        else:
                            patterns.add(clean_line)
                            patterns.add(f"{clean_line}/")  # Add with trailing slash too
        return patterns

    def should_ignore(self: "ProjectStructureGenerator", path: Path) -> bool:
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
            if pattern.endswith("/") and (rel_path_str.startswith(pattern) or path_str.startswith(pattern)):
                return True

        return False

    def parse_python_file(self: "ProjectStructureGenerator", file_path: str) -> dict[str, Any]:
        """Parse a Python file and extract classes and functions with their docstrings."""
        try:
            with Path(file_path).open(encoding="utf-8") as file:
                tree = ast.parse(file.read())
        except (SyntaxError, UnicodeDecodeError, PermissionError, FileNotFoundError) as e:
            return {"error": f"Error parsing Python file: {e!s}"}
        else:
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

    def _process_python_file(self: "ProjectStructureGenerator", path: Path, prefix: str, output: list[str]) -> None:
        """Process a Python file and append its analysis to the output."""
        analysis = self.parse_python_file(str(path))

        if analysis.get("classes"):
            output.append(f"{prefix}    Classes:\n")
            for cls in analysis["classes"]:
                output.append(f"{prefix}     • {cls['name']}\n")
                self._append_docstring(cls["docstring"], prefix, output)

        if analysis.get("functions"):
            output.append(f"{prefix}    Functions:\n")
            for func in analysis["functions"]:
                output.append(f"{prefix}     • {func['name']}\n")
                self._append_docstring(func["docstring"], prefix, output)

    def _append_docstring(
        self: "ProjectStructureGenerator",
        docstring: str,
        prefix: str,
        output: list[str],
    ) -> None:
        """Append a formatted docstring to the output list."""
        if docstring:
            docstring_lines = docstring.strip().split("\n")
            for line in docstring_lines:
                if not line.strip():
                    output.append(f"{prefix}      \n")
                else:
                    output.append(f"{prefix}      {line.strip()}\n")
            output.append("\n")

    def _process_directory(
        self: "ProjectStructureGenerator",
        path: Path,
        prefix: str,
        output: list[str],
    ) -> None:
        """Process a directory and append its contents to the output."""
        output.append(f"{prefix}📁 {path.name}/\n")
        # Sort directories first, then files
        items = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
        next_prefix = prefix + "  "
        for item in items:
            if not self.should_ignore(item):
                self._add_to_output(item, next_prefix, output)

    def _add_to_output(
        self: "ProjectStructureGenerator",
        path: Path,
        prefix: str,
        output: list[str],
    ) -> None:
        """Add a file or directory to the output with proper formatting."""
        if self.should_ignore(path):
            return

        if path.is_file():
            output.append(f"{prefix}📄 {path.name}\n")
            if path.suffix == ".py":
                self._process_python_file(path, prefix, output)
        else:
            self._process_directory(path, prefix, output)

    def generate_structure(self: "ProjectStructureGenerator") -> str:
        """Generate the project structure with code analysis."""
        output: list[str] = ["# Project Structure\n\n"]

        # Start from root
        output.append("## Directory Structure and Code Analysis\n\n")
        output.append("📁 Project Root\n")

        items = sorted(self.root_path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
        for item in items:
            if not self.should_ignore(item):
                self._add_to_output(item, "  ", output)

        return "".join(output)

    def save_structure(self: "ProjectStructureGenerator") -> None:
        """Generate and save the project structure to a markdown file."""
        structure = self.generate_structure()
        output_path = self.root_path / self.output_file
        with output_path.open("w", encoding="utf-8") as f:
            f.write(structure)
        print(f"Project structure has been saved to {output_path}")


if __name__ == "__main__":
    generator = ProjectStructureGenerator(".")
    generator.save_structure()
