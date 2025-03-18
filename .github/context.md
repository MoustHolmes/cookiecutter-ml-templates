# Cookiecutter machine learning template library

I wanna create my own library for machine learning templates. This is as much for my self for making sure that when I have done a project I clean it up and make it so that i can reuse the good parts. I want to have a variety of templates since most machine learning projects fall into a few categories. Like image classification, regression, graph data, variational auto encoders, NLL, reinforcement learning.




-  **Multiple specialised templates**. Not just a single template to fit all but multiple which makes easier to modify to your purpose and is more educational and helps with how fast you can get to a working for your project if you don't have to change the default project from classification to regression or another type.
- cookiecutter makes it very flexible to choose what you want and what you don't.
- **Collaborative**: Having multiple templates makes it easier for other people to add the project

# Structure
I was thinking a structure like this?
Cookiecutter_machine_learning_template_library
## Repository Structure

```

Cookiecutter_machine_learning_template_library/
├── docs/ # Global documentation (MkDocs Material)
├── hooks/ # Shared Cookiecutter hooks (optional; can also be per template)
├── templates/ # Collection of ML project templates
│ ├── barebone/
│ │ ├── cookiecutter.json
│ │ ├── hooks/
│ │ ├── {{ cookiecutter.repo_name }}/
│ │ └── ... (other files)
│ ├── barebone_classification/
│ │ ├── cookiecutter.json
│ │ └── ... (classification-specific scaffold)
│ ├── mnist_classification/
│ │ └── ... (MNIST demo project)
│ ├── barebone_regression/
│ │ └── ... (regression template)
│ ├── starfish_object_detection/
│ │ └── ... (object detection scaffold)
│ └── cartpole_reinforcement_learning/
│ └── ... (reinforcement learning scaffold)
├── tests/ # Integration tests for validating template generation
├── tasks.py # Automation tasks (e.g., build, test, docs, environment setup)
├── .pre-commit-config.yaml # Pre-commit hook configuration (using Ruff, Black, etc.)
├── .github/
│ └── workflows/ # GitHub Actions CI/CD workflows for linting, testing, and docs building
├── README.md # This file
└── requirements.txt # Global development dependencies

```

I will use the different cookiecutter hooks like pre_prompt.py pre_gen_project.py post_gen_project.py for removing the unused templates after creations of the template

# Best practices
I have done a few projects by now and have learned a thing or two about best practices both in regards to code style and machine learning.
I want to make it as easy to make good structured projects.

## AI assisted  coding
I use vscode and have recently started using github copilot. With its agent mode where it can look around the workspace to find relevant files, make changes to those files and run commands many thing like having good code structure have become very easy when you use tools like black, ruff and pytest.

One thing I found is that its not very good at is starting from scratch which is one of the reason im creating these templates so that is can have a good starting point.

i want to make sure that the ai that reads the code know the structure and the philosophy of the project. github copilot supports having a custom instructions file in .github/copilot-instructions.md where everything on code style and structure should be placed

use a roadmap for implementing a feature.
test driven development. write unit tests for all critical part of the code like datasets models and test often.
When writing machine learning code write the expected input and output shapes.

do not start working on new features on your own accord.

# Other templates
## [[Lightning-Hydra-Template]]
I have used this template twice and its the main inspiration for this project as i think its nearly perfect. But there is some flaws
- Supports  7 different loggers  which on the surface sounds good
- Makes use of the creators own package pyrootutils which is a dependency I don't want.
- Makes us of some custom wrappers which makes sure logging on multiple gpu is done correctly but I think is outside of the scope of a template and is something lightning should fix if its a problem.  I also think is makes the code less readable .

## ml_ops_template
https://github.com/SkafteNicki/mlops_template used in the ml_ops course I took.
its very plain but well structured. It does however it does include some bloat for the course and some api stuff I don't feel i need. If cleaned up its my favourite pure pytorch template.
I have made a project with this template at https://github.com/mmmmaja/starfishDetection
which makes use of hydra and lightning.

