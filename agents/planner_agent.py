from langchain_openai.chat_models import ChatOpenAI
from langchain.output_parsers import XMLOutputParser
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import END, StateGraph
from dotenv import load_dotenv, find_dotenv
from langchain_community.chat_models import ChatOllama
from langchain_anthropic import ChatAnthropic
from utilities.util_functions import print_wrapped
from utilities.langgraph_common_functions import call_model, ask_human, after_ask_human_condition


load_dotenv(find_dotenv())

llm = ChatOpenAI(model="gpt-4-vision-preview", temperature=0.3)
#llm = ChatAnthropic(model='claude-3-opus-20240229')
#llm = ChatOllama(model="mixtral") #, temperature=0)


class AgentState(TypedDict):
    messages: Sequence[BaseMessage]
    voter_messages: Sequence[BaseMessage]


system_message = SystemMessage(
    content="You are programmer and scrum master expert. You guiding your code monkey friend about what changes need to be done "
            "in code in order to execute given task. You describing in GIT-like format what code "
            "need to be inserted, deleted, replaced or which file created. Provide only the changes."
            "When writing your changes plan, you planning only code changes, neither library installation or tests or anything else."
            "At every your message, you providing proposition of all changes, not just some."
            "The user can't modify your code. So do not suggest incomplete code which requires users to modify."
)

voter_system_message = SystemMessage(
    content="Several implementation plans for a task implementation have been proposed. "
            "Carefully analyze these plans and determine which one accomplishes "
            "the task most effectively.\n"
            "Take in account the following criteria:\n"
            "1. The primary criterion is the effectiveness of the plan in executing the task."
            "2. A secondary criterion is the completeness of the code. "
            "The ideal plan would not require any further modifications or completion of placeholders."
            "\n\n"
            " Respond in xml:\n"
            "```xml"
            "<response>"
            "   <reasoning>"
            "       Explain your decision process in detail. Provide pros and cons of every proposition."
            "   </reasoning>"
            "   <choice>"
            "       Provide here nr of plan you chosen. Only the number and nothing more."
            "   </choice>"
            "</response>"
            "```"
)


# node functions
def call_planers(state):
    messages = state["messages"]
    nr_plans = 3
    plan_propositions_str = "Here are plan propositions:"
    print(f"\nGenerating plan propositions...")
    plan_propositions_messages = llm.batch([messages for _ in range(nr_plans)])
    for i, proposition in enumerate(plan_propositions_messages):
        plan_propositions_str += f"\n\n###\n\nProposition nr {i+1}:\n\n" + proposition.content

    print("Choosing the best plan...")
    state["voter_messages"].append(HumanMessage(content=plan_propositions_str))
    chain = llm | XMLOutputParser()
    response = chain.invoke(state["voter_messages"])

    choice = int(response["response"][1]["choice"])
    plan = plan_propositions_messages[choice - 1]
    state["messages"].append(plan)
    print_wrapped(f"Chosen plan:\n\n{plan.content}")

    return state


def call_model_corrector(state):
    state, response = call_model(state, llm)
    return state


# workflow definition
researcher_workflow = StateGraph(AgentState)

researcher_workflow.add_node("planers", call_planers)
researcher_workflow.add_node("agent", call_model_corrector)
researcher_workflow.add_node("human", ask_human)
researcher_workflow.set_entry_point("planers")

researcher_workflow.add_edge("planers", "human")
researcher_workflow.add_edge("agent", "human")
researcher_workflow.add_conditional_edges("human", after_ask_human_condition)

researcher = researcher_workflow.compile()


def planning(task, file_contents, images):
    print("Planner starting its work")
    message_content = [f"Task: {task},\n\nFiles:\n{file_contents}"] + images
    message_from_researcher = HumanMessage(content=message_content)

    inputs = {
        "messages": [system_message, message_from_researcher],
        "voter_messages": [voter_system_message, message_from_researcher]
    }
    planner_response = researcher.invoke(inputs, {"recursion_limit": 50})["messages"][-2]

    return planner_response.content
