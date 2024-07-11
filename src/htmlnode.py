import re

from textnode import TextNode


#Assumptions:
#Expected behaviour:
#   parent class for LeafNode and ParentNode 
#Encapsulation change:
class HTMLNode:
    # tag: a string representing the HTML tag name (p, a, h1, etc)
    # value: a string representing the value of the HTML tag (e.g. text)
    # children: a list of HTMLNode objects representing the children 
    # of this node
    # props: a dictionary of key-value pairs representing the attributes of
    # the HTML tag. For example, a link (<a> tag) might have
    # {"href": "https://www.boot.dev"}
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
        # child classes will override this method to render themselves as html

    def props_to_html(self):        
        ret_value = ""
        for key in self.props:
            ret_value += f' {key}="{self.props[key]}"'

        ret_value = ret_value.lstrip()
        return ret_value

    def __repr__(self):
        ret_value = "" 
        if self.tag != None:
            print(f"tag:{self.tag}")
        if self.value != None:
            print(f"value:{self.value}")
        if self.children != None:
            print(f"children:{self.children}")
        if self.props != None:
            print(f"props:{self.props}")
        return ret_value

    def __eq__(self, HTMLNode2):
        flag = True
        if(self.tag != HTMLNode2.tag or self.value != HTMLNode2.value):
            flag = False

        # does not test self.children being equal between compared nodes. 
        # testing self.children most likely requires recursion         

        if(self.props == None and HTMLNode2.props == None):
            pass
        elif(self.props == None or HTMLNode2.props == None):
            flag = False
        else:
            dict_keys = self.props.keys()
            dict_keys2 = HTMLNode2.props.keys()
            if(len(dict_keys)) != len(dict_keys2):
                flag = False
            else:
                for key in dict_keys:
                    if key not in dict_keys2:
                        flag = False

        return flag

#Assumptions:
#Expected behaviour:
#Encapsulation change:
class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag=="" or self.tag==None:
            raise ValueError
        if self.children==None:
            raise ValueError("no children asigned to ParentNode")

        html_string = f"<{self.tag}>"
        for child in self.children:
            html_string += child.to_html()
        html_string += f"</{self.tag}>"
        return html_string

#Assumptions:
#Expected behaviour:
#Encapsulation change:
class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)
    
    def __repr__(self):
        ret_string = ""
        if self.tag != None:
            print(f"tag is:{self.tag}")
        if self.value != None:
            print(f"value is:{self.value}")
        if self.props != None:
            print(f"props are:{self.props}")
        return ret_string

    def to_html(self):
        if self.value == None:
            raise ValueError
        if self.tag == None:
            return self.value
        else:
            if self.props == None:
                return f"<{self.tag}>{self.value}</{self.tag}>"
            else:
                prop = self.props_to_html()
                return f"<{self.tag} {prop}>{self.value}</{self.tag}>"
            
#Assumptions:
#  that the parameter text_node is a TextNode class object.
#Expected behaviour:
#  creates and returns a LeafNode class object outof the text_node parameter.
#Encapsulation change:
#  none.
def text_node_to_html_node(text_node):
    if text_node.text_type == "text":
        return LeafNode(None, text_node.text)
    elif text_node.text_type == "bold":
        return LeafNode("b", text_node.text)
    elif text_node.text_type == "italic":
        return LeafNode("i", text_node.text)
    elif text_node.text_type == "code":
        return LeafNode("code", text_node.text)
    elif text_node.text_type == "link":
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == "image":
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise Exception("unknown text_type in function text_node_to_html_node")



text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

#Assumptions:
#   that the paramter "old_nodes" is a list containing various TextNodes.
#   the parameter "delimiter" contains either "**", "*", or "`".
#   the parameter "text_type" contains either text_type_bold, text_type_italic,
#  or text_type_code.
#Expected behaviour:
#   checks each old_nodes if it is a text_type_text it proceeds to break up
#  that text into what the delimiter argument is defined as and the remainder
#  into text .. however it outputs only a TextNode class object list.
#Encapsulation change:
#  none.
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], text_type_text))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

