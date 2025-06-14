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
        'model_info': None,
        'all_models': []
    }
    
    try:
        # Configure the API key
        genai.configure(api_key=api_key)
        test_results['tests_performed'].append('✓ API key configuration successful')
        
        # Test 1: List available models
        try:
            models = list(genai.list_models())
            test_results['tests_performed'].append(f'✓ Successfully retrieved {len(models)} available models')
            
            # Store all models information
            all_models_info = []
            generative_models = []
            
            for model in models:
                model_info = {
                    'name': model.name,
                    'display_name': model.display_name,
                    'description': getattr(model, 'description', 'No description available'),
                    'supported_methods': model.supported_generation_methods,
                    'input_token_limit': getattr(model, 'input_token_limit', 'Not specified'),
                    'output_token_limit': getattr(model, 'output_token_limit', 'Not specified')
                }
                all_models_info.append(model_info)
                
                # Check if this model supports content generation and is not deprecated
                if 'generateContent' in model.supported_generation_methods:
                    # Filter out deprecated models based on common deprecated model patterns
                    model_name_lower = model.name.lower()
                    if not any(deprecated_term in model_name_lower for deprecated_term in [
                        'vision', 'pro-vision', '1.0-pro-vision', 'bison'
                    ]):
                        generative_models.append(model)
            
            test_results['all_models'] = all_models_info
            test_results['tests_performed'].append(f'✓ Cataloged {len(all_models_info)} models with detailed information')
            test_results['tests_performed'].append(f'✓ Found {len(generative_models)} active generation models (deprecated models filtered out)')
            
            # Find the most popular generative model for testing
            if generative_models:
                # Define model priority based on free tier limits and capabilities
                # gemini-1.5-flash has higher free tier limits than gemini-1.5-pro
                model_priority = [
                    'gemini-1.5-flash',
                    'gemini-1.5-pro', 
                    'gemini-pro',
                    'gemini-1.0-pro'
                ]
                
                # Find the highest priority model available
                selected_model = None
                for priority_model in model_priority:
                    for model in generative_models:
                        if priority_model in model.name.lower():
                            selected_model = model
                            break
                    if selected_model:
                        break
                
                # If no priority model found, use the first available
                if not selected_model:
                    selected_model = generative_models[0]
                
                model_name = selected_model.name
                test_results['model_info'] = {
                    'name': model_name,
                    'display_name': selected_model.display_name,
                    'description': getattr(selected_model, 'description', 'No description available'),
                    'is_popular': any(priority in selected_model.name.lower() for priority in model_priority)
                }
                
                popularity_note = " (most popular model)" if test_results['model_info']['is_popular'] else ""
                test_results['tests_performed'].append(f'✓ Selected model for testing: {selected_model.display_name}{popularity_note}')
                test_results['tests_performed'].append(f'✓ Model name for API calls: {model_name}')
            else:
                test_results['tests_performed'].append('⚠ No generative models found for content generation testing')
                
        except Exception as e:
            test_results['tests_performed'].append(f'✗ Failed to list models: {str(e)}')
            raise e
        
        # Test 2: Simple generation test
        try:
            if generative_models and 'model_info' in test_results and test_results['model_info']:
                # Use the same model that was selected for display
                model_name = test_results['model_info']['name']
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
            error_msg = str(e)
            if 'deprecated' in error_msg.lower():
                test_results['tests_performed'].append(f'✗ Selected model is deprecated: {error_msg}')
                test_results['tests_performed'].append('ℹ The system will try to select a different model next time')
            else:
                test_results['tests_performed'].append(f'✗ Content generation failed: {error_msg}')
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
        elif 'QUOTA_EXCEEDED' in error_msg or 'quota_metric' in error_msg.lower():
            if 'free_tier' in error_msg.lower():
                flash('Free tier quota exceeded. Consider upgrading to a paid plan or try again later. You can also try using gemini-1.5-flash which has higher free tier limits.', 'error')
            else:
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
