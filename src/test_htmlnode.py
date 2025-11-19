import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode()
        self.assertEqual(f'{node}', 'HTMLNode {\n  tag: None\n  value: None\n  children: None\n  props: None\n}')

        node1 = HTMLNode("p", "This is some text")
        self.assertEqual(f'{node1}', 'HTMLNode {\n  tag: "p"\n  value: "This is some text"\n  children: None\n  props: None\n}')
        
        node2 = HTMLNode("p", "This is some text with children", [node, node1])
        self.assertEqual(f'{node2}', 'HTMLNode {\n  tag: "p"\n  value: "This is some text with children"\n  children: [\n    HTMLNode {\n      tag: None\n      value: None\n      children: None\n      props: None\n    },\n    HTMLNode {\n      tag: "p"\n      value: "This is some text"\n      children: None\n      props: None\n    },\n  ]\n  props: None\n}')
        
        node3 = HTMLNode("p", "This is some text with props", None, {"a":"b", "c":"d"})
        self.assertEqual(f'{node3}', 'HTMLNode {\n  tag: "p"\n  value: "This is some text with props"\n  children: None\n  props: {\n    a: "b",\n    c: "d",\n  }\n}')
        
        node4 = HTMLNode("p", "This is some text with nested", [node2, node3], {"a":"b", "c":"d"})
        self.assertEqual(f'{node4}', 'HTMLNode {\n  tag: "p"\n  value: "This is some text with nested"\n  children: [\n    HTMLNode {\n      tag: "p"\n      value: "This is some text with children"\n      children: [\n        HTMLNode {\n          tag: None\n          value: None\n          children: None\n          props: None\n        },\n        HTMLNode {\n          tag: "p"\n          value: "This is some text"\n          children: None\n          props: None\n        },\n      ]\n      props: None\n    },\n    HTMLNode {\n      tag: "p"\n      value: "This is some text with props"\n      children: None\n      props: {\n        a: "b",\n        c: "d",\n      }\n    },\n  ]\n  props: {\n    a: "b",\n    c: "d",\n  }\n}')


if __name__ == "__main__":
    unittest.main()