from os import link
from htmlnode import LeafNode, ParentNode
from textnode import TextType, TextNode, BlockType
import re, sys, os


def text_node_to_html_node(text_node):
    # Determine the conversion based on the text_type enum
    match text_node.text_type:
        case TextType.TEXT | TextType.NORMAL:
            # No tag, just raw text
            return LeafNode(None, text_node.text)
            
        case TextType.BOLD:
            # <b> tag
            return LeafNode("b", text_node.text)
            
        case TextType.ITALIC:
            # <i> tag
            return LeafNode("i", text_node.text)
            
        case TextType.CODE:
            # <code> tag
            return LeafNode("code", text_node.text)
            
        case TextType.LINK:
            # <a> tag with href prop. text_node.text is the anchor text.
            return LeafNode("a", text_node.text, {"href": text_node.url})
            
        case TextType.IMAGE:
            # <img> tag. text_node.text is the alt text, text_node.url is the src.
            # Value is an empty string as <img> is self-closing.
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
            
        case _:
            # If the type doesn't match any of the above, it's invalid
            raise Exception(f"Unsupported TextType: {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):

    '''
        The beauty of this function is that it will take care of inline code, bold, and italic text, all in one! 
        The logic is identical, the delimiter and matching text_type are the only thing that changes, 
        e.g. 
            ** for bold, 
            _ for italic, and 
            a backtick for code. 
        Also, because it operates on an input list, 
        we can call it multiple times to handle different types of delimiters. 
        The order in which you check for different delimiters matters, 
        which actually simplifies implementation.
    '''
    new_node = []
    # If an "old node" is not a TextType.TEXT type, just add it to the new list as-is, 
    #   we only attempt to split "text" type objects (not bold, italic, etc).
    for node in old_nodes:
        # We only split TEXT nodes; if it's already CODE or BOLD, skip it
        if node.text_type != TextType.TEXT:
            new_node.append(node)
            continue
            
        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise Exception("that's invalid Markdown syntax.")

        for i in range(len(parts)):
            if parts[i] == "":
                continue
            
            if i % 2 == 0:
                new_node.append(TextNode(parts[i], TextType.TEXT))
            else:
                new_node.append(TextNode(parts[i], text_type))

    return new_node

    # If a matching closing delimiter is not found, just raise an exception with a helpful error message, 
    #   that's invalid Markdown syntax.
    # The .split() string method was useful
    # The .extend() list method was useful

def extract_markdown_images(text):
    '''
        Create a similar function extract_markdown_links(text) that extracts markdown links instead of images. 
        It should return tuples of anchor text and URLs. For example:
        
        text = "This is text with a link [to boot dev](https://www.boot.dev) 
            and [to youtube](https://www.youtube.com/@bootdotdev)"
        print(extract_markdown_links(text))

        # Output
        # [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        '''

    pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    matches = re.findall(pattern, text)

    return matches

def extract_markdown_links(text):
    '''
        Given a string of text, extract all markdown link syntaxes [link text](url)
        and return a list of tuples (link_text, url).

        text = "This is text with a [Google](https://www.google.com) and [Boot.dev](https://www.boot.dev)"
        print(extract_markdown_links(text))
        # [("Google", "https://www.google.com"), ("Boot.dev", "https://www.boot.dev")]
        '''

    pattern = r'(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)'
    matches = re.findall(pattern, text)

    return matches

def split_nodes_image(old_nodes):

    new_nodes = []
    for node in old_nodes:
        # We only split TEXT nodes; if it's already CODE or BOLD, skip it
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        original_text = node.text
        images = extract_markdown_images(original_text)

        if len(images) == 0:
            new_nodes.append(node)
            continue

        for image in images:

            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)

            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0]:
                #new_nodes.append(f'TextNode("{sections[0]}", {TextType.TEXT})')
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            #new_nodes.append(f'TextNode("{image[0]}", {TextType.IMAGE}, "{image[1]}")')
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            original_text = sections[1]

        if original_text:
            #new_nodes.append(f'TextNode("{original_text}", {TextType.TEXT})')
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        # We only split TEXT nodes; if it's already CODE or BOLD, skip it
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        original_text = node.text
        links = extract_markdown_links(original_text)

        if len(links) == 0:
            new_nodes.append(node)
            continue

        for link in links:

            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)

            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")

            if sections[0]:
                #new_nodes.append(f'TextNode("{sections[0]}", {TextType.TEXT})')
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            #new_nodes.append(f'TextNode("{link[0]}", {TextType.LINK}, "{link[1]}")')
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))

            original_text = sections[1]

        if original_text:
            #new_nodes.append(f'TextNode("{original_text}", {TextType.TEXT})')
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    # text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")

    # output
    # [
    #   TextNode("This is ", TextType.TEXT),
    #    TextNode("text", TextType.BOLD),
    #    TextNode(" with an ", TextType.TEXT),
    #    TextNode("italic", TextType.ITALIC),
    #    TextNode(" word and a ", TextType.TEXT),
    #    TextNode("code block", TextType.CODE),
    #    TextNode(" and an ", TextType.TEXT),
    #    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
    #    TextNode(" and a ", TextType.TEXT),
    #    TextNode("link", TextType.LINK, "https://boot.dev"),
    # ]
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    
    return nodes

def markdown_to_blocks(markdown):

    blocks = markdown.split("\n\n")
    new_blocks = []
    for block in blocks:
        stripped_block = block.strip()
        if stripped_block:
            new_blocks.append(stripped_block)

    return new_blocks

