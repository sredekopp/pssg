import unittest

from htmlnode import LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(f'{parent_node.to_html()}', '<div><span>child</span></div>')

        grandchild_node = LeafNode("b", "grandchild",  {"class": "c"})
        child_node = ParentNode("span", [grandchild_node],  {"class": "b"})
        parent_node = ParentNode("div", [child_node], {"class": "a"})
        self.assertEqual(f'{parent_node.to_html()}', '<div class="a"><span class="b"><b class="c">grandchild</b></span></div>')

if __name__ == "__main__":
    unittest.main()