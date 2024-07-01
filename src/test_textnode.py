import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold", "https://boot.dev")
        node2 = TextNode("This is a text node", "bold", "https://boot.dev")
        self.assertEqual(node, node2)


text_node1 = TextNode("text text text", "text", "https://www")
if type(text_node1) == TextNode:
    print("yes")


if __name__ == "__main__":
    unittest.main()

# This test creates two TextNode objects with the same properties and 
# asserts that they are equal. If you run your tests with ./test.sh, you 
# should see that the test passes.




