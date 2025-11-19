import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a link node", TextType.LINK, "http://a@b.com")
        node2 = TextNode("This is a link node", TextType.LINK, "http://a@b.com")
        self.assertEqual(node, node2)

    def test_not_eq_text(self):
        # Check 'text' attribute
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_type(self):
        # Check 'text_type' attribute
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_eq_url(self):
        # Check 'url' attribute
        node = TextNode("This is a link node", TextType.LINK, "http://a@b.com")
        node2 = TextNode("This is a link node", TextType.LINK, "http://x@y.com")
        self.assertNotEqual(node, node2)

        # Check 'url' attribute (None)
        node = TextNode("This is a link node", TextType.LINK, "http://a@b.com")
        node2 = TextNode("This is a link node", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")
        self.assertEqual(html_node.to_html(), "<b>This is a bold text node</b>")

    def test_italic(self):
        node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")
        self.assertEqual(html_node.to_html(), "<i>This is an italic text node</i>")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")
        self.assertEqual(html_node.to_html(), "<code>This is a code node</code>")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "http://a@b.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertDictEqual(html_node.props, {"href" : "http://a@b.com"})
        self.assertEqual(html_node.to_html(), '<a href="http://a@b.com">This is a link node</a>')

    def test_img(self):
        node = TextNode("This is an img node", TextType.IMAGE, "http://a@b.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertDictEqual(html_node.props, {"alt" : "This is an img node", "src" : "http://a@b.com"})
        self.assertEqual(html_node.to_html(), '<img alt="This is an img node" src="http://a@b.com"/>')

if __name__ == "__main__":
    unittest.main()