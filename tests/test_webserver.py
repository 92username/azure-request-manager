import unittest
import json
import os
import sys
import tempfile
from unittest.mock import patch, MagicMock

# Add parent directory to path to import webserver
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import webserver

class TestWebserver(unittest.TestCase):
    
    def setUp(self):
        # Create a temporary file for testing config operations
        self.temp_config = tempfile.NamedTemporaryFile(delete=False)
        self.temp_config_path = self.temp_config.name
        # Write default config to temp file
        default_config = {
            "api_url": "https://test.com/api",
            "interval_seconds": 30,
            "failure_rate": 10,
            "failure_modes": ["timeout", "500"]
        }
        with open(self.temp_config_path, 'w') as f:
            json.dump(default_config, f)
        
        # Setup test client
        webserver.app.config['TESTING'] = True
        self.client = webserver.app.test_client()
        
    def tearDown(self):
        # Remove the temporary file
        os.unlink(self.temp_config_path)
    
    @patch('webserver.CONFIG_PATH')
    def test_load_config(self, mock_path):
        # Redirect config path to our temp file
        mock_path.return_value = self.temp_config_path
        
        # Test loading the config
        config = webserver.load_config()
        self.assertEqual(config['api_url'], 'https://test.com/api')
        self.assertEqual(config['interval_seconds'], 30)
        self.assertEqual(config['failure_rate'], 10)
        self.assertEqual(config['failure_modes'], ['timeout', '500'])
    
    @patch('webserver.CONFIG_PATH')
    def test_save_config(self, mock_path):
        # Redirect config path to our temp file
        mock_path.return_value = self.temp_config_path
        
        # Test saving a new config
        new_config = {
            "api_url": "https://updated.com/api",
            "interval_seconds": 60,
            "failure_rate": 20,
            "failure_modes": ["timeout"]
        }
        result = webserver.save_config(new_config)
        self.assertTrue(result)
        
        # Verify the config was saved correctly
        with open(self.temp_config_path, 'r') as f:
            saved_config = json.load(f)
        self.assertEqual(saved_config['api_url'], 'https://updated.com/api')
        self.assertEqual(saved_config['interval_seconds'], 60)
        self.assertEqual(saved_config['failure_rate'], 20)
        self.assertEqual(saved_config['failure_modes'], ['timeout'])

    @patch('webserver.render_template')
    @patch('webserver.load_config')
    def test_index_route(self, mock_load_config, mock_render_template):
        # Setup mock return values
        mock_config = {"api_url": "https://test.com/api"}
        mock_load_config.return_value = mock_config
        mock_render_template.return_value = "Mock HTML"
        
        # Test the index route
        response = self.client.get('/')
        mock_render_template.assert_called_once_with('index.html', config=mock_config)

if __name__ == '__main__':
    unittest.main()