def block_to_block_type(block):
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    

    if block.startswith('>'):
        lines = block.split("\n")
        if all(line.startswith(">") for line in lines):
            return BlockType.QUOTE
    
    if block.startswith('- '):
        lines = block.split("\n")
        if all(line.startswith("-") for line in lines):
            return BlockType.UNORDERED_LIST
    
    if block.startswith('1.'):
        lines = block.split("\n")
        is_ordered = True
        for i in range(len(lines)):
            if not lines[i].startswith(f"{i + 1}. "):
                return BlockType.PARAGRAPH

        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):

    blocks = markdown_to_blocks(markdown)
    #blocks = markdown.split("\n\n")
    block_nodes = []

    # Determine the type of block (you already have a function for this)
    for block in blocks:
        
        html_node = block_to_html_node(block)
        block_nodes.append(html_node)

    return ParentNode("div", block_nodes)



def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []

    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)

    return children 

def block_to_html_node(block):
    block_type = block_to_block_type(block)

    if block_type == BlockType.HEADING:
        return heading_to_node(block)
    if block_type == BlockType.CODE:
        return code_to_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ul_to_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return ol_to_node(block)
    
    return paragraph_to_node(block)
    
def paragraph_to_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    # Applied strip() function
    children = text_to_children(paragraph.strip())
    return ParentNode("p", children)

def code_to_node(block):
    # Strip the triple backticks and any surrounding whitespace

    # org
    #text = block.strip("```")
    # Try the fix
    lines = block.split("\n")
    inner = "\n".join(lines[1:-1]) + "\n"

    # Create a raw TextNode directly
    #text_node = TextNode(text, TextType.TEXT)
    text_node = TextNode(inner, TextType.TEXT)
    code_child = text_node_to_html_node(text_node)

    # Standard HTML for code: <pre><code>...</code></pre>
    code_node = ParentNode("code", [code_child])

    return ParentNode("pre", [code_node])

def quote_to_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        # Remove the '>' and any leading space
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def ul_to_node(block):
    lines = block.split("\n")
    items = []
    for line in lines:
        text = line[2:] # Strip "- " or "* "
        children = text_to_children(text)
        items.append(ParentNode("li", children))
    return ParentNode("ul", items)

def ol_to_node(block):
    lines = block.split("\n")
    items = []
    for line in lines:
        # Split at the first dot-space combo
        parts = line.split(". ", 1)
        text = parts[1]
        children = text_to_children(text)
        items.append(ParentNode("li", children))
    return ParentNode("ol", items)

def heading_to_node(block):
    # 1. Count the number of '#' at the start of the block
    level = 0
    for char in block:
        if char == '#':
            level += 1
        else:
            break
            
    # Safety check: Markdown technically only supports h1-h6
    if level + 1 >= len(block) or block[level] != " ":
        raise ValueError(f"Invalid heading level: {level}")

    # 2. Extract the text after the '#' and the space
    text = block[level + 1:]
    
    # 3. Create the tag name (e.g., "h1", "h2", etc.)
    tag = f"h{level}"
    
    # 4. Convert the heading text into child nodes (to support bold/italic in headers)
    children = text_to_children(text)
    
    # 5. Return the ParentNode
    return ParentNode(tag, children)


def extract_title(markdown):

    # Split the input into individual lines
    lines = markdown.split('\n')
    
    for line in lines:
        # Check if the line starts with # (followed by a space or just the #)
        if line.startswith('#'):
            # Ensure it is specifically an H1 and not H2 (##), H3 (###), etc.
            content = line.lstrip('#').strip()
            
            # Check if there were exactly 1 '#' by ensuring the second char isn't '#'
            if not line.startswith('##'):
                return content
                
    # If the loop finishes without returning, no H1 was found
    raise Exception("No H1 header found in the markdown content.")


def generate_page(from_path, template_path, dest_path, basepath="/"):
    # Print a message like "Generating page from from_path to dest_path using template_path".
    # Read the markdown file at from_path and store the contents in a variable.
    # Read the template file at template_path and store the contents in a variable.
    # Use your markdown_to_html_node function and .to_html() method to convert the markdown file 
    #   to an HTML string.
    # Use the extract_title function to grab the title of the page.
    # Replace the {{ Title }} and {{ Content }} placeholders in the template with the HTML 
    #   and title you generated.
    # Write the new full HTML page to a file at dest_path. Be sure to create any necessary directories 
    #   if they don't exist.

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # 1. Read the Markdown file
    with open(from_path, 'r', encoding="utf-8") as f:
        markdown_content = f.read()

    # 2. Read the Template file
    with open(template_path, 'r', encoding="utf-8") as f:
        template_content = f.read()

    # 3. Convert Markdown to HTML
    # Note: Assuming markdown_to_html_node returns a ParentNode or LeafNode
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    # 4. Extract the Page Title
    title = extract_title(markdown_content)

    # 5. Replace Placeholders
    # First trial
    normalized_base = basepath
    # Ensure it starts with / if it's not empty
    if not normalized_base.startswith("/") and normalized_base != "":
        normalized_base = "/" + normalized_base

    if not normalized_base.endswith("/"):
        normalized_base += "/"

    # We replace the Title first, then the Content
    full_html = template_content.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", html_content)

    #safe_base = basepath if basepath.endswith("/") else f"{basepath}/"

    full_html = full_html.replace('href="/', f'href="')
    full_html = full_html.replace('src="/', f'src="')


    # 6. Ensure Destination Directory Exists
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    # 7. Write the result to the destination
    with open(dest_path, 'w', encoding="utf-8") as f:
        f.write(full_html)

    print(f"Successfully generated: {dest_path}")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith(".md"):
                from_path = os.path.join(root, file)
                relative_path = os.path.relpath(from_path, dir_path_content)
                dest_path = os.path.join(dest_dir_path, relative_path).replace(".md", ".html")
                generate_page(from_path, template_path, dest_path, basepath=basepath)

