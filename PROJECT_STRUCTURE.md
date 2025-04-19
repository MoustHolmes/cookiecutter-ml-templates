# Project Structure

## Directory Structure and Code Analysis

📁 Project Root
  📁 hooks/
    📄 post_gen_project.py
  📁 templates/
    📁 barebone/
      📁 hooks/
        📄 post_gen_project.py
      📁 {{cookiecutter.repo_name}}/
        📁 configs/
          📁 callbacks/
            📄 default_callbacks.yaml
          📁 data/
          📁 experiments/
          📁 logger/
            📄 wandb_logger.yaml
          📁 model/
          📁 trainer/
            📄 default_trainer.yaml
          📄 train_config.yaml
        📁 data/
          📁 processed/
          📁 raw/
        📁 docs/
          📁 source/
            📄 index.md
          📄 mkdocs.yaml
        📁 notebooks/
        📁 reports/
          📁 figures/
        📁 src/
          📁 {{cookiecutter.project_name}}/
            📁 callbacks/
            📁 data/
              📄 barebone_datamodule.py
            📁 model/
              📄 barebones_lightningmodule.py
            📄 __init__.py
            📄 barebones_datamodule.py
                Classes:
                 • BarebonesDataModule
                  No description

                Functions:
                 • prepare_data
                  Download data if needed. This method is called only from a single process.

                 • setup
                  Load data. Set variables: `self.data_train`, `self.data_val`, `self.data_test`.

                 • train_dataloader
                  No description

                 • val_dataloader
                  No description

                 • test_dataloader
                  No description

            📄 barebones_lightningmodule.py
                Classes:
                 • BarebonesLightningModule
                  No description

                Functions:
                 • forward
                  Forward pass of the model.
                  
                  Args:
                  x: Input tensor of shape (batch_size, 28, 28)
                  
                  Returns:
                  torch.Tensor: Output tensor of shape (batch_size, 10)

                 • training_step
                  No description

                 • validation_step
                  No description

                 • test_step
                  No description

                 • configure_optimizers
                  No description

            📄 train.py
                Functions:
                 • train
                  No description

        📁 tests/
          📄 __init__.py
          📄 test_data.py
          📄 test_model.py
        📄 LICENSE
        📄 pyproject.toml
        📄 README.md
        📄 requirements.txt
        📄 requirements_dev.txt
        📄 tasks.py
            Functions:
             • create_environment
              Create a new conda environment for project.

             • requirements
              Install project requirements.

             • dev_requirements
              Install development requirements.

             • preprocess_data
              Preprocess data.

             • train
              Train model.

             • test
              Run tests.

             • build_docs
              Build documentation.

             • serve_docs
              Serve documentation.

      📄 cookiecutter.json
    📁 classification/
      📁 hooks/
        📄 post_gen_project.py
      📁 {{cookiecutter.repo_name}}/
        📁 configs/
        📁 data/
        📁 src/
          📁 models/
        📁 tests/
          📄 __init__.py
        📄 pyproject.toml
        📄 README.md
      📄 cookiecutter.json
    📁 MNIST_wandb_image_logger/
      📁 hooks/
        📄 post_gen_project.py
      📁 {{cookiecutter.repo_name}}/
        📁 configs/
          📁 callbacks/
            📄 default_callbacks.yaml
          📁 data/
            📄 default_data_module.yaml
          📁 experiments/
            📄 debug.yaml
          📁 logger/
            📄 wandb_logger.yaml
          📁 model/
            📄 default_model.yaml
          📁 trainer/
            📄 default_trainer.yaml
          📄 paths_config.yaml
          📄 train_config.yaml
        📁 data/
          📁 MNIST/
            📁 raw/
          📁 processed/
          📁 raw/
        📁 docs/
          📁 source/
            📄 index.md
          📄 mkdocs.yaml
        📁 logs/
        📁 notebooks/
        📁 outputs/
        📁 reports/
          📁 figures/
        📁 src/
          📁 {{cookiecutter.project_name}}/
            📁 callbacks/
              📄 __init__.py
              📄 image_logger.py
                  Classes:
                   • ImageLoggerCallback
                    No description

                  Functions:
                   • denormalize
                    Denormalize images from [-mean/std, (1-mean)/std] back to [0, 1].

                   • on_train_batch_end
                    Log images to WandB on train batch end.

            📁 data/
              📄 barebone_datamodule.py
            📁 model/
              📄 barebones_lightningmodule.py
            📄 __init__.py
            📄 barebones_datamodule.py
                Classes:
                 • BarebonesDataModule
                  No description

                Functions:
                 • prepare_data
                  Download data if needed. This method is called only from a single process.

                 • setup
                  Load data. Set variables: `self.data_train`, `self.data_val`, `self.data_test`.

                 • train_dataloader
                  No description

                 • val_dataloader
                  No description

                 • test_dataloader
                  No description

            📄 barebones_lightningmodule.py
                Classes:
                 • BarebonesLightningModule
                  No description

                Functions:
                 • forward
                  Forward pass of the model.
                  
                  Args:
                  x: Input tensor of shape (batch_size, 28, 28)
                  
                  Returns:
                  torch.Tensor: Output tensor of shape (batch_size, 10)

                 • training_step
                  No description

                 • validation_step
                  No description

                 • test_step
                  No description

                 • configure_optimizers
                  No description

            📄 train.py
                Functions:
                 • train
                  No description

        📁 tests/
          📄 __init__.py
          📄 test_data.py
              Functions:
               • data_dir
                No description

               • datamodule
                No description

               • test_datamodule_attributes
                Test if the datamodule has the correct attributes.

               • test_prepare_data
                Test prepare_data creates the required files.

               • test_setup
                Test setup creates the correct splits.

               • test_train_dataloader
                Test if train_dataloader returns the correct type and batch size.

               • test_val_dataloader
                Test if val_dataloader returns the correct type and batch size.

               • test_test_dataloader
                Test if test_dataloader returns the correct type and batch size.

          📄 test_model.py
              Functions:
               • model
                No description

               • test_model_init
                Test if the model initializes correctly.

               • test_model_forward
                Test the forward pass of the model.

               • test_model_training_step
                Test the training step of the model.

               • test_model_validation_step
                Test the validation step of the model.

               • test_model_test_step
                Test the test step of the model.

               • test_configure_optimizers
                Test if the model configures optimizer correctly.

        📄 LICENSE
        📄 pyproject.toml
        📄 README.md
        📄 requirements.txt
        📄 requirements_dev.txt
        📄 tasks.py
            Functions:
             • create_environment
              Create a new conda environment for project.

             • requirements
              Install project requirements.

             • dev_requirements
              Install development requirements.

             • preprocess_data
              Preprocess data.

             • train
              Train model.

             • test
              Run tests.

             • build_docs
              Build documentation.

             • serve_docs
              Serve documentation.

             • test_debug
              Run training with debug configuration for quick testing.

      📄 cookiecutter.json
  📁 tests/
    📄 test_create_project.py
        Functions:
         • temp_dir
          Provide a temporary directory for tests.
          
          Args:
          tmp_path: pytest fixture providing temporary directory
          
          Returns:
          Path to temporary directory

         • test_barebone_template_success
          Test successful generation of barebone template.
          
          Args:
          temp_dir: temporary directory for test

         • test_project_name_with_number_prefix
          Test that project name cannot start with a number.
          
          Args:
          temp_dir: temporary directory for test

         • test_project_name_with_spaces
          Test that project name cannot contain spaces.
          
          Args:
          temp_dir: temporary directory for test

         • test_project_name_with_special_chars
          Test that project name cannot contain special characters.
          
          Args:
          temp_dir: temporary directory for test

         • test_invalid_python_version
          Test that invalid Python version is rejected.
          
          Args:
          temp_dir: temporary directory for test

         • test_classification_template_success
          Test successful generation of classification template.
          
          Args:
          temp_dir: temporary directory for test

         • test_project_structure
          Test that generated project has correct structure.
          
          Args:
          temp_dir: temporary directory for test

  📄 project_structure.py
      Classes:
       • ProjectStructureGenerator
        A class for generating a markdown representation of a project's structure.
        
        with code analysis.

      Functions:
       • should_ignore
        Check if the path should be ignored based on gitignore and base patterns.

       • parse_python_file
        Parse a Python file and extract classes and functions with their docstrings.

       • generate_structure
        Generate the project structure with code analysis.

       • save_structure
        Generate and save the project structure to a markdown file.

       • add_to_output
        Recursively add directory contents to output with proper indentation.

  📄 pyproject.toml
  📄 README.md
  📄 requirements.txt
  📄 tasks.py
      Functions:
       • test
        Run tests.

       • setup
        Set up the development environment.

       • create_template
        Create a new project from a template.

