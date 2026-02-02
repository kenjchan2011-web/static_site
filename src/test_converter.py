from platform import node
import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from converter import extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_node_to_html_node, text_to_textnodes, markdown_to_blocks, block_to_block_type, markdown_to_html_node, extract_title
from textnode import TextNode, TextType, BlockType


class TestHTMLNode(unittest.TestCase):

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")


    def test_bold_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.to_html(), "<b>This is a text node</b>")


    def test_bold_text(self):
        node = TextNode("This is a text node", TextType.LINK, "http://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.to_html(), "<a href=http://google.com>This is a text node</a>")


    # Ch3 - L4
    # Test cases for extract_markdown_images
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    # Test cases for extract_markdown_links
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.boot.dev)"
        )
        self.assertListEqual([("link", "https://www.boot.dev")], matches)

    # Ch3 - L5
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
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")
        ],
        new_nodes,
        )


    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.boot.dev) and [another link](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT), 
                TextNode("link", TextType.LINK, "https://www.boot.dev"), 
                TextNode(" and ", TextType.TEXT), 
                TextNode("another link", TextType.LINK, "https://www.youtube.com/@bootdotdev")
            ],
            new_nodes)

    # Ch3 - L6
    def test_text_to_textnodes(self):
        text_node = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")

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
                TextNode("link", TextType.LINK, "https://boot.dev")
            ],
            text_node,
        )

    def test_text_to_textnodes2(self):
        text_node = text_to_textnodes("This is **bold text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.test.com/testicon.jpeg) and a [link](http://google.com)")

        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT), 
                TextNode("bold text", TextType.BOLD), 
                TextNode(" with an ", TextType.TEXT), 
                TextNode("italic", TextType.ITALIC), 
                TextNode(" word and a ", TextType.TEXT), 
                TextNode("code block", TextType.CODE), 
                TextNode(" and an ", TextType.TEXT), 
                TextNode("obi wan image", TextType.IMAGE, "https://i.test.com/testicon.jpeg"), 
                TextNode(" and a ", TextType.TEXT), 
                TextNode("link", TextType.LINK, "http://google.com")
            ],
            text_node,
        )


    # Ch4 - L1
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
            ]
        )


    def test_markdown_to_blocks2(self):
        md = """
This is _italic_ paragraph

This is another paragraph with **bold** text and `code` here
This is the same paragraph on a new line
Additional line is added

- This is a list
- with items

- this is another block
"""
        
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is _italic_ paragraph",
                "This is another paragraph with **bold** text and `code` here\nThis is the same paragraph on a new line\nAdditional line is added",
                "- This is a list\n- with items",
                "- this is another block"
            ]
        )


    def test_heading(self):
        self.assertEqual(block_to_block_type("# heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### heading"), BlockType.HEADING)
        # False heading (no space)
        self.assertEqual(block_to_block_type("#heading"), BlockType.PARAGRAPH)


    def test_code(self):
        self.assertEqual(block_to_block_type("```code\nmore code```"), BlockType.CODE)
        # False code (missing closing backticks)
        self.assertEqual(block_to_block_type("```incomplete"), BlockType.PARAGRAPH)

    def test_quote(self):
        self.assertEqual(block_to_block_type("> line 1\n> line 2"), BlockType.QUOTE)
        # False quote (second line missing >)
        self.assertEqual(block_to_block_type("> line 1\nline 2"), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("- item 1\n- item 2"), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. first\n2. second\n3. third"), BlockType.ORDERED_LIST)
        # False order (skips a number)
        self.assertEqual(block_to_block_type("1. first\n3. third"), BlockType.PARAGRAPH)


    # Ch4 - L3
    def test_paragraphs(self):

        md="""
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
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


    def test_extract_title(self):
        md = "# First Title"
        #md = "## Second title"
        #md = "#      First Title"
        title = extract_title(md)
        self.assertEqual(
            title,
            'First Title'
        )

    def test_extract_title_with_extra_space(self):
        #md = "## Second title"
        md = "#      Extra Space Title"
        title = extract_title(md)
        self.assertEqual(
            title,
            'Extra Space Title'
        )


if __name__ == "__main__":
    unittest.main()