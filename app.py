import os
import logging
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import google.generativeai as genai
from google.generativeai.types import GenerationConfig

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

@app.route('/')
def index():
    """Display the main API key testing form."""
    return render_template('index.html')

@app.route('/test-api-key', methods=['POST'])
def test_api_key():
    """Test the provided Gemini API key and return detailed results."""
    api_key = request.form.get('api_key', '').strip()
    
    # Basic input validation
    if not api_key:
        flash('Please provide an API key.', 'error')
        return redirect(url_for('index'))
    
    if len(api_key) < 30:  # Basic length check for API keys
        flash('API key appears to be too short. Please check and try again.', 'error')
        return redirect(url_for('index'))
    
    test_results = {
        'success': False,
        'api_key_masked': mask_api_key(api_key),
        'tests_performed': [],
        'error_message': None,
        'model_info': None
    }
    
    try:
        # Configure the API key
        genai.configure(api_key=api_key)
        test_results['tests_performed'].append('✓ API key configuration successful')
        
        # Test 1: List available models
        try:
            models = list(genai.list_models())
            test_results['tests_performed'].append(f'✓ Successfully retrieved {len(models)} available models')
            
            # Find a suitable generative model
            generative_models = [m for m in models if 'generateContent' in m.supported_generation_methods]
            if generative_models:
                model_name = generative_models[0].name
                test_results['model_info'] = {
                    'name': model_name,
                    'display_name': generative_models[0].display_name,
                    'description': getattr(generative_models[0], 'description', 'No description available')
                }
                test_results['tests_performed'].append(f'✓ Found suitable model: {generative_models[0].display_name}')
            else:
                test_results['tests_performed'].append('⚠ No generative models found')
                
        except Exception as e:
            test_results['tests_performed'].append(f'✗ Failed to list models: {str(e)}')
            raise e
        
        # Test 2: Simple generation test
        try:
            if generative_models:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(
                    "Hello! Please respond with 'API test successful' to confirm connectivity.",
                    generation_config=GenerationConfig(
                        max_output_tokens=50,
                        temperature=0.1
                    )
                )
                
                if response and response.text:
                    test_results['tests_performed'].append('✓ Successfully generated content')
                    test_results['tests_performed'].append(f'✓ Model response: "{response.text.strip()}"')
                else:
                    test_results['tests_performed'].append('⚠ Content generation returned empty response')
            else:
                test_results['tests_performed'].append('⚠ Skipped content generation test (no suitable models)')
                
        except Exception as e:
            test_results['tests_performed'].append(f'✗ Content generation failed: {str(e)}')
            # Don't raise here as this might be a quota/permission issue but key might still be valid
        
        # If we got this far, the API key is at least valid
        test_results['success'] = True
        flash('API key test completed successfully!', 'success')
        
    except Exception as e:
        error_msg = str(e)
        test_results['error_message'] = error_msg
        
        # Provide specific error messages for common issues
        if 'API_KEY_INVALID' in error_msg or 'invalid API key' in error_msg.lower():
            flash('Invalid API key. Please check your key and try again.', 'error')
        elif 'PERMISSION_DENIED' in error_msg:
            flash('Permission denied. Please check if your API key has the required permissions.', 'error')
        elif 'QUOTA_EXCEEDED' in error_msg:
            flash('API quota exceeded. Please check your usage limits.', 'error')
        elif 'timeout' in error_msg.lower() or 'connection' in error_msg.lower():
            flash('Network error. Please check your internet connection and try again.', 'error')
        else:
            flash(f'API test failed: {error_msg}', 'error')
        
        app.logger.error(f"API key test failed: {error_msg}")
    
    return render_template('index.html', test_results=test_results)

def mask_api_key(api_key):
    """Mask API key for display purposes, showing only first 8 and last 4 characters."""
    if len(api_key) <= 12:
        return '*' * len(api_key)
    return api_key[:8] + '*' * (len(api_key) - 12) + api_key[-4:]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
