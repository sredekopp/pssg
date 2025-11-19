import re

from enum import Enum
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import ParentNode, LeafNode, append_child

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING   = "heading"
    CODE      = "code"
    QUOTE     = "quote"
    ULIST     = "unordered_list"
    OLIST     = "ordered_list"

def markdown_to_html_node(markdown):
    block_nodes = []
    
    for block in markdown_to_blocks(markdown):
        block_type = block_to_block_type(block)
        
        match block_type:
            case BlockType.PARAGRAPH:
                block_nodes.append(
                    process_block("p", block))

            case BlockType.HEADING:
                # strip leading '#'s, returns tuple: (level, stripped_text)
                heading_info = prepare_heading(block)
                block_nodes.append(
                    process_block(f"h{heading_info[0]}", heading_info[1]))
            
            case BlockType.CODE:
                block_nodes.append(
                    process_code(block))
            
            case BlockType.QUOTE:
                # remove leading '>'s
                prepared_quote = prepare_quote(block) 
                block_nodes.append(
                    process_block("blockquote", prepared_quote))
            
            case BlockType.OLIST:
                block_nodes.append(
                    process_list("ol", r'^(\d+\.\s)', block))
            
            case BlockType.ULIST:
                block_nodes.append(
                    process_list("ul", r'^(-\s)', block))
    
    return ParentNode("div", block_nodes)

def prepare_heading(block):
    match = re.match(r'^(#{1,6})\s', block)
    heading_level = len(match.groups()[0])
    return (heading_level, block[heading_level+1:])

def prepare_quote(block):
    formatted_lines = [] 
    lines = block.split("\n")
    for line in lines:
        if line.startswith(">"):
            formatted_lines.append(line[1:].strip())
        else:
            formatted_lines.append(line)
    return " ".join(formatted_lines)

def process_block(block_tag, block):
    lines = block.split("\n")
    formatted_block = " ".join(lines)
    return ParentNode(block_tag, process_text(formatted_block))

def process_code(block):
    code = block[4:-3]
    return ParentNode('pre', [text_node_to_html_node(TextNode(code, TextType.CODE))])

def process_list(list_tag, pattern, block):
    item_nodes = []
    for item_text in prepare_list_items(pattern, block):
        item_nodes.append(ParentNode("li", process_text(item_text)))
    return ParentNode(list_tag, item_nodes)

def process_text(text):
    nodes = []
    for node in text_to_textnodes(text):
        nodes.append(text_node_to_html_node(node))
    return nodes
    
def prepare_list_items(pattern, block):
    list_items = []
    for line in block.split("\n"):
        match = re.match(pattern, line)
        if match:
            list_items.append(line[len(match.groups()[0]):])
        else:
            list_items.append(line)
    return list_items

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        filtered_block = block.strip()
        filtered_blocks.append(filtered_block)
    return filtered_blocks

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH

def extract_title(markdown):
    for block in markdown_to_blocks(markdown):
        if block_to_block_type(block) == BlockType.HEADING:
            heading_info = prepare_heading(block)
            if heading_info[0] == 1:
                return block[1:].strip()