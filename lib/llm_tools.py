#!/usr/bin/env python3
"""
LLM Integration Module for Guidora Story Generation
Provides unified interface for OpenAI, Anthropic, and other LLM providers
"""

import os
import json
import time
import logging
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import hashlib

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("💡 Install python-dotenv for automatic .env loading: pip install python-dotenv")

# Optional imports - will gracefully handle missing dependencies
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

@dataclass
class LLMResponse:
    """Standardized response from LLM providers."""
    content: str
    provider: str
    model: str
    tokens_used: int
    cost_estimate: float
    response_time: float
    timestamp: str
    prompt_hash: str

@dataclass
class LLMConfig:
    """Configuration for LLM providers."""
    provider: str  # "openai", "anthropic", "local"
    model: str
    api_key: Optional[str] = None
    max_tokens: int = 1000
    temperature: float = 0.7
    timeout: int = 30
    retry_attempts: int = 3
    cost_limit_per_request: float = 0.10  # $0.10 max per request

class LLMProvider:
    """Base class for LLM providers."""
    
    def __init__(self, config: LLMConfig):
        self.config = config
        self.logger = logging.getLogger(f"llm.{config.provider}")
        self._setup_client()
    
    def _setup_client(self):
        """Setup provider-specific client."""
        raise NotImplementedError
    
    def generate(self, prompt: str, **kwargs) -> LLMResponse:
        """Generate response from LLM."""
        raise NotImplementedError
    
    def _calculate_cost(self, tokens: int, model: str) -> float:
        """Calculate cost based on token usage."""
        # Approximate costs (USD per 1K tokens) - update based on current pricing
        cost_per_1k = {
            "gpt-4": 0.03,
            "gpt-4-turbo": 0.01,
            "gpt-3.5-turbo": 0.002,
            "claude-3-opus": 0.015,
            "claude-3-sonnet": 0.003,
            "claude-3-haiku": 0.0005
        }
        
        base_model = model.split("-")[0] + "-" + model.split("-")[1] if "-" in model else model
        rate = cost_per_1k.get(base_model, 0.01)  # Default conservative estimate
        return (tokens / 1000) * rate

class OpenAIProvider(LLMProvider):
    """OpenAI provider implementation."""
    
    def _setup_client(self):
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI package not available. Install with: pip install openai")
        
        api_key = self.config.api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        
        self.client = openai.OpenAI(api_key=api_key)
    
    def generate(self, prompt: str, **kwargs) -> LLMResponse:
        """Generate response using OpenAI API."""
        start_time = time.time()
        prompt_hash = hashlib.md5(prompt.encode()).hexdigest()[:12]
        
        try:
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                timeout=self.config.timeout,
                **kwargs
            )
            
            content = response.choices[0].message.content
            tokens_used = response.usage.total_tokens
            cost = self._calculate_cost(tokens_used, self.config.model)
            response_time = time.time() - start_time
            
            # Check cost limit
            if cost > self.config.cost_limit_per_request:
                self.logger.warning(f"Cost ${cost:.4f} exceeds limit ${self.config.cost_limit_per_request}")
            
            return LLMResponse(
                content=content,
                provider="openai",
                model=self.config.model,
                tokens_used=tokens_used,
                cost_estimate=cost,
                response_time=response_time,
                timestamp=datetime.now().isoformat(),
                prompt_hash=prompt_hash
            )
            
        except Exception as e:
            self.logger.error(f"OpenAI generation failed: {e}")
            raise

class AnthropicProvider(LLMProvider):
    """Anthropic Claude provider implementation."""
    
    def _setup_client(self):
        if not ANTHROPIC_AVAILABLE:
            raise ImportError("Anthropic package not available. Install with: pip install anthropic")
        
        api_key = self.config.api_key or os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("Anthropic API key not found. Set ANTHROPIC_API_KEY environment variable.")
        
        self.client = anthropic.Anthropic(api_key=api_key)
    
    def generate(self, prompt: str, **kwargs) -> LLMResponse:
        """Generate response using Anthropic API."""
        start_time = time.time()
        prompt_hash = hashlib.md5(prompt.encode()).hexdigest()[:12]
        
        try:
            response = self.client.messages.create(
                model=self.config.model,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                messages=[{"role": "user", "content": prompt}],
                **kwargs
            )
            
            content = response.content[0].text
            tokens_used = response.usage.input_tokens + response.usage.output_tokens
            cost = self._calculate_cost(tokens_used, self.config.model)
            response_time = time.time() - start_time
            
            # Check cost limit
            if cost > self.config.cost_limit_per_request:
                self.logger.warning(f"Cost ${cost:.4f} exceeds limit ${self.config.cost_limit_per_request}")
            
            return LLMResponse(
                content=content,
                provider="anthropic",
                model=self.config.model,
                tokens_used=tokens_used,
                cost_estimate=cost,
                response_time=response_time,
                timestamp=datetime.now().isoformat(),
                prompt_hash=prompt_hash
            )
            
        except Exception as e:
            self.logger.error(f"Anthropic generation failed: {e}")
            raise

