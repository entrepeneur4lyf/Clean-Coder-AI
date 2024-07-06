from agents.researcher_agent import research_task
from agents.planner_agent import planning
from agents.executor_agent import Executor


task = """
Make tooltip in the home page showing above the finder window. Also rename it to make name more understandable:
profileUnavailabeTooltip for example. also rename redirectToPost function to seeMemProfile. 
"""


files, file_contents, images = research_task(task)

plan = planning(task, file_contents, images)

executor = Executor(files)
executor.do_task(task, plan, file_contents)
