import unittest
from unittest.mock import patch, MagicMock
import json
import requests  # Ensure the requests module is imported
from main import get_course_information

class TestGetCourseInformation(unittest.TestCase):
    
    @patch('requests.get')
    def test_get_course_information_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'apiResponse': {
                'response': {
                    'classes': [
                        {
                            'displayName': '2024 Spring COMPSCI 189 001',
                            'course': {
                                'subjectArea': {
                                    'description': 'Computer Science'
                                }
                            },
                            'aggregateEnrollmentStatus': {
                                'enrolledCount': 704
                            }
                        }
                    ]
                }
            }
        }
        mock_get.return_value = mock_response
        
        result = get_course_information(2242, 'compsci189')
        result_dict = json.loads(result)
        
        self.assertEqual(result_dict['display_name'], '2024 Spring COMPSCI 189 001')
        self.assertEqual(result_dict['department'], 'Computer Science')
        self.assertEqual(result_dict['enrollment_count'], 704)

    @patch('requests.get')
    def test_get_course_information_failure(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Client Error: Not Found for url")
        mock_get.return_value = mock_response

        result = get_course_information(2242, 'data8')
        result_dict = json.loads(result)
        
        self.assertTrue('Failed to retrieve data for data8' in result_dict)

if __name__ == '__main__':
    unittest.main()
