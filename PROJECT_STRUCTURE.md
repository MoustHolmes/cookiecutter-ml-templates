# Project Structure

## Directory Structure and Code Analysis

📁 Project Root
  📁 docs/
    📁 available-templates/
      📄 barebone.md
      📄 classification.md
      📄 flow-matching.md
      📄 mnist-wandb.md
      📄 overview.md
    📁 development/
      📄 contributing.md
      📄 creating-templates.md
      📄 testing-templates.md
    📁 getting-started/
      📄 first-project.md
      📄 installation.md
      📄 quickstart.md
    📁 guides/
      📄 dependency-management.md
      📄 github-integration.md
      📄 hydra-config.md
      📄 project-structure.md
      📄 testing.md
    📁 reference/
      📄 best-practices.md
      📄 faq.md
      📄 template-options.md
    📄 index.md
  📁 hooks/
    📄 post_gen_project.py
  📁 site/
    📁 assets/
      📁 images/
        📄 favicon.png
      📁 javascripts/
        📁 lunr/
          📁 min/
            📄 lunr.ar.min.js
            📄 lunr.da.min.js
            📄 lunr.de.min.js
            📄 lunr.du.min.js
            📄 lunr.el.min.js
            📄 lunr.es.min.js
            📄 lunr.fi.min.js
            📄 lunr.fr.min.js
            📄 lunr.he.min.js
            📄 lunr.hi.min.js
            📄 lunr.hu.min.js
            📄 lunr.hy.min.js
            📄 lunr.it.min.js
            📄 lunr.ja.min.js
            📄 lunr.jp.min.js
            📄 lunr.kn.min.js
            📄 lunr.ko.min.js
            📄 lunr.multi.min.js
            📄 lunr.nl.min.js
            📄 lunr.no.min.js
            📄 lunr.pt.min.js
            📄 lunr.ro.min.js
            📄 lunr.ru.min.js
            📄 lunr.sa.min.js
            📄 lunr.stemmer.support.min.js
            📄 lunr.sv.min.js
            📄 lunr.ta.min.js
            📄 lunr.te.min.js
            📄 lunr.th.min.js
            📄 lunr.tr.min.js
            📄 lunr.vi.min.js
            📄 lunr.zh.min.js
          📄 tinyseg.js
          📄 wordcut.js
        📁 workers/
          📄 search.973d3a69.min.js
          📄 search.973d3a69.min.js.map
        📄 bundle.f55a23d4.min.js
        📄 bundle.f55a23d4.min.js.map
      📁 stylesheets/
        📄 main.e53b48f4.min.css
        📄 main.e53b48f4.min.css.map
        📄 palette.06af60db.min.css
        📄 palette.06af60db.min.css.map
    📁 development/
      📁 contributing/
        📄 index.html
      📁 creating-templates/
        📄 index.html
      📁 testing-templates/
        📄 index.html
    📁 getting-started/
      📁 first-project/
        📄 index.html
      📁 installation/
        📄 index.html
      📁 quickstart/
        📄 index.html
    📁 guides/
      📁 dependency-management/
        📄 index.html
      📁 hydra-config/
        📄 index.html
      📁 project-structure/
        📄 index.html
      📁 testing/
        📄 index.html
    📁 reference/
      📁 best-practices/
        📄 index.html
      📁 faq/
        📄 index.html
      📁 template-options/
        📄 index.html
    📁 search/
      📄 search_index.json
    📄 404.html
    📄 index.html
    📄 sitemap.xml
    📄 sitemap.xml.gz
  📁 templates/
    📁 barebone/
      📁 hooks/
        📄 post_gen_project.py
            Functions:
             • create_github_repository
              Create a GitHub repository using GitHub CLI.

      📁 {{cookiecutter.repo_name}}/
        📁 configs/
          📁 callbacks/
            📄 default_callbacks.yaml
          📁 data/
            📄 default_data_module.yaml
          📁 experiment/
          📁 logger/
            📄 wandb_logger.yaml
          📁 model/
            📄 default_model.yaml
          📁 trainer/
            📄 default_trainer.yaml
          📄 paths_config.yaml
          📄 train_config.yaml
        📁 data/
          📁 processed/
          📁 raw/
          📄 README.md
        📁 docs/
          📁 source/
            📄 index.md
          📄 mkdocs.yaml
        📁 notebooks/
        📁 reports/
          📁 figures/
        📁 src/
          📁 {{cookiecutter.repo_name}}/
            📁 callbacks/
            📁 data/
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

            📁 models/
              📄 __init__.py
            📄 __init__.py
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
          📄 conftest.py
              Functions:
               • cfg_train
                A pytest fixture for loading the training configuration.
                
                Returns:
                A DictConfig containing a valid training configuration.

               • cfg_train_debug
                A pytest fixture for loading the training configuration with debug overrides.
                
                Returns:
                A DictConfig containing a valid training configuration for debugging.

          📄 test_config.py
              Functions:
               • test_train_config
                Tests the training configuration provided by the `cfg_train` pytest fixture.
                
                :param cfg_train: A DictConfig containing a valid training configuration.

               • test_config_has_required_fields
                Tests that the configuration has all required fields.
                
                :param cfg_train: A DictConfig containing a valid training configuration.

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

        📄 tasks_pip.py
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

        📄 tasks_uv.py
            Functions:
             • create_environment
              Create a new uv environment for project.

             • requirements
              Install project requirements using uv.

             • dev_requirements
              Install development requirements using uv.

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
          📁 {{cookiecutter.repo_name}}/
            📁 models/
            📄 __init__.py
        📁 tests/
          📄 __init__.py
        📄 pyproject.toml
        📄 README.md
        📄 requirements.txt
        📄 requirements_dev.txt
        📄 tasks_pip.py
            Functions:
             • create_environment
              Create a new conda environment for project.

             • requirements
              Install project requirements.

             • dev_requirements
              Install development requirements.

             • train
              Train model.

             • test
              Run tests.

        📄 tasks_uv.py
            Functions:
             • create_environment
              Create a new environment for project.

             • requirements
              Install project requirements.

             • dev_requirements
              Install development requirements.

             • train
              Train model.

             • test
              Run tests.

      📄 cookiecutter.json
    📁 flow_matching/
      📁 hooks/
        📄 post_gen_project.py
            Functions:
             • remove_file
              Remove a file.

             • create_github_repository
              Create a GitHub repository using GitHub CLI.

             • main
              Execute the post-generation tasks.

      📁 {{cookiecutter.repo_name}}/
        📁 configs/
          📁 callbacks/
            📄 default_callbacks.yaml
          📁 data/
            📄 default_data_module.yaml
            📄 moons_data_module.yaml
          📁 experiment/
            📄 debug.yaml
            📄 moons.yaml
          📁 logger/
            📄 wandb_logger.yaml
          📁 model/
            📄 default_model.yaml
            📄 latent_flow.yaml
            📄 moons_model.yaml
            📄 vae.yaml
          📁 trainer/
            📄 default_trainer.yaml
          📄 paths_config.yaml
          📄 train_config.yaml
        📁 data/
          📁 MNIST/
            📁 raw/
              📄 t10k-images-idx3-ubyte
              📄 t10k-images-idx3-ubyte.gz
              📄 t10k-labels-idx1-ubyte
              📄 t10k-labels-idx1-ubyte.gz
              📄 train-images-idx3-ubyte
              📄 train-images-idx3-ubyte.gz
              📄 train-labels-idx1-ubyte
              📄 train-labels-idx1-ubyte.gz
          📄 README.md
        📁 docs/
          📁 source/
            📄 index.md
          📄 mkdocs.yaml
        📁 notebooks/
          📄 train.ipynb
        📁 reports/
        📁 src/
          📁 {{cookiecutter.repo_name}}/
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
              📄 __init__.py
              📄 barebone_datamodule.py
              📄 MNIST_datamodule.py
                  Classes:
                   • MNISTDataModule
                    No description

                  Functions:
                   • prepare_data
                    No description

                   • setup
                    No description

                   • train_dataloader
                    No description

                   • val_dataloader
                    No description

                   • test_dataloader
                    No description

              📄 moons_datamodule.py
                  Classes:
                   • MoonsDataModule
                    No description

                  Functions:
                   • prepare_data
                    No description

                   • setup
                    Generates and splits the dataset. Called on every GPU.

                   • train_dataloader
                    No description

                   • val_dataloader
                    No description

                   • test_dataloader
                    No description

            📁 models/
              📄 __init__.py
              📄 mlp.py
              📄 unet.py
                  Classes:
                   • FourierEncoder
                    Based on https://github.com/lucidrains/denoising-diffusion-pytorch/blob/main/denoising_diffusion_pytorch/karras_unet.py#L183

                   • ResidualBlock
                    Basic residual block with time and class conditioning.

                   • UNet
                    Simplified U-Net architecture for conditional vector field/score estimation.

                  Functions:
                   • forward
                    Args:
                    - t: (bs, 1, 1, 1) or (bs,)
                    Returns:
                    - embeddings: (bs, dim)

                   • forward
                    No description

                   • forward
                    No description

            📁 modules/
              📄 __init__.py
              📄 samplers.py
                  Classes:
                   • GaussianSampler
                    Samples from a standard Gaussian distribution N(0, I).

                   • UniformSampler
                    Samples from a uniform distribution U(-1, 1).

                  Functions:
                   • forward
                    Generates samples.
                    
                    Args:
                    num_samples (int): The number of samples to generate (batch size).
                    device (torch.device): The device to place the samples on.
                    
                    Returns:
                    torch.Tensor: A tensor of random samples.

                   • forward
                    Generates samples.
                    
                    Args:
                    num_samples (int): The number of samples to generate (batch size).
                    device (torch.device): The device to place the samples on.
                    
                    Returns:
                    torch.Tensor: A tensor of random samples.

              📄 schedulers.py
                  Classes:
                   • LinearScheduler
                    Linear scheduler where alpha_t = t.

                   • CosineScheduler
                    Cosine scheduler often used in diffusion models.

                  Functions:
                   • forward
                    No description

                   • forward
                    No description

              📄 solvers.py
                  Classes:
                   • EulerSolver
                    A simple first-order Euler method ODE solver.

                   • RK4Solver
                    Fourth-order Runge-Kutta (RK4) ODE solver.

                  Functions:
                   • solve
                    Solves the ODE from t=0 to t=1.
                    
                    Args:
                    model (nn.Module): The model predicting the vector field.
                    x0 (torch.Tensor): The initial condition at t=0 (e.g., noise).
                    labels (torch.Tensor): The conditional labels.
                    steps (int): The number of discretization steps.
                    
                    Returns:
                    torch.Tensor: The solution at t=1.

                   • solve
                    Solves the ODE from t=0 to t=1 using the RK4 method.
                    
                    Args:
                    model (nn.Module): The model predicting the vector field.
                    x0 (torch.Tensor): The initial condition at t=0 (e.g., noise).
                    labels (torch.Tensor): The conditional labels.
                    steps (int): The number of discretization steps.
                    
                    Returns:
                    torch.Tensor: The solution at t=1.

            📁 util/
              📄 __init__.py
              📄 plot_imgs.py
                  Functions:
                   • show_imgs
                    No description

            📄 __init__.py
            📄 flow_matching_module.py
            📄 train.py
                Functions:
                 • train
                  No description

            📄 vae_module.py
                Classes:
                 • SpatialEncoder
                  No description

                 • SpatialDecoder
                  No description

                 • SpatialVAE
                  No description

                Functions:
                 • forward
                  No description

                 • forward
                  No description

                 • forward
                  No description

                 • reparameterize
                  No description

                 • model_step
                  No description

                 • training_step
                  No description

                 • validation_step
                  No description

                 • test_step
                  No description

                 • configure_optimizers
                  No description

                 • calculate_latent_stats
                  mimics Wan2.2 scale calculation

        📁 tests/
          📄 __init__.py
          📄 conftest.py
              Functions:
               • cfg_train
                A pytest fixture for loading the training configuration.
                
                Returns:
                A DictConfig containing a valid training configuration.

               • cfg_train_debug
                A pytest fixture for loading the training configuration with debug overrides.
                
                Returns:
                A DictConfig containing a valid training configuration for debugging.

          📄 test_config.py
              Functions:
               • test_train_config
                Tests the training configuration provided by the `cfg_train` pytest fixture.
                
                :param cfg_train: A DictConfig containing a valid training configuration.

               • test_train_config_debug
                Tests the training configuration with debug overrides.
                
                :param cfg_train_debug: A DictConfig containing a valid debug training configuration.

               • test_config_has_required_fields
                Tests that the configuration has all required fields.
                
                :param cfg_train: A DictConfig containing a valid training configuration.

               • test_config_overrides
                Tests that configuration values are properly set.
                
                :param cfg_train: A DictConfig containing a valid training configuration.

               • test_model_components
                Tests that model configuration has all required components.
                
                :param cfg_train: A DictConfig containing a valid training configuration.

               • test_instantiate_all_components
                Tests that all configuration components can be instantiated without errors.
                
                :param cfg_train: A DictConfig containing a valid training configuration.

               • test_train_with_fast_dev_run
                Tests that training runs successfully with fast_dev_run enabled.
                
                This test performs a complete training run with the debug configuration,
                which includes fast_dev_run=True to run only 1 batch through train/val/test.
                
                :param cfg_train_debug: A DictConfig containing the debug training configuration.

          📄 test_data.py
          📄 test_model.py
          📄 test_train_script.py
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

        📄 tasks_pip.py
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

        📄 tasks_uv.py
            Functions:
             • create_environment
              Create a new environment for project.

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
      📄 TEMPLATE_SUMMARY.md
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
          📁 {{cookiecutter.repo_name}}/
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

            📁 models/
              📄 __init__.py
            📄 __init__.py
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

             • test_debug
              Run training with debug configuration for quick testing.

        📄 tasks_pip.py
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

        📄 tasks_uv.py
            Functions:
             • create_environment
              Create a new environment for project.

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
    📁 rl/
      📁 hooks/
        📄 post_gen_project.py
            Functions:
             • create_github_repository
              Create a GitHub repository using GitHub CLI.

             • main
              Execute the post-generation tasks.

      📁 {{cookiecutter.repo_name}}/
        📁 configs/
          📁 agent/
            📄 dqn.yaml
            📄 ppo_continuous.yaml
            📄 ppo_discrete.yaml
            📄 rpo.yaml
            📄 sac.yaml
            📄 td3.yaml
          📁 callbacks/
            📄 default_callbacks.yaml
          📁 environment/
            📄 cartpole.yaml
            📄 cartpole_replay.yaml
            📄 lunar_lander.yaml
            📄 lunar_lander_ppo.yaml
            📄 pendulum.yaml
            📄 pendulum_ppo.yaml
          📁 experiment/
            📄 debug.yaml
            📄 dqn_cartpole.yaml
            📄 dqn_debug.yaml
            📄 lunar_lander.yaml
            📄 ppo_cartpole.yaml
            📄 ppo_debug.yaml
            📄 ppo_lunar_lander.yaml
            📄 ppo_pendulum.yaml
            📄 rpo_lunar_lander.yaml
            📄 rpo_pendulum.yaml
            📄 sac_lunar_lander.yaml
            📄 sac_pendulum.yaml
            📄 td3_lunar_lander.yaml
            📄 td3_pendulum.yaml
          📁 logger/
            📄 wandb_logger.yaml
          📁 trainer/
            📄 default_trainer.yaml
          📄 paths_config.yaml
          📄 train_config.yaml
        📁 data/
          📄 README.md
        📁 docs/
          📁 source/
            📄 index.md
          📄 mkdocs.yaml
        📁 src/
          📁 {{cookiecutter.repo_name}}/
            📁 callbacks/
              📄 __init__.py
              📄 episode_logger.py
                  Classes:
                   • EpisodeLoggerCallback
                    Periodically evaluates the agent with greedy rollouts and logs metrics.
                    
                    At the end of every ``log_every_n_epochs`` training epochs the callback:
                    
                    1. Runs ``eval_episodes`` deterministic episodes in the datamodule's
                    environment using the actor's greedy (mean) action.
                    2. Logs ``eval/mean_episode_reward`` and ``eval/mean_episode_length``
                    to the trainer logger.
                    
                    Args:
                    eval_episodes: Number of greedy episodes to run per evaluation.
                    log_every_n_epochs: How often (in Lightning epochs) to run evaluation.

                  Functions:
                   • on_train_epoch_end
                    Run evaluation rollouts and log results.
                    
                    Args:
                    trainer: The active Lightning trainer.
                    pl_module: The agent LightningModule (SACModule or TD3Module).

              📄 video_logger.py
                  Classes:
                   • VideoLoggerCallback
                    Renders a greedy episode and logs it as a WandB video.
                    
                    At the end of every ``log_every_n_epochs`` training epochs the callback:
                    
                    1. Creates a *separate* ``RecordVideo``-wrapped environment so the
                    training environment is never disturbed.
                    2. Runs one deterministic episode using the agent's greedy policy.
                    3. Passes the recorded mp4 file to ``wandb.Video`` for upload.
                    
                    Args:
                    log_every_n_epochs: How often (in Lightning epochs) to record a video.
                    fps: Frame-rate for the uploaded video.
                    max_episode_steps: Hard cap on episode length to avoid runaway rollouts.
                    ``None`` uses the environment's own time limit.

                  Functions:
                   • on_train_epoch_end
                    Render and log a video episode.
                    
                    Args:
                    trainer: The active Lightning trainer.
                    pl_module: The agent LightningModule (SACModule or TD3Module).

            📁 data/
              📄 __init__.py
              📄 env_datamodule.py
              📄 replay_buffer.py
                  Classes:
                   • Batch
                    A mini-batch of transitions sampled from the replay buffer.
                    
                    All tensors are float32 with shapes:
                    
                    - ``obs``:      ``(B, obs_dim)``
                    - ``action``:   ``(B, action_dim)``
                    - ``reward``:   ``(B,)``
                    - ``next_obs``: ``(B, obs_dim)``
                    - ``done``:     ``(B,)``  — 1.0 only on genuine termination, 0.0 on truncation

                   • ReplayBuffer
                    Fixed-capacity circular experience replay buffer.
                    
                    Transitions are stored as numpy arrays (CPU). Sampling returns a
                    :class:`Batch` of float32 ``torch.Tensor`` objects on CPU; move to the
                    correct device inside the training loop.
                    
                    Args:
                    obs_dim: Dimensionality of the observation space.
                    action_dim: Dimensionality of the action space.
                    buffer_size: Maximum number of transitions to store.

                  Functions:
                   • add
                    Store a single transition.
                    
                    ``truncated`` is accepted for API compatibility with the Gymnasium step
                    return, but it is intentionally ignored: only genuine ``terminated``
                    episodes set ``done=1``. This preserves correct value-function
                    bootstrapping for time-limited environments.
                    
                    Args:
                    obs: Current observation.
                    action: Action taken.
                    reward: Immediate reward received.
                    next_obs: Observation after taking the action.
                    terminated: True if the episode ended due to a terminal state.
                    truncated: True if the episode ended due to a time limit (ignored).

                   • sample
                    Sample a uniformly random mini-batch of transitions.
                    
                    Args:
                    batch_size: Number of transitions to sample.
                    
                    Returns:
                    A :class:`Batch` of float32 tensors on CPU.
                    
                    Raises:
                    ValueError: If the buffer contains fewer transitions than ``batch_size``.

              📄 rollout_datamodule.py
                  Classes:
                   • RolloutDataModule
                    Vectorized environment datamodule for on-policy algorithms (PPO/RPO).
                    
                    Creates a ``SyncVectorEnv`` with ``num_envs`` parallel environments.
                    Exposes ``obs_shape``, ``act_shape``, and ``is_continuous`` so
                    ``PPOModule.setup()`` can pre-allocate rollout buffers.
                    
                    The train dataloader returns a single dummy item per epoch — one call to
                    ``training_step`` owns the complete PPO rollout + update round.
                    
                    Args:
                    env_id: Gymnasium environment ID (e.g. ``"CartPole-v1"``).
                    num_envs: Number of parallel environments.
                    seed: Base random seed; env ``i`` gets ``seed + i``.

                  Functions:
                   • thunk
                    No description

                   • setup
                    No description

                   • train_dataloader
                    No description

                   • on_before_batch_transfer
                    No description

                   • teardown
                    No description

            📁 models/
              📄 __init__.py
              📄 actor.py
                  Classes:
                   • StochasticActor
                    Stochastic Gaussian actor for SAC with tanh squashing and action rescaling.
                    
                    Args:
                    obs_dim: Observation dimensionality.
                    action_dim: Action dimensionality.
                    hidden_dim: Hidden layer width.
                    num_layers: Number of hidden layers.
                    log_std_min: Lower clamp for log std.
                    log_std_max: Upper clamp for log std.
                    action_scale: (high - low) / 2 for the action space.
                    action_bias: (high + low) / 2 for the action space.

                   • DeterministicActor
                    Deterministic actor for TD3 with action rescaling.
                    
                    Args:
                    obs_dim: Observation dimensionality.
                    action_dim: Action dimensionality.
                    hidden_dim: Hidden layer width.
                    num_layers: Number of hidden layers.
                    action_scale: (high - low) / 2 for the action space.
                    action_bias: (high + low) / 2 for the action space.

                  Functions:
                   • get_action
                    Sample action via reparameterization and compute log prob.
                    
                    Args:
                    obs: ``(B, obs_dim)``
                    
                    Returns:
                    ``(action, log_prob, mean)`` where action is rescaled to the env's
                    action range, log_prob is ``(B,)``, and mean is the deterministic
                    greedy action (also rescaled).

                   • act_deterministic
                    Return deterministic (mean) action for evaluation.
                    
                    Args:
                    obs: ``(B, obs_dim)``
                    
                    Returns:
                    ``tanh(mean) * scale + bias`` with shape ``(B, action_dim)``.

                   • forward
                    Compute rescaled deterministic action.
                    
                    Args:
                    obs: ``(B, obs_dim)``
                    
                    Returns:
                    Action in ``[bias - scale, bias + scale]`` with shape ``(B, action_dim)``.

                   • act_deterministic
                    No description

              📄 critic.py
                  Classes:
                   • TwinCritic
                    Twin Q-network used as the critic in both SAC and TD3.
                    
                    Maintains two **independent** Q-networks (``q1``, ``q2``) with identical
                    architectures.  The minimum of their outputs is used when computing
                    Bellman targets to reduce overestimation bias (Clipped Double-Q Learning).
                    
                    Args:
                    obs_dim: Dimensionality of the observation space.
                    action_dim: Dimensionality of the action space.
                    hidden_dim: Width of each hidden MLP layer.
                    num_layers: Number of hidden MLP layers per Q-network.

                  Functions:
                   • forward
                    Compute Q-values from both networks.
                    
                    Args:
                    obs: Observation tensor of shape ``(B, obs_dim)``.
                    action: Action tensor of shape ``(B, action_dim)``.
                    
                    Returns:
                    Tuple ``(q1, q2)`` each of shape ``(B, 1)``.

                   • min_q
                    Element-wise minimum of the two Q-values.
                    
                    Used in Bellman target computation to penalise overoptimism.
                    
                    Args:
                    obs: Observation tensor of shape ``(B, obs_dim)``.
                    action: Action tensor of shape ``(B, action_dim)``.
                    
                    Returns:
                    Tensor of shape ``(B, 1)`` containing ``min(q1, q2)``.

              📄 ppo_agent.py
                  Classes:
                   • PPOAgentDiscrete
                    PPO agent for discrete action spaces (e.g. CartPole).
                    
                    Args:
                    obs_dim: Observation dimensionality.
                    n_actions: Number of discrete actions.
                    hidden_dim: Hidden layer width (default 64 matching CleanRL).

                   • PPOAgentContinuous
                    PPO agent for continuous action spaces (e.g. Pendulum, HalfCheetah).
                    
                    Also supports RPO (Robust Policy Optimization) when ``rpo_alpha > 0``:
                    during policy-gradient computation a uniform perturbation is added to the
                    action mean, as in the original RPO paper.
                    
                    Args:
                    obs_dim: Observation dimensionality.
                    action_dim: Action dimensionality.
                    hidden_dim: Hidden layer width (default 64 matching CleanRL).
                    rpo_alpha: Perturbation half-width for RPO; 0 disables it (pure PPO).

                  Functions:
                   • layer_init
                    Orthogonal weight init used by CleanRL's PPO agents.

                   • get_value
                    No description

                   • get_action_and_value
                    Sample or evaluate action under Categorical policy.
                    
                    Args:
                    obs: ``(B, obs_dim)``
                    action: If provided, evaluate log-prob/entropy for this action.
                    
                    Returns:
                    ``(action, log_prob, entropy, value)`` all shape ``(B,)`` except
                    action which is ``(B,)`` integer indices.

                   • act_deterministic
                    Return argmax action for callbacks/evaluation.

                   • get_value
                    No description

                   • get_action_and_value
                    Sample or evaluate action under diagonal Normal policy.
                    
                    Args:
                    obs: ``(B, obs_dim)``
                    action: If provided, evaluate log-prob/entropy (RPO perturbation
                    is applied to the mean before evaluation when rpo_alpha > 0).
                    
                    Returns:
                    ``(action, log_prob, entropy, value)`` with log_prob/entropy summed
                    over the action dimensions.

                   • act_deterministic
                    Return mean action for callbacks/evaluation.

              📄 qnetwork.py
                  Classes:
                   • QNetwork
                    Q-value network mapping observations to per-action Q-values.
                    
                    Args:
                    obs_dim: Observation dimensionality.
                    n_actions: Number of discrete actions.

                  Functions:
                   • forward
                    Return Q-values for all actions.
                    
                    Args:
                    obs: ``(B, obs_dim)``
                    
                    Returns:
                    ``(B, n_actions)`` Q-values.

            📁 modules/
              📄 __init__.py
              📄 normalizers.py
                  Classes:
                   • RunningMeanStd
                    Welford's online algorithm for running mean and variance.
                    
                    Maintains a numerically stable estimate of the mean and variance across
                    all observations seen during training.  Thread-safety is not guaranteed
                    — use in a single-process training loop only.
                    
                    Args:
                    shape: Shape of the quantity being tracked (e.g. ``(obs_dim,)`` for
                    a 1-D observation).
                    epsilon: Small constant added to the variance estimate to avoid
                    division by zero during normalisation.

                  Functions:
                   • update
                    Update running statistics with a batch of observations.
                    
                    Uses the parallel/batch variant of Welford's algorithm so that the
                    entire collected batch is incorporated in a single call.
                    
                    Args:
                    x: Array of shape ``(N, *shape)`` containing ``N`` observations.

                   • normalize
                    Normalise observations to approximately zero mean and unit variance.
                    
                    Args:
                    x: Observation array of shape ``(*shape,)`` or ``(N, *shape)``.
                    clip: Symmetric clip value applied after normalisation.  Prevents
                    extreme outliers from destabilising training.
                    
                    Returns:
                    Normalised float32 array with the same shape as ``x``,
                    clipped to ``[-clip, clip]``.

            📁 util/
              📄 __init__.py
              📄 plot_rewards.py
                  Functions:
                   • plot_reward_curve
                    Plot a smoothed episode reward curve.
                    
                    Args:
                    rewards: List of per-episode total rewards.
                    window: Rolling-average window size for smoothing.
                    title: Plot title.
                    save_path: If provided, save the figure to this path instead of
                    displaying interactively.

            📄 __init__.py
            📄 dqn_module.py
            📄 ppo_module.py
                Classes:
                 • PPOModule
                  PPO/RPO LightningModule.
                  
                  The training loop here is unconventional: the ``RolloutDataModule``
                  returns a dummy single-item dataloader so Lightning fires
                  ``training_step`` once per epoch.  That single call owns the entire
                  PPO round: collect rollouts → GAE → update_epochs × minibatches.
                  
                  Args:
                  agent: PPOAgentDiscrete or PPOAgentContinuous instance.
                  num_steps: Rollout length per environment per PPO update.
                  num_envs: Number of parallel environments (must match RolloutDataModule).
                  gamma: Discount factor.
                  gae_lambda: GAE lambda for advantage estimation.
                  num_minibatches: Number of minibatches per update epoch.
                  update_epochs: Number of gradient epochs per PPO update.
                  clip_coef: PPO clipping coefficient ε.
                  ent_coef: Entropy bonus coefficient.
                  vf_coef: Value-function loss coefficient.
                  max_grad_norm: Gradient clipping max norm.
                  norm_adv: Whether to normalise advantages per minibatch.
                  clip_vloss: Whether to apply clipped value loss (as in CleanRL).
                  target_kl: Early-stop update epoch if approx KL exceeds this.
                  anneal_lr: Linearly decay learning rate to 0 over total_timesteps.
                  total_timesteps: Used only when anneal_lr=True.
                  optimizer: Partial optimizer factory (default Adam lr=3e-4, eps=1e-5).

                Functions:
                 • setup
                  No description

                 • configure_optimizers
                  No description

                 • training_step
                  No description

                 • act_deterministic
                  Return deterministic action for callbacks and evaluation.

            📄 sac_module.py
            📄 td3_module.py
            📄 train.py
                Functions:
                 • train
                  Instantiate all components and run the training loop.
                  
                  Args:
                  cfg: Hydra-composed configuration dict.

        📁 tests/
          📄 __init__.py
          📄 conftest.py
          📄 test_config.py
              Functions:
               • test_train_config_loads
                Default config must contain agent, env, and trainer sections.

               • test_config_has_required_targets
                All instantiable config nodes must have a _target_ field.

               • test_agent_has_actor_and_critic
                SAC agent config must have nested actor and critic sub-configs.

               • test_instantiate_env
                RLDataModule must instantiate without errors.

               • test_instantiate_agent
                SACModule must instantiate without errors.

               • test_instantiate_trainer
                Trainer must instantiate without errors.

               • test_debug_config_has_fast_dev_run
                Debug experiment must set fast_dev_run=True.

               • test_debug_config_small_buffer
                Debug experiment must use a small replay buffer.

          📄 test_data.py
          📄 test_model.py
          📄 test_train_script.py
              Functions:
               • test_train_fast_dev_run
                Training with fast_dev_run=True must complete without errors.
                
                This test exercises the full pipeline:
                - Hydra config composition
                - RLDataModule setup + experience collection
                - SACModule training_step (collect + gradient update)
                - Callbacks instantiation

        📄 LICENSE
        📄 pyproject.toml
        📄 README.md
        📄 requirements.txt
        📄 requirements_dev.txt
        📄 tasks_pip.py
            Functions:
             • create_environment
              Create a new conda environment for project.

             • requirements
              Install project requirements.

             • dev_requirements
              Install development requirements.

             • train
              Train SAC agent on Pendulum-v1 (default).

             • train_td3
              Train TD3 agent on Pendulum-v1.

             • test
              Run tests.

             • test_debug
              Run a fast debug training pass (single step, no WandB).

             • build_docs
              Build documentation.

             • serve_docs
              Serve documentation locally.

        📄 tasks_uv.py
            Functions:
             • create_environment
              Create a new uv virtual environment and install dependencies.

             • requirements
              Install project requirements.

             • dev_requirements
              Install development requirements.

             • train
              Train SAC agent on Pendulum-v1 (default).

             • train_td3
              Train TD3 agent on Pendulum-v1.

             • test
              Run tests.

             • test_debug
              Run a fast debug training pass (single step, no WandB).

             • build_docs
              Build documentation.

             • serve_docs
              Serve documentation locally.

      📄 cookiecutter.json
  📁 tests/
    📄 README.md
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

         • test_mnist_wandb_image_logger_template_success
          Test successful generation of MNIST_wandb_image_logger template.
          
          Args:
          temp_dir: temporary directory for test

         • test_barebone_minimal_structure
          Test generation of barebone template with minimal structure (no docs).
          
          Args:
          temp_dir: temporary directory for test

         • test_barebone_with_uv_deps_manager
          Test generation of barebone template with UV dependency manager.
          
          Args:
          temp_dir: temporary directory for test

         • test_barebone_with_pip_deps_manager
          Test generation of barebone template with pip dependency manager.
          
          Args:
          temp_dir: temporary directory for test

         • test_classification_with_uv_deps_manager
          Test generation of classification template with UV dependency manager.
          
          Args:
          temp_dir: temporary directory for test

         • test_flow_matching_with_uv_deps_manager
          Test generation of flow_matching template with UV dependency manager.
          
          Args:
          temp_dir: temporary directory for test

         • test_mnist_wandb_with_uv_deps_manager
          Test generation of MNIST_wandb_image_logger template with UV dependency manager.
          
          Args:
          temp_dir: temporary directory for test

         • test_rl_template_success
          Test successful generation of RL template with default options.
          
          Args:
          temp_dir: temporary directory for test

         • test_rl_template_with_uv_deps_manager
          Test generation of RL template with UV dependency manager.
          
          Args:
          temp_dir: temporary directory for test

         • test_barebone_template_internal_tests
          Test that the generated barebone template's internal tests pass.
          
          This is an integration test that:
          1. Generates a project from the template
          2. Installs its dependencies
          3. Runs the generated project's test suite
          
          Args:
          temp_dir: temporary directory for test

         • test_flow_matching_template_internal_tests
          Test that the generated flow_matching template's internal tests pass.
          
          This is an integration test that:
          1. Generates a project from the template
          2. Installs its dependencies
          3. Runs the generated project's test suite
          
          Args:
          temp_dir: temporary directory for test

         • test_mnist_wandb_template_internal_tests
          Test that the generated MNIST_wandb_image_logger template's internal tests pass.
          
          This is an integration test that:
          1. Generates a project from the template
          2. Installs its dependencies
          3. Runs the generated project's test suite
          
          Args:
          temp_dir: temporary directory for test

  📄 CLAUDE.md
  📄 mkdocs.yml
  📄 PROJECT_STRUCTURE.md
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

  📄 pyproject.toml
  📄 pyrightconfig.json
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

