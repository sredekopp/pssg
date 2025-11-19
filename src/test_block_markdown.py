import unittest

from block_markdown import (
    BlockType,
    markdown_to_html_node,
    markdown_to_blocks,
    block_to_block_type,
    extract_title
)

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type(self):
        md = """
# This is a heading paragraph

## This is a second heading

This is paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

```
# code block to check markdown types
types = []
for block in markdown_to_blocks(md):
    types.append(block_to_block_type(block))
print(types)
```

- This is an unordered list
- with items

1. This is an ordered list
2. with items
"""
        block_types = []
        for block in markdown_to_blocks(md):
            block_types.append(block_to_block_type(block))
        self.assertListEqual(
            [
                BlockType.HEADING,
                BlockType.HEADING,
                BlockType.PARAGRAPH,
                BlockType.CODE,
                BlockType.ULIST,
                BlockType.OLIST
            ],
            block_types
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_blockquote(self):
        md = """
> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><blockquote>"I am in fact a Hobbit in all but size."  -- J.R.R. Tolkien</blockquote></div>',
        )

    def test_extract_title(self):
        md = """
.# This is not a heading
## This is a second heading
### This is a third heading
#### This is a fourth heading
##### This is a fifth heading
###### This is a sixth heading

This is paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

```
# code block to check markdown types
types = []
for block in markdown_to_blocks(md):
    types.append(block_to_block_type(block))
print(types)
```

- This is an unordered list
- with items

1. This is an ordered list
2. with items

# This is a level 1 heading paragraph
"""
        self.assertEqual(
            extract_title(md),
            "This is a level 1 heading paragraph",
        )
