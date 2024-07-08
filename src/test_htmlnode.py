import unittest

from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("<a>", "link to Bootdev",None, {"href": "https://www.boot.dev", "target": "_blank"})
        node2= HTMLNode("<a>", "link to Bootdev",None, {"href": "https://www.boot.dev", "target": "_blank"})
        self.assertEqual(node, node2)


# testing ParentNode is below this line
node = ParentNode(
    "p",
    [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
        ParentNode(
            "p",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                    ]),
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                    ]),

            ]),

    ],
)
print(node.to_html())


# testing function text_node_to_html_node(text_node)
textnode1 = TextNode("text text text", "text", None)
textnode2 = TextNode("this is bold text", "bold", None)
textnode3 = TextNode("this is italic text", "italic", None)
textnode4 = TextNode("this is code text", "code", None)
textnode5 = TextNode("this is a link", "link", "https://www.boot.dev")
textnode6 = TextNode("pic description", "image", "https//www.linkTo.png")
leafNode1 = text_node_to_html_node(textnode6)
print("---------------")
print(leafNode1.to_html())
print(leafNode1)


node = TextNode("This is text with a `code block` word", "text", "")
new_nodes = split_nodes_delimiter([node], "`", "code")
print(new_nodes)


text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
print(extract_markdown_images(text))
#expected output:
# [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")]


text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
answer1 = extract_markdown_links(text)
print(answer1)
# expected output
answer2 = [("link", "https://www.example.com"), ("another", "https://www.example.com/another")]


node2 = TextNode(
    "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
    text_type_text,
)
# node2 = TextNode("text text text", text_type_text)
new_nodes2 = split_nodes_image([node2])
print("--------------")
print(new_nodes2)


node3 = TextNode(
    "This is text with a [link](https://storage.googleapis.com) and another [second link](https://example.link.com) and that concludes the 2 links.",
    text_type_text,
)
new_nodes3 = split_nodes_link([node3])
print("--------------")
print(new_nodes3)


text_test1 = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
text_test2 =  "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev) [link](https://www.ruv.is) **ruv** *is* a website."
print("----------------")
text_to_textnodes_2 = text_to_textnodes(text_test2)
print(text_to_textnodes_2)

print("-----------------")
html_nodes_2 = []
for textnode in text_to_textnodes_2:
    html_nodes_2.append(text_node_to_html_node(textnode))

print("----------------")
string_1 = ""
for html_node in html_nodes_2:
    string_1 += html_node.to_html()

print(string_1)


if __name__ == "__main__":
    unittest.main()

