![Logo](./assets/logo_wide.png)
<div align="center">
<h2>Your 2-in-1 AI Scrum Master and Developer</h2>
</div>

Clean Coder: Your AI-powered software project assistant. Plan, manage, and code your projects step-by-step. From task breakdown to implementation, Clean Coder streamlines your development process for efficient, organized results.

## Try it right away:
```
# clone repo
git clone https://github.com/GregorD1A1/Clean-Coder-AI

# go to directory
cd Clean-Coder-AI

# install dependencies
pip install -r requirements.txt

# provide path to the project directory you'll work on
export WORK_DIR=/path/to/your/project/dir

# provide api keys
export OPENAI_API_KEY=your_api_key_here
export ANTHROPIC_PROJECT_ID=your_api_key_here

# run Clean Coder
python clean_coder_pipeline.py
```
or check detailed instructions [how to start in documentation](https://clean-coder.dev/quick_start/programmer_pipeline/).


## Key advantages:

- Well-designed context pipeline: The LLM only receives necessary information into its context. This significantly improves the LLM's attention and reduces costs.
- Ability to create a frontend based on images with designs.
- Automatic context updates after file modifications: There's no need to manually reload the file into the LLM context after adding a few lines.
- Automatic code linting and log check to ensure corectness of inserted code.
- Well-designed tools: These are specially designed to exchange appropriate parts of the code and navigate the file system. A human approval feature is added as a safety measure in case of code interference tools.

# How to work with Clean Coder

## Minimal Setup

Change name of `.env.template` file to `.env` and open it with text editor. Provide your OpenAI and Anthropic api keys, and path to project directory you will be working on with trailing slash.

Next, install required dependencies by running:

`pip install -r requirements.txt`

## Recommended setup

### Bugs self-correction
To allow AI correct it's own mistakes automatically, set up saving logs to the text file in your project. Next, provide path to log file `LOG_FILE=` in .env file. Use trailing slash.

### Retrieval tool for Researcher agent
Sometimes just looking on the file system is not enough to Researcher agent been able to provide other agents with all necesary files; especially if your project contains a lot of files with code. Then retreival tool becoming handy: it allows Researcher to find needed files semantically, using generated descriptions and vector search.

To set it up, run 

`python rag/write_descriptions.py`

file to create descriptions of all code files in your project and save them in vector starage. Eventually, you can provide subfolders with code files "subfolders_with_files" argument of "write_descriptions" function if you don't want it to describe all code files in your project.

Next, get api key for cohere and provide it on .env after `COHERE_API_KEY=`.

## Working process


### 1. Define Task

In `clean_coder_pipeline.py`, modify the task variable. Describe your task in detail. It is advisable to provide "unit" tasks - smaller ones and run the program multiple times rather than asking it to perform a complex task all at once. Specify which files to edit and, if creating a frontend, which design templates to use.

### 2. Launch

Launch Clean Coder by running:

`python clean_coder_pipeline.py`

### 3. Researcher Agent

Launch the app. The first agent to begin work is the Researcher - its job is to examine files in the project directory and identify only the necessary files to work on. Additionally, it can locate image graphics as templates for frontend coding (you need to store designs somewhere in the project dir.).

Once the research is complete, the Researcher will display the suggested files to work on. Type 'ok' and press enter if you agree with his research or provide your feedback if you want it to add/remove some files.

### 4. Planner Agent

The Planner is the most responsible agent - it drafts the plan for code modifications. It's recommended to thoroughly review the plan it proposes and request it to make changes until the plan it outputs is satisfactory. Then, type 'ok' to proceed to the executor. Only the last planner message is provided to the executor, so ensure that it provides the complete plan in it.

### 5. Executor Agent

This is where the actual magic happens. The Executor will implement the planned changes to your project files. It will call tools in sequence, which will either modify files or create new ones. For tools that interact with the project, a safety mechanism is introduced - you need to confirm the tool execution by writing 'ok'. It's recommended to first check what change it intends to make and provide feedback if you think it might break something. After all changes are implemented, it will check the log file (if you set it up) and make further changes if there are issues with the logs. Next, it will ask you to confirm if everything is done as intended - provide feedback if you want it to improve something or type 'ok' to end the pipeline.


## Demo videos

[![Demo video](https://img.youtube.com/vi/LLiABw4gY_w/maxresdefault.jpg)](https://youtu.be/LLiABw4gY_w "Demo video")

[![Demo video](https://img.youtube.com/vi/d5qbX-v4qwM/maxresdefault.jpg)](https://youtu.be/d5qbX-v4qwM "Demo video")

## Contibutions

All contributions to the project are very welcome!

If you're planning to make a major change, please open an issue first to discuss your proposed changes.
