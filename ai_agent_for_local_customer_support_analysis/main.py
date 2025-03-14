#!/usr/bin/env python
import sys
from ai_agent_for_local_customer_support_analysis.crew import AiAgentForLocalCustomerSupportAnalysisCrew

# This main file is intended to be a way for your to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'social_media_urls': 'sample_value',
        'research_keywords': 'sample_value',
        'news_source_urls': 'sample_value',
        'local_platform_list': 'sample_value'
    }
    AiAgentForLocalCustomerSupportAnalysisCrew().crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'social_media_urls': 'sample_value',
        'research_keywords': 'sample_value',
        'news_source_urls': 'sample_value',
        'local_platform_list': 'sample_value'
    }
    try:
        AiAgentForLocalCustomerSupportAnalysisCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        AiAgentForLocalCustomerSupportAnalysisCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'social_media_urls': 'sample_value',
        'research_keywords': 'sample_value',
        'news_source_urls': 'sample_value',
        'local_platform_list': 'sample_value'
    }
    try:
        AiAgentForLocalCustomerSupportAnalysisCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: main.py <command> [<args>]")
        sys.exit(1)

    command = sys.argv[1]
    if command == "run":
        run()
    elif command == "train":
        train()
    elif command == "replay":
        replay()
    elif command == "test":
        test()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import ScrapeWebsiteTool
from crewai_tools import SeleniumScrapingTool
from crewai_tools import ScrapeElementFromWebsiteTool

scrape_tool = ScrapeWebsiteTool()
selenium_tool = SeleniumScrapingTool()
element_scrape_tool = ScrapeElementFromWebsiteTool()
social_media_researcher=Agent(
  role= "Social Media & Reviews Specialist",
  goal= "Scrape and analyze online reviews, social media posts, and forum discussions"
    "using {social_media_urls} and extract recurring themes such as long wait times,"
    "language barriers, and limited after-hours support using {research_keywords}.",
  backstory= "As an experienced research specialist focusing on digital content, you"
    "excel at capturing customer sentiments from various social media platforms and"
    "review sites. Your insights help identify core issues in customer support based"
    "on trending feedback.",
  tools=[scrape_tool],
  verbose=True)
news_analysis_specialist=Agent(
  role= "Local News Analyst",
  goal= "Scrape and process news articles using {news_source_urls} to extract data"
   " points and quotes about customer support challenges and improvements, applying"
   " {research_keywords} for guiding themes.",
  backstory= "Leveraging a deep understanding of local news trends, you turn articles"
    "into actionable data. Your analytical skills uncover systemic issues and patterns"
    "in customer support reported by the media.",
  tools=[selenium_tool,element_scrape_tool],
  verbose=True)
platform_investigator=Agent(
  role= "Platform Research Specialist",
  goal= "Evaluate customer feedback and support complaints from specific platforms"
    "such as {local_platform_list} by scraping relevant websites and extracting real-world"
    "examples illustrating common issues.",
  backstory=" With expertise in navigating diverse digital platforms, you specialize"
    "in capturing and analyzing customer experiences on sites like Daraz.pk, Foodpanda.pk,"
   " and others. Your mission is to gather evidence directly from user interactions.",
  tools=[scrape_tool,selenium_tool,element_scrape_tool],
  verbose=True)
data_aggregator_insight=Agent(
  role= "Data Aggregation & Report Expert",
  goal= "Consolidate findings from various sources, analyze the aggregated data using"
    "{research_keywords}, and generate a comprehensive report with actionable insights"
    "and recommendations for improving customer support.",
  backstory= "As the final integrator of multiple research streams, your aptitude for"
    "data synthesis helps translate raw information into clear reports that drive strategic"
    "decisions.",
  verbose=True)
scrape_social_media_reviews=Task(
  description=(" Using the provided {social_media_urls}, scrape online reviews, forum"
  "  discussions, and social media posts related to customer support issues. Leverage"
  "  the ScrapeWebsiteTool to capture the raw data, ensuring to capture details linked"
   " with {research_keywords}."),
  expected_output=("Raw scraped data including customer reviews and social media posts"
   " highlighting themes like long wait times and other support performance issues"
    "using {research_keywords}."),
  tools=[scrape_tool ],
  async_execution= False,
  agent= social_media_researcher,)
analyze_social_media_feedback=Task(
  description=(" Analyze the scraped social media data to identify recurring customer"
   " support issues using the keywords {research_keywords}. Focus on spotting patterns"
    "such as long wait times, language barriers, and limited after-hours support."),
  expected_output=("A structured summary listing recurring customer support problems"
   " extracted from social media reviews and discussions."),
  async_execution= False,
  agent= social_media_researcher,
  context=[ scrape_social_media_reviews])
