from invoke import task

@task
def test(c):
    """Run tests"""
    c.run("pytest tests/")

@task
def setup(c):
    """Setup development environment"""
    c.run("pip install -r requirements.txt")
    c.run("pre-commit install")

@task
def create_template(c, template="barebone", output_dir="."):
    """Create a new project from template"""
    c.run(f"cookiecutter templates/{template} --output-dir {output_dir}")
