class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, TextNode2):
        if(self.text == TextNode2.text and 
            self.text_type == TextNode2.text_type and
            self.url == TextNode2.url
           ):
            return True
        else:
            return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"



