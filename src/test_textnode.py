import unittest

from textnode import TextNode, TextType
from converter import split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    #NORMAL = "normal"
    #BOLD = "bold"
    #ITALIC = "italic"
    #CODE = "code"
    #LINK = "link"
    #IMAGE = "image"

    def test_eq_normal(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(node, node2)

    def test_not_eq_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_link_diff(self):
        node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("This is some anchor text", TextType.LINK, "https://yahoo.com")
        self.assertNotEqual(node, node2)


    def test_split_nodes_delimiter_code(self):
        index = 0
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        #result = ['TextNode(This is text with a , TextType.TEXT)', 'TextNode(code block, TextType.CODE)', 'TextNode( word, TextType.TEXT)']
        result = [TextNode('This is text with a ', TextType.TEXT), TextNode('code block', TextType.CODE), TextNode(' word', TextType.TEXT)]
        
        for node in new_nodes:
            self.assertEqual(new_nodes[index], result[index])


    def test_split_nodes_delimiter_bold(self):
        index = 0
        node = TextNode("This is text with a **bold style** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        #result = ['TextNode(This is text with a , TextType.TEXT)', 'TextNode(bold style, TextType.BOLD)', 'TextNode( word, TextType.TEXT)']
        result = [TextNode('This is text with a ', TextType.TEXT), TextNode('bold style', TextType.BOLD), TextNode( 'word', TextType.TEXT)]
        
        for node in new_nodes:
            self.assertEqual(new_nodes[index], result[index])


    def test_split_nodes_delimiter_italic(self):
        index = 0
        node = TextNode("This is text with a _italic style_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        #result = ['TextNode(This is text with a , TextType.TEXT)', 'TextNode(italic style, TextType.BOLD)', 'TextNode( word, TextType.TEXT)']
        result = [TextNode('This is text with a ', TextType.TEXT), TextNode('italic style', TextType.BOLD), TextNode(' word', TextType.TEXT)]
        
        for node in new_nodes:
            self.assertEqual(new_nodes[index], result[index])


if __name__ == "__main__":
    unittest.main()