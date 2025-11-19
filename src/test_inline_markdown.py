import re
import unittest

from textnode import TextNode, TextType
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images, 
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes
)

class TestInlineMarkdown(unittest.TestCase):
    def test_split_none(self):
        node = TextNode("This is text with no markup", TextType.TEXT)
        self.assertEqual(f'{split_nodes_delimiter([node], "`", TextType.CODE)}', "[TextNode('This is text with no markup', text)]")
        
    def test_split_empty(self):
        node = TextNode("Empty code block ``", TextType.TEXT)
        self.assertEqual(f'{split_nodes_delimiter([node], "`", TextType.CODE)}', "[TextNode('Empty code block ', text)]")

    def test_split_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        self.assertEqual(f'{split_nodes_delimiter([node], "**", TextType.BOLD)}', "[TextNode('This is text with a ', text), TextNode('bold', bold), TextNode(' word', text)]")

    def test_split_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        self.assertEqual(f'{split_nodes_delimiter([node], "_", TextType.ITALIC)}', "[TextNode('This is text with an ', text), TextNode('italic', italic), TextNode(' word', text)]")

    def test_split_code(self):
        node = TextNode("This is text with a ```code block``` in it", TextType.TEXT)
        self.assertEqual(f'{split_nodes_delimiter([node], "`", TextType.CODE)}', "[TextNode('This is text with a ', text), TextNode('code block', code), TextNode(' in it', text)]")

    def test_split_start(self):
        node = TextNode("`code block` at the start of the text", TextType.TEXT)
        self.assertEqual(f'{split_nodes_delimiter([node], "`", TextType.CODE)}', "[TextNode('code block', code), TextNode(' at the start of the text', text)]")

    def test_split_end(self):
        node = TextNode("Finish the text with a `code block`", TextType.TEXT)
        self.assertEqual(f'{split_nodes_delimiter([node], "`", TextType.CODE)}', "[TextNode('Finish the text with a ', text), TextNode('code block', code)]")

    def test_split_multiple(self):
        node = TextNode("Multiple code blocks `here` and `here`", TextType.TEXT)
        self.assertEqual(f'{split_nodes_delimiter([node], "`", TextType.CODE)}', "[TextNode('Multiple code blocks ', text), TextNode('here', code), TextNode(' and ', text), TextNode('here', code)]")

        node = TextNode("This is a _really_ **special** `code block`", TextType.TEXT)
        self.assertEqual(f'{split_nodes_delimiter(split_nodes_delimiter(split_nodes_delimiter([node], "`", TextType.CODE), "_", TextType.ITALIC), "**", TextType.BOLD)}', "[TextNode('This is a ', text), TextNode('really', italic), TextNode(' ', text), TextNode('special', bold), TextNode(' ', text), TextNode('code block', code)]")

    def test_extract_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.boot.dev) and another [second link](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_text_to_testnodes(self):
        new_nodes = text_to_textnodes(
            "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

if __name__ == "__main__":
    unittest.main()