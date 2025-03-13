from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import ScrapeWebsiteTool
from crewai_tools import SeleniumScrapingTool
from crewai_tools import ScrapeElementFromWebsiteTool

@CrewBase
class AiAgentForLocalCustomerSupportAnalysisCrew():
    """AiAgentForLocalCustomerSupportAnalysis crew"""

    @agent
    def social_media_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['social_media_researcher'],
            tools=[ScrapeWebsiteTool()],
        )

    @agent
    def news_analysis_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['news_analysis_specialist'],
            tools=[SeleniumScrapingTool(), ScrapeElementFromWebsiteTool()],
        )

    @agent
    def platform_investigator(self) -> Agent:
        return Agent(
            config=self.agents_config['platform_investigator'],
            tools=[ScrapeWebsiteTool(), SeleniumScrapingTool(), ScrapeElementFromWebsiteTool()],
        )

    @agent
    def data_aggregator_insight(self) -> Agent:
        return Agent(
            config=self.agents_config['data_aggregator_insight'],
            tools=[],
        )


    @task
    def scrape_social_media_reviews(self) -> Task:
        return Task(
            config=self.tasks_config['scrape_social_media_reviews'],
            tools=[ScrapeWebsiteTool()],
        )

    @task
    def analyze_social_media_feedback(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_social_media_feedback'],
            
        )

    @task
    def scrape_news_articles(self) -> Task:
        return Task(
            config=self.tasks_config['scrape_news_articles'],
            tools=[SeleniumScrapingTool()],
        )

    @task
    def extract_news_insights(self) -> Task:
        return Task(
            config=self.tasks_config['extract_news_insights'],
            tools=[ScrapeElementFromWebsiteTool()],
        )

    @task
    def scrape_platform_feedback(self) -> Task:
        return Task(
            config=self.tasks_config['scrape_platform_feedback'],
            tools=[ScrapeWebsiteTool(), SeleniumScrapingTool()],
        )

    @task
    def extract_platform_examples(self) -> Task:
        return Task(
            config=self.tasks_config['extract_platform_examples'],
            tools=[ScrapeElementFromWebsiteTool()],
        )

    @task
    def aggregate_and_consolidate_data(self) -> Task:
        return Task(
            config=self.tasks_config['aggregate_and_consolidate_data'],
            
        )

    @task
    def generate_comprehensive_report(self) -> Task:
        return Task(
            config=self.tasks_config['generate_comprehensive_report'],
            
        )


    @crew
    def crew(self) -> Crew:
        """Creates the AiAgentForLocalCustomerSupportAnalysis crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
