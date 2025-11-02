import sys
sys.path.append('.')
from lib.translators.natural_translator import NaturalTranslator
import json

# Create translator
t = NaturalTranslator()

# Sample story
maya_story = {
    'title': 'Seeing Signs: A Journey to Inner Strength', 
    'description': 'Discover how everyday challenges reveal unexpected paths to growth.', 
    'story_content': "Imagine you're about to miss an important interview because your car won't start. Meet Maya, a software developer who discovers inner strength through unexpected setbacks."
}

# Translate to Urdu
result = t.translate_story(maya_story, 'ur')

print('🎉 Enhanced Urdu Translation Sample:')
print('=' * 50)
print('📝 Title:', result['title'])
print('📺 YouTube Title:', result['youtube_title']) 
print('📝 Script Length:', len(result['script']), 'characters')
print('🌍 Cultural Adaptations:', result.get('cultural_adaptations', 'None')[:150] + '...')
print('📊 Readability Score:', result.get('readability_score', 'N/A'))
print('⏱️ Estimated Duration:', result.get('estimated_duration', 'N/A'), 'seconds')
print('💰 Translation Cost: $' + str(result['translation_metadata']['estimated_cost']))