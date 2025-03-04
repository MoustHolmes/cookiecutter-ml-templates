import os
import pytest
from cookiecutter.main import cookiecutter
from cookiecutter.exceptions import FailedHookException

@pytest.fixture
def temp_dir(tmp_path):
    return tmp_path

def test_barebone_template_success(temp_dir):
    output_dir = temp_dir / "barebone_test"
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.normpath(os.path.join(current_dir, "..", "templates", "barebone"))
    
    # Generate project
    cookiecutter(
        template=template_dir,
        output_dir=str(output_dir),
        no_input=True,
        extra_context={
            "project_name": "test_project",
            "author_name": "Test Author",
            "description": "Test Description",
            "python_version": "3.10"
        }
    )
    
    # Check if critical files exist
    generated_dir = output_dir / "test_project"
    assert generated_dir.exists()
    assert (generated_dir / "README.md").exists()

def test_project_name_with_number_prefix(temp_dir):
    output_dir = temp_dir / "invalid_test"
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.normpath(os.path.join(current_dir, "..", "templates", "barebone"))
    
    with pytest.raises(FailedHookException):
        cookiecutter(
            template=template_dir,
            output_dir=str(output_dir),
            no_input=True,
            extra_context={
                "project_name": "1test_project",
                "author_name": "Test Author",
                "description": "Test Description",
                "python_version": "3.10"
            }
        )

def test_project_name_with_spaces(temp_dir):
    output_dir = temp_dir / "invalid_test"
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.normpath(os.path.join(current_dir, "..", "templates", "barebone"))
    
    with pytest.raises(FailedHookException):
        cookiecutter(
            template=template_dir,
            output_dir=str(output_dir),
            no_input=True,
            extra_context={
                "project_name": "Test Project",
                "author_name": "Test Author",
                "description": "Test Description",
                "python_version": "3.10"
            }
        )

def test_project_name_with_special_chars(temp_dir):
    output_dir = temp_dir / "invalid_test"
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.normpath(os.path.join(current_dir, "..", "templates", "barebone"))
    
    with pytest.raises(FailedHookException):
        cookiecutter(
            template=template_dir,
            output_dir=str(output_dir),
            no_input=True,
            extra_context={
                "project_name": "test-project!",
                "author_name": "Test Author",
                "description": "Test Description",
                "python_version": "3.10"
            }
        )

def test_invalid_python_version(temp_dir):
    output_dir = temp_dir / "invalid_test"
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.normpath(os.path.join(current_dir, "..", "templates", "barebone"))
    
    with pytest.raises(FailedHookException):
        cookiecutter(
            template=template_dir,
            output_dir=str(output_dir),
            no_input=True,
            extra_context={
                "project_name": "test_project",
                "author_name": "Test Author",
                "description": "Test Description",
                "python_version": "3.9"
            }
        )

def test_classification_template_success(temp_dir):
    output_dir = temp_dir / "classification_test"
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.normpath(os.path.join(current_dir, "..", "templates", "classification"))
    
    # Generate project
    cookiecutter(
        template=template_dir,
        output_dir=str(output_dir),
        no_input=True,
        extra_context={
            "project_name": "test_classification",
            "author_name": "Test Author",
            "description": "Test Description",
            "python_version": "3.10"
        }
    )
    
    # Check if critical files and directories exist
    generated_dir = output_dir / "test_classification"
    assert generated_dir.exists()
    assert (generated_dir / "src").exists()
    assert (generated_dir / "tests").exists()
    assert (generated_dir / "configs").exists()
    assert (generated_dir / "data").exists()


