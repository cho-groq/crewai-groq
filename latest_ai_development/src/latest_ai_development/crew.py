from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool
from .tools.custom_tool import PDFTool

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class LatestAiDevelopment():
    """LatestAiDevelopment crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml' 

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def pdf_to_txt(self) -> Agent:
        return Agent(
            config=self.agents_config['pdf_to_txt'],
            verbose=True,
            tools=[PDFTool()]
        )
    
    @agent
    def reader_summarizer(self) -> Agent:
        return Agent(
            config=self.agents_config['reader_summarizer'],
            verbose=True,
            tools=[FileReadTool(file_path='./papers/output')]
        )

    @agent
    def quote_finder(self) -> Agent:
        return Agent(
            config=self.agents_config['quote_finder'],
            verbose=True,
            tools=[FileReadTool(file_path='./papers/output')]
        )

    @agent
    def quote_rater(self) -> Agent:
        return Agent(
            config=self.agents_config['quote_rater'],
            verbose=True,
            
        )

    @agent
    def final_editor(self) -> Agent:
        return Agent(
            config=self.agents_config['final_editor'],
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def pdf_to_txt_task(self) -> Task:
        return Task(
            config=self.tasks_config['pdf_to_txt_task'],
            output_file='./papers/output.txt'
        )
    
    @task
    def summary_task(self) -> Task:
        return Task(
            config=self.tasks_config['summary_task'],
            output_file='summary.md'
        )

    @task
    def quote_extraction_task(self) -> Task:
        return Task(
            config=self.tasks_config['quote_extraction_task'],
            output_file='quotes_raw.md'
        )

    @task
    def quote_rating_task(self) -> Task:
        return Task(
            config=self.tasks_config['quote_rating_task'],
            output_file='quotes_rated.md'
        )

    @task
    def final_quote_selection_task(self) -> Task:
        return Task(
            config=self.tasks_config['final_quote_selection_task'],
            output_file='quotes_final.md'
        )


    @crew
    def crew(self) -> Crew:
        """Creates the LatestAiDevelopment crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential, # the order in which you make the tasks matter
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
