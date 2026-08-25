import pytest
from src.crew import ResearchCrew

def test_setup_agents():
    crew = ResearchCrew("Test Topic")
    researcher, writer = crew.setup_agents()
    
    assert researcher.role == 'Senior Research Analyst'
    assert 'Test Topic' in researcher.goal
    
    assert writer.role == 'Tech Content Strategist'
    assert 'Test Topic' in writer.goal

def test_setup_tasks():
    crew = ResearchCrew("Test Topic")
    researcher, writer = crew.setup_agents()
    tasks = crew.setup_tasks(researcher, writer)
    
    assert len(tasks) == 2
    assert 'Test Topic' in tasks[0].description
    assert tasks[0].agent == researcher
    assert tasks[1].agent == writer

def test_run():
    crew = ResearchCrew("Test Topic")
    result = crew.run()
    assert "Simulated execution" in result
