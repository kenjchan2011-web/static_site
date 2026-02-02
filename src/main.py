#from textnode import TextNode, TextType
#from htmlnode import HTMLNode, LeafNode, ParentNode
from platform import node
from matplotlib import text
#from textnode import TextNode, TextType
#from converter import extract_markdown_images, extract_markdown_links, split_nodes_image, text_node_to_html_node, split_nodes_delimiter, split_nodes_link, text_to_textnodes, markdown_to_blocks, block_to_block_type, markdown_to_html_node
#import converter

from converter import extract_title, generate_page, generate_pages_recursive
from update import build_page, refresh_environment

def main():

    #SOURCE_PATH = "content/index.md"
    #TEMPLATE_PATH = "template.html"
    #DESTINATION_PATH = "public/index.html"

    source_dir = "/home/kenjc/development/projects/static_site_generator/static_site/content"
    dest_dir = "/home/kenjc/development/projects/static_site_generator/static_site/static"
    template_path = "/home/kenjc/development/projects/static_site_generator/static_site/template.html"

    #build_page()
    generate_pages_recursive(source_dir, template_path, dest_dir)
    refresh_environment()



    #node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    #props = {"href": "https://www.boot.dev"}
    #html_node = HTMLNode("a", "Test", None, props)
    
    #html_node = HTMLNode("a", "Test", None, props)
    #leaf_node = LeafNode("p", "This is a paragraph of text.").to_html()
    #leaf_node = LeafNode("a", "Click me!", {"href": "https://www.google.com"}).to_html()


    #child_node = LeafNode("span", "child")
    #parent_node = ParentNode("div", [child_node]).to_html()

    #node = ParentNode(
    #    "p",
    #    [
    #        LeafNode("b", "Bold text"),
    #        LeafNode(None, "Normal text"),
    #        LeafNode("i", "italic text"),
    #        LeafNode(None, "Normal text"),
    #    ],
    #)
    
    #node = TextNode("This is a text node", TextType.LINK, "http://google.com")
    #html_node = text_node_to_html_node(node)
    #print(html_node.tag)
    #print(html_node.to_html())

    #node = TextNode("This is text with a `code block` word", TextType.TEXT)
    #new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

    #node = TextNode("This is text with a **bold style** word", TextType.TEXT)
    #new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

    #node = TextNode("This is text with a _italic style_ word", TextType.TEXT)
    #new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)

    #node = TextNode("This is text with a _italic style word", TextType.TEXT)
    #new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
    #print(new_nodes)

    # Ch3 - L4
    #text = "![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    #print(extract_markdown_images(text))

    #text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    #print(extract_markdown_links(text)) 
    
    # Ch3 - L5
    #node = TextNode(
    #    "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
    #    TextType.TEXT,
    #)
    #new_nodes = split_nodes_link([node])
    #print(new_nodes)

    #node = TextNode(
    #    "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
    #    TextType.TEXT,
    #)
    #new_nodes = split_nodes_image([node])
    #print(new_nodes)
    
    # Ch3 - L6
    #node = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
    #print(node)

    # Ch4 - L1
#    md = """
#This is **bolded** paragraph

#This is another paragraph with _italic_ text and `code` here
#This is the same paragraph on a new line

#- This is a list
#- with items
#"""
#    blocks = markdown_to_blocks(md)
#    print(blocks)

    #Ch4 - L1
    #md = ">This is the same paragraph on a new line<"
    #code_type = block_to_block_type(md)
    #print(code_type)

    # Ch4 - L3
    #md = """
#This is **bolded** paragraph
#text in a p
#tag here

#This is another paragraph with _italic_ text and `code` here

#"""

#    md = """
#```
#This is text that _should_ remain
#the **same** even with inline stuff
#```
#"""
#    node = markdown_to_html_node(md)
#    #print(node)
#    html = node.to_html()
#    print(html)
    #self.assertEqual(
    #    html,
    #    "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    #)

    #print(html)

if __name__ == "__main__":
    main()