scrape_news_articles=Task(
  description=(" Utilize {news_source_urls} to scrape recent news articles that mention"
  "  customer support challenges or improvements. Use SeleniumScrapingTool to access"
   " dynamic content when needed."),
  expected_output=( "Raw content from news articles including references to customer"
   " support issues, complaints, or improvements."),
  tools=[selenium_tool],
  async_execution= False,
  agent= news_analysis_specialist,)
extract_news_insights=Task(
  description=( "Extract key data points, quotes, and evidence from the news articles"
   " that indicate systemic customer support issues, guided by {research_keywords}."
   " Use ScrapeElementFromWebsiteTool to target specific parts of the articles."),
  expected_output=( "A collection of extracted insights and data points that highlight"
    "recurring customer support problems as reported in the news."),
  tools=[element_scrape_tool],
  async_execution= False,
  agent= news_analysis_specialist,
  context=[scrape_news_articles])
scrape_platform_feedback=Task(
  description=( "Access websites listed in {local_platform_list}, including Daraz.pk,"
   " Foodpanda.pk, and others, to scrape customer feedback and support complaints."
   " Employ tools like ScrapeWebsiteTool or SeleniumScrapingTool based on each site’s"
   " structure."),
  expected_output=(" Raw customer feedback and complaint data from the specified platforms"
   " capturing direct user experiences and issues."),
  tools=[scrape_tool,selenium_tool],
  async_execution= False,
  agent= platform_investigator,)
extract_platform_examples=Task(
  description=( "From the scraped feedback of {local_platform_list}, extract concrete"
  "  examples and case studies that illustrate customer support pain points, using"
   " targeted extraction with ScrapeElementFromWebsiteTool."),
  expected_output=( "A curated list of case studies and real-world examples that showcase"
   " recurring customer support issues from the designated platforms."),
  tools=[element_scrape_tool],
  async_execution= False,
  agent= platform_investigator,
  context=[scrape_platform_feedback])
aggregate_and_consolidate_data=Task(
  description=( "Aggregate and consolidate data from social media analysis, news insights,"
   " and platform-specific feedback. Analyze the combined data to identify and verify"
    "recurring customer support issues based on {research_keywords}."),
  expected_output=(" A consolidated dataset summarizing key recurring customer support"
   " issues along with supporting evidence from multiple sources."),
  async_execution= False,
  agent= data_aggregator_insight,
  context=[analyze_social_media_feedback,extract_news_insights,extract_platform_examples])
generate_comprehensive_report=Task(
  description=( "Using the aggregated data from previous tasks, generate a comprehensive"
   " report that details the identified customer support pain points. Include actionable"
    "insights and recommendations for improvement, guided by the trends from {research_keywords}."),
  expected_output=( "A formatted comprehensive report summarizing key pain points, supported"
    "by data and real-world examples, along with actionable recommendations for enhancing"
    "customer support."),
  async_execution= False,
  agent= data_aggregator_insight,
  context=[aggregate_and_consolidate_data])
crew = Crew(
    agents=[
        social_media_researcher,
        news_analysis_specialist,
        platform_investigator,
        data_aggregator_insight
    ],
    tasks=[
        scrape_social_media_reviews,
        analyze_social_media_feedback,
        scrape_news_articles,
        extract_news_insights,
        scrape_platform_feedback,
        extract_platform_examples,
        aggregate_and_consolidate_data,
        generate_comprehensive_report
    ],
    verbose=2,
    memory=True
)
inputs = {
    'local_platform_list': [
        'Daraz.pk', 'Foodpanda.pk', 'Careem', 'Bykea', 'EasyPaisa',
        'OLX Pakistan', 'Ufone', 'Zong', 'Jazz'
    ],
    'social_media_urls': [
        'https://www.facebook.com/DarazPK/reviews',
        'https://www.facebook.com/FoodpandaPK/reviews',
        'https://twitter.com/search?q=customer+support+Pakistan',
        'https://www.reddit.com/r/Pakistan/comments/',
        'https://www.facebook.com/Bykea',
        'https://twitter.com/Bykea',
        'https://www.facebook.com/EasyPaisa',
        'https://twitter.com/EasyPaisa',
        'https://www.facebook.com/OLXPakistan',
        'https://twitter.com/OLXPakistan',
        'https://www.facebook.com/UfoneOfficial',
        'https://twitter.com/UfoneOfficial',
        'https://www.facebook.com/ZongPK',
        'https://twitter.com/ZongPK',
        'https://www.facebook.com/JazzPK',
        'https://twitter.com/JazzPK'
    ],
    'news_source_urls': [
        'https://www.dawn.com',
        'https://www.geo.tv',
        'https://tribune.com.pk',
        'https://www.thenews.com.pk'
    ],
    'research_keywords': [
        'customer support', 'long wait times', 'language barriers',
        'after-hours support', 'complaint resolution', 'service delays',
        'feedback analysis', 'support improvement', 'digital support issues',
        'customer dissatisfaction'
    ]
}