## nn-template
https://github.com/grok-ai/nn-template
Have the best documentation using materials mkdocs. the integrations with github and the commands run in [post_gen_query.py](https://github.com/grok-ai/nn-template/blob/8ba02bba8f015e1eb7efb0d2ab8c9d433bd1c431/hooks/post_gen_project.py#L72) is very nice.


## minimal-ml-template
https://github.com/AntreasAntoniou/minimal-ml-template
uses hydra-zen instead and huggingface for model and dataset registry. I don't enjoy the project structure. but the template



# Packages
## Pytorch lightning
I like to use pytorch lightning both for code structure but also the added features like distributed training callbacks like early stopping

## Hydra
for config files
### Hydra-zen
im not totally convinced by this package yet
https://mit-ll-responsible-ai.github.io/hydra-zen/

## WandB
in contrast to the [[Lightning-Hydra-Template]] I want to only use one logger (maybe a csv logger when offline) this also allows me to make use of wandb more advanced features like model register artifacts and make custom logging callbacks specific for wandb.

## Cookiecutter
see [[Cookiecutter Data Science]] I wanna use the a cookiecutter template with my own template using cookiecutter is more flexible that just creating a github template


## Code style

### pre-commit
https://pre-commit.com/
I have to figure out what i want in my pre-commits as there is many different options as can be seen in the different templates [nn-template](https://github.com/grok-ai/nn-template/blob/8ba02bba8f015e1eb7efb0d2ab8c9d433bd1c431/%7B%7B%20cookiecutter.repository_name%20%7D%7D/.pre-commit-config.yaml), [mlops-template](https://github.com/SkafteNicki/mlops_template/blob/master/%7B%7B%20cookiecutter.repo_name%20%7D%7D/.pre-commit-config.yaml), [lightning-hydra-template](https://github.com/ashleve/lightning-hydra-template/blob/main/.pre-commit-config.yaml)
### ruff
https://docs.astral.sh/ruff/

### Black
https://github.com/psf/black

## Tasks - invoke
https://www.pyinvoke.org/

## Documentation - Material for MkDocs
https://squidfunk.github.io/mkdocs-material/
its a package for writing documentation. for my project I want to use it for a bit more than just documenting the templates and projects. I also want go into more detail on the used packages like wandb lightning, ruff, black and reference to other reading materials videos etc like [[Lightning-Hydra-Template]].


## Tests -pytest
I want to make good use of unit tests especially since i will make use of ai coding copilots which works best if there is tests to make sure that what they write is correct.

There should be some tests which is in the main template which tests the creation of templates and such. but there is also the tests that is in the templates for the code in the spesific template like for dataset models etc.

however I would like to be able to run a long test that creates tries to create the template and then run the tests in the templates

# Features
These features doesn't need to be in every template but i would like to try to implement them
### Callbacks
one of the main pros for pytorch lightning is the code structure and callbacks is a way to define optional callbacks for the training loop and model which is able to use hooks at different points in training validation testing and prediction to what ever I wan . this could be complicated logging of metrics like logging attention. the advantage of callbacks is that code that isn't strictly necessary for training the model is abstracted into other files which makes it easier to read and understand model and the training.
also being able to simply turn off things like wandb artefacts or models registry if something breaks is super useful.

## WANDB model registry
I would like to be able to easily upload models to wandb registry https://docs.wandb.ai/guides/core/registry/

I have worked in collaborations where models basically never left the creators machine being able to share models easily would be nice

## WANDB artefacts for datasets
https://docs.wandb.ai/guides/artifacts/
I often end up having a notebook filled with random plots on the dataset but being able to just go into wandb see which artifact was used to run that

## Automatic Analysis plots / saving predictions in wandb tables
https://docs.wandb.ai/guides/models/tables/

## Model profiling
https://pytorch-lightning.readthedocs.io/en/1.5.10/advanced/profiler.html

## Ensemble methods
i want to easily be able to run ensemble methods if i want to use the template for kaggle competitions
# Environments
I have been using conda as my default for creating environments so I will stick to that but could consider using [[uv]]

## Documentation
the [[Lightning-Hydra-Template]] does a good job of actually providing documentation of basic use of the template but I would like mine to be even more educational with lots of lessons I have learned form the [[Machine Learning Operations]] course and the reasons for choosing the packages.
