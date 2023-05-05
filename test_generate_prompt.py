import unittest
from app import generate_prompt

class TestGeneratePrompt(unittest.TestCase):

    def test_generate_prompt_case_1(self):
        locations = ["Tel Aviv"]
        nights = ["3"]
        neighborhoods = ["Old North"]
        travel_desires = ["Museums", "Hanging out on the beach"]

        prompt = generate_prompt(locations, nights, neighborhoods, travel_desires)
        self.assertIn("Tel Aviv", prompt)
        self.assertIn("3", prompt)
        self.assertIn("Old North", prompt)

    def test_generate_prompt_case_2(self):
        locations = ["Tel Aviv", "Miami"]
        nights = ["2", "3"]
        neighborhoods = ["Old North", "South Beach"]
        travel_desires = ["Museums", "Hanging out on the beach"]

        prompt = generate_prompt(locations, nights, neighborhoods, travel_desires)
        self.assertIn("Tel Aviv", prompt)
        self.assertIn("2", prompt)
        self.assertIn("Old North", prompt)
        self.assertIn("Miami", prompt)
        self.assertIn("3", prompt)
        self.assertIn("South Beach", prompt)

    def test_generate_prompt_case_3(self):
        locations = ["Tel Aviv", "Miami", "New York"]
        nights = ["2", "3", "4"]
        neighborhoods = ["Old North", "South Beach", "Manhattan"]
        travel_desires = ["Museums", "Hanging out on the beach", "Trying local food"]

        prompt = generate_prompt(locations, nights, neighborhoods, travel_desires)
        self.assertIn("Tel Aviv", prompt)
        self.assertIn("2", prompt)
        self.assertIn("Old North", prompt)
        self.assertIn("Miami", prompt)
        self.assertIn("3", prompt)
        self.assertIn("South Beach", prompt)
        self.assertIn("New York", prompt)
        self.assertIn("4", prompt)
        self.assertIn("Manhattan", prompt)

    def test_generate_prompt_case_4(self):
        locations = ["Tel Aviv", "Miami"]
        nights = ["2", "3"]
        neighborhoods = ["Old North", ""]
        travel_desires = ["Museums", "Hanging out on the beach"]

        prompt = generate_prompt(locations, nights, neighborhoods, travel_desires)
        self.assertIn("Tel Aviv", prompt)
        self.assertIn("2", prompt)
        self.assertIn("Old North", prompt)
        self.assertIn("Miami", prompt)
        self.assertIn("3", prompt)
        self.assertNotIn("South Beach", prompt)

if __name__ == '__main__':
    unittest.main()