"""
Test Cases for Counter Web Service
"""
from unittest import TestCase
import status
from counter import app

class CounterTest(TestCase):
    """Test Cases for Counter Web Service"""

    def setUp(self):
        self.client = app.test_client()

    def test_create_a_counter(self):
        """It should create a counter"""
        result = self.client.post("/counters/foo")
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        data = result.get_json()
        self.assertIn("foo", data)
        self.assertEqual(data["foo"], 0)

    def test_duplicate_counter(self):
        """It should return an error for duplicates"""
        result = self.client.post("/counters/bar")
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        
        result = self.client.post("/counters/bar")
        self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)

    def test_update_a_counter(self):
        """It should update the counter's value by 1"""
        result = self.client.post("/counters/baz")
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

        data = result.get_json()
        counter_value = data["baz"]
        result = self.client.put("/counters/baz")
        self.assertEqual(result.status_code, status.HTTP_200_OK)

        data = result.get_json()
        self.assertEqual(data["baz"], counter_value + 1)

        result = self.client.put("/counters/xdlol")
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)

    def test_read_a_counter(self):
        """It should read a counter's value"""
        result = self.client.post("/counters/hi")
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

        result = self.client.get("/counters/hi")
        self.assertEqual(result.status_code, status.HTTP_200_OK)

        data = result.get_json()
        self.assertEqual(data["hi"], 0)

        result = self.client.get("/counters/lol")
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)

        for _ in range(5):
            result = self.client.put("/counters/hi")
        data = result.get_json()
        self.assertEqual(data["hi"], 5)

    def test_delete_a_counter(self):
        """It should delete a counter"""
        result = self.client.post("/counters/bye")
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

        result = self.client.delete("/counters/bye")
        self.assertEqual(result.status_code, status.HTTP_204_NO_CONTENT)

        result = self.client.delete("/counters/xd")
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)

    
