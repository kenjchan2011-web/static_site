#from textnode import TextType

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag              # <p, a, h, ...>
        self.value = value          # 
        self.children = children    # HTMLNode object
        self.props = props          # Dictionary: {"href": "https://www.google.com"}

    def to_html(self):
        raise NotImplementedError("Error for now.")
        

    def props_to_html(self):
        if not self.props:
            return ""

        prop_string = ""
        if self.props is not None:
            if "href" in self.props:
                prop_string = f'href={self.props["href"]}'
            else:
                prop_string = ""

        for key in self.props:
            if key != "href":
                prop_string += f' {key}="{self.props[key]}"'

        return prop_string


    def __repr__(self):

        return (
            f"HTMLNode(tag={self.tag}, value={self.value}, "
            f"children={self.children}, {self.props_to_html()})"
        )


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value.")
        
        if not self.tag:
            return self.value

        if self.props_to_html() == "":
            return f"<{self.tag}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"


    def __repr__(self):
        #return f"LeafNode({self.tag}, {self.value}, {self.props})"
        if self.props_to_html() == "":
            if self.tag is None:
                return f"{self.value}"
            else:
                return f"<{self.tag}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)


    def to_html(self):

        if self.tag is None:
            raise ValueError("ParentNode must have a tag.")

        if self.children is None:
            raise ValueError("ParentNode must have children.")

        children_html = ""
        for child in self.children:
            children_html += child.to_html()

        if "href" in self.props_to_html():
            return f"<{self.tag} {self.props_to_html()}>{children_html}</{self.tag}>"
        else:
            return f"<{self.tag}>{children_html}</{self.tag}>"

    def __repr__(self):
        #return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
        return ParentNode(self.tag, self.children, self.props)
    
