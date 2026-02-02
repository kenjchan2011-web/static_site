import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):

        #self.tag = tag              # <p, a, h, ...>
        #self.value = value          # 
        #self.children = children    # HTMLNode object
        #self.props = props          # Dictionary: {"href": "https://www.google.com"}


    def test_node_a(self):
        props = {"href":"http://google", "alt":"google", "target": "_blank"}
        html_content = HTMLNode( "a", "google", None , props)
        self.assertIn("google", html_content.props["alt"])

    def test_node_p(self):
        props = {"style": "color:red"}
        html_content = HTMLNode( "p", "Colot text", None , props)
        self.assertIn("red", html_content.props["style"])

    def test_node_table(self):
        props = {"border": 0}
        html_content = HTMLNode( "table", "Table border", "<tr>" , props)
        self.assertEqual(0, html_content.props["border"])


    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href=https://www.google.com>Click me!</a>')


    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

if __name__ == "__main__":
    unittest.main()