#Assumptions:
#Expected behaviour:
#   finds all strings resembling: "![any text](and a link)"
#   returns a list of tuples resembling: "[('any text','and a link'), ..]"
#Encapsulation change:
#   none.
def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

#Assumptions:
#Expected behaviour:
#    same as the function extract_markdown_image except this function finds
#   a string resembling: "[any text](and a link)"
#Encapsulation change:
#   none.
def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


#Assumptions:
#   that the argument "old_nodes" containes a list of TextNode class objects.
#Expected behaviour:
#   for all nodes in old_nodes that are text_type_text and where an image
#  link is found within .. that node's image gets extracted into a TextNode
#  class objects .. 
#  and the remainder of that node's text that does not belong to the image
#  gets extracted into their own TextNode class objects.
#   returned value is a list of TextNodes.
#Encapsulation change:
#  none.
def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        image_tup = extract_markdown_images(node.text)
        if len(image_tup) == 0: # no images found
            new_nodes.append(node)
            continue

        text_remainder = node.text
        strung_nodes = []
        for tup in image_tup:
            split_node = text_remainder.split(f"![{tup[0]}]({tup[1]})", 1)
            if split_node[0] == "":
                strung_nodes.append(TextNode(tup[0], text_type_image, tup[1]))
            else:
                strung_nodes.append(TextNode(split_node[0], text_type_text))
                strung_nodes.append(TextNode(tup[0], text_type_image, tup[1]))
            text_remainder = split_node[1]

        if text_remainder != "":
            strung_nodes.append(TextNode(text_remainder, text_type_text))

        new_nodes.extend(strung_nodes)
    return new_nodes

  

#Assumptions:
#  that the parameter old_nodes contains a list of TextNode class objects.
#Expected behaviour:
#  processes only TextNode class objects that are of the type text_type_text.
#  if it finds a link in the TextNode it proceeds to extract it one by one.
#  Placing the link into a TextNode and surrounding text that does not belong
# to the link into their own TextNodes.
#  Returned value is a list of textnodes
def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        link_tup = extract_markdown_links(node.text)
        if len(link_tup) == 0: # no links found
            new_nodes.append(node)
            continue

        text_remainder = node.text
        strung_nodes = []
        for tup in link_tup:
            split_node = text_remainder.split(f"[{tup[0]}]({tup[1]})", 1)
            if split_node[0] == "":
                strung_nodes.append(TextNode(tup[0], text_type_link, tup[1]))
            else:
                strung_nodes.append(TextNode(split_node[0], text_type_text))
                strung_nodes.append(TextNode(tup[0], text_type_link, tup[1]))
            if len(split_node) > 1:
                text_remainder = split_node[1]

        if text_remainder != "":
            strung_nodes.append(TextNode(text_remainder, text_type_text))

        new_nodes.extend(strung_nodes)
    return new_nodes


#Assumptions:
#  The parameter "text" is a string that contains a document. Various text in
# the document is surrounded by **, *, `, [link](..), or ![link](..) to 
# indicate that the text they surround are respectively bold, italic, code, 
# links, or image links.
#Expected behaviour:
#   Outputs a list of TextNodes.
#   Takes a string and makes a TextNode outof it, 
#  and defines that TextNode into other types of TextNodes other than
#  text_type_text.
def text_to_textnodes(text):
    ret_node = []
    init_text_node = [TextNode(text, text_type_text)]

    ret_node = split_nodes_delimiter(init_text_node, "**", text_type_bold)
    ret_node = split_nodes_delimiter(ret_node, "*", text_type_italic)
    ret_node = split_nodes_delimiter(ret_node, "`", text_type_code)
    ret_node = split_nodes_image(ret_node)
    ret_node = split_nodes_link(ret_node)
    return ret_node

