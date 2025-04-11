import requests
import json
from typing import Dict, Any, List

class OllamaInterface:
    def __init__(self, host: str = 'http://localhost:11434', model: str = 'llama3'):
        """
        Initialize Ollama interface
        
        :param host: Ollama server host
        :param model: LLM model to use
        """
        self.host = host
        self.model = model

    def generate(self, prompt: str, max_tokens: int = 500) -> str:
        """
        Generate text using Ollama
        
        :param prompt: Input prompt
        :param max_tokens: Maximum tokens to generate
        :return: Generated text
        """
        url = f'{self.host}/api/generate'
        payload = {
            'model': self.model,
            'prompt': prompt,
            'stream': False,
            'options': {
                'max_tokens': max_tokens
            }
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()['response']
        except requests.RequestException as e:
            print(f"Ollama generation error: {e}")
            return ""

    def summarize_job_description(self, job_description: str) -> Dict[str, Any]:
        """
        Summarize job description using Ollama
        
        :param job_description: Full job description text
        :return: Structured job description summary
        """
        prompt = f"""
        Analyze the following job description and extract key details:
        
        {job_description}
        
        Please provide a structured summary with the following fields:
        - Job Title
        - Required Skills (comma-separated list)
        - Experience Level
        - Key Responsibilities
        - Minimum Qualifications
        
        Respond in JSON format.
        """
        
        summary = self.generate(prompt)
        try:
            return json.loads(summary)
        except json.JSONDecodeError:
            return {
                'title': '',
                'required_skills': [],
                'experience_level': '',
                'responsibilities': '',
                'qualifications': ''
            }