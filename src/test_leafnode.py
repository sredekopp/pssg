import unittest

from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("p", "This is some html text")
        self.assertEqual(f'{node.to_html()}', '<p>This is some html text</p>')
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(f'{node.to_html()}', '<a href="https://www.google.com">Click me!</a>')

if __name__ == "__main__":
    unittest.main()