class LLMManager:
    """High-level manager for LLM operations with failover and caching."""
    
    def __init__(self, 
                 primary_config: LLMConfig,
                 fallback_config: Optional[LLMConfig] = None,
                 cache_responses: bool = True):
        self.primary_provider = self._create_provider(primary_config)
        self.fallback_provider = self._create_provider(fallback_config) if fallback_config else None
        self.cache_responses = cache_responses
        self.response_cache = {}
        self.usage_stats = {
            'total_requests': 0,
            'total_tokens': 0,
            'total_cost': 0.0,
            'provider_usage': {}
        }
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("llm_manager")
    
    def _create_provider(self, config: LLMConfig) -> LLMProvider:
        """Create provider instance based on config."""
        if config.provider == "openai":
            return OpenAIProvider(config)
        elif config.provider == "anthropic":
            return AnthropicProvider(config)
        else:
            raise ValueError(f"Unsupported provider: {config.provider}")
    
    def generate(self, prompt: str, use_cache: bool = True, **kwargs) -> LLMResponse:
        """Generate response with failover and caching."""
        prompt_hash = hashlib.md5(prompt.encode()).hexdigest()
        
        # Check cache first
        if use_cache and self.cache_responses and prompt_hash in self.response_cache:
            self.logger.info(f"Using cached response for prompt {prompt_hash[:8]}")
            return self.response_cache[prompt_hash]
        
        # Try primary provider
        try:
            response = self._generate_with_retry(self.primary_provider, prompt, **kwargs)
            self._update_stats(response)
            
            # Cache successful response
            if self.cache_responses:
                self.response_cache[prompt_hash] = response
            
            return response
            
        except Exception as e:
            self.logger.error(f"Primary provider failed: {e}")
            
            # Try fallback provider
            if self.fallback_provider:
                try:
                    self.logger.info("Attempting fallback provider")
                    response = self._generate_with_retry(self.fallback_provider, prompt, **kwargs)
                    self._update_stats(response)
                    
                    if self.cache_responses:
                        self.response_cache[prompt_hash] = response
                    
                    return response
                    
                except Exception as fallback_error:
                    self.logger.error(f"Fallback provider also failed: {fallback_error}")
                    raise
            else:
                raise
    
    def _generate_with_retry(self, provider: LLMProvider, prompt: str, **kwargs) -> LLMResponse:
        """Generate with retry logic."""
        last_exception = None
        
        for attempt in range(provider.config.retry_attempts):
            try:
                return provider.generate(prompt, **kwargs)
            except Exception as e:
                last_exception = e
                if attempt < provider.config.retry_attempts - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    self.logger.warning(f"Attempt {attempt + 1} failed, retrying in {wait_time}s: {e}")
                    time.sleep(wait_time)
                else:
                    self.logger.error(f"All {provider.config.retry_attempts} attempts failed")
        
        raise last_exception
    
    def _update_stats(self, response: LLMResponse):
        """Update usage statistics."""
        self.usage_stats['total_requests'] += 1
        self.usage_stats['total_tokens'] += response.tokens_used
        self.usage_stats['total_cost'] += response.cost_estimate
        
        provider = response.provider
        if provider not in self.usage_stats['provider_usage']:
            self.usage_stats['provider_usage'][provider] = {
                'requests': 0, 'tokens': 0, 'cost': 0.0
            }
        
        self.usage_stats['provider_usage'][provider]['requests'] += 1
        self.usage_stats['provider_usage'][provider]['tokens'] += response.tokens_used
        self.usage_stats['provider_usage'][provider]['cost'] += response.cost_estimate
    
    def get_usage_stats(self) -> Dict:
        """Get current usage statistics."""
        return self.usage_stats.copy()
    
    def save_usage_log(self, filepath: str):
        """Save usage statistics to file."""
        with open(filepath, 'w') as f:
            json.dump({
                'stats': self.usage_stats,
                'timestamp': datetime.now().isoformat()
            }, f, indent=2)

def create_default_manager() -> LLMManager:
    """Create a default LLM manager with sensible defaults."""
    
    # Try OpenAI first
    primary_config = LLMConfig(
        provider="openai",
        model="gpt-4-turbo",
        max_tokens=1000,
        temperature=0.7,
        cost_limit_per_request=0.05  # Conservative limit for MVP
    )
    
    # Only use fallback if Anthropic is available
    fallback_config = None
    try:
        import anthropic
        fallback_config = LLMConfig(
            provider="anthropic", 
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            temperature=0.7,
            cost_limit_per_request=0.05
        )
    except ImportError:
        print("💡 Using OpenAI only. Install anthropic for fallback: pip install anthropic")
    
    return LLMManager(primary_config, fallback_config)

# Usage example for testing
if __name__ == "__main__":
    print("🤖 Testing LLM Integration")
    print("=" * 40)
    
    try:
        manager = create_default_manager()
        
        test_prompt = """
        Convert this practical wisdom into a modern story:
        "Prioritize prayer and remembrance throughout the day for spiritual well-being."
        
        Create a 200-word story about a busy professional who discovers the power of 
        mindful moments during their workday. Make it universal and inspiring.
        """
        
        response = manager.generate(test_prompt)
        
        print(f"✅ Generated story ({response.tokens_used} tokens, ${response.cost_estimate:.4f})")
        print(f"Provider: {response.provider} - {response.model}")
        print(f"Content: {response.content[:100]}...")
        
        # Show usage stats
        stats = manager.get_usage_stats()
        print(f"\n📊 Usage Stats: {stats['total_requests']} requests, ${stats['total_cost']:.4f} total")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("💡 Make sure to set OPENAI_API_KEY or ANTHROPIC_API_KEY environment variable")
