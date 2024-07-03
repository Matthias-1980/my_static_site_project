from htmlnode import *

#Assumptions: 
#   that the pargument "markdown" is an entire document
#Expected behaviour:
#   breaks a document down into lists. Each list element is considered a block.
#   Blocks are defined by new lines between them.
#Encapsulation change: 
#   none
def markdown_to_blocks(markdown):
    new_block_flag = False
    true_new_block = False
    assembled_line = ""
    ret_list = []

    for letter in markdown:
        if true_new_block and letter != '\n':
            assembled_line = assembled_line.strip()
            # assembled_line += '\n' #end of blocks get new line character
            ret_list.append(assembled_line)
            assembled_line = ""
            assembled_line += letter
            new_block_flag = False
            true_new_block = False

        elif new_block_flag and letter == '\n':
            true_new_block = True

        elif letter == '\n':
            new_block_flag = True

        else:
            if new_block_flag:
                # elements within same block get seperated by new line char
                assembled_line += ('\n' + letter)
            else:
                assembled_line += letter
                
            new_block_flag = False

    ret_list.append(assembled_line.strip())

    return ret_list


block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"

#Assumptions:
#   Headings allow empty heading text: "### " vs "### Heading Text".
#Expected behaviour:
#   For each first characters per block in a list of blocks .. 
#  those characters define what that block is: code, quote, list, heading, .. .
#Encapsulation change:
#   None.
def block_to_block_type(block_list):
    max_heading_degree = 6

    ret_tuple_list = []
    for block in block_list:
        
        if block[0] == '#':
            heading_degree = 0
            for cha in block:
                if cha == '#':
                    heading_degree += 1
                else:
                    break

            if (len(block) > heading_degree and 
                heading_degree <= max_heading_degree):
                if block[heading_degree] == ' ':
                    tupl = (block, block_type_heading)
                    ret_tuple_list.append(tupl)
                    continue

            tupl = (block, block_type_paragraph)
            ret_tuple_list.append(tupl)

        elif block[0:3] == "```" and block[-3:] == "```":
            tupl = (block, block_type_code)
            ret_tuple_list.append(tupl)

        elif block[0] == '>':
            search_flag = False
            proper_flag = False
            one_line = True
            
            if block.find('\n') != -1:
                one_line = False
            else:
                one_line = True
                proper_flag = True

            for cha in block:
                if one_line:
                    break
                if not search_flag and cha == '\n':
                    search_flag = True
                    proper_flag = False
                    continue
                if search_flag and cha == '>':
                    proper_flag = True
                    search_flag = False
                if search_flag and cha == ' ':
                    proper_flag = False
                    break

            if proper_flag:
                tupl = (block, block_type_quote)
                ret_tuple_list.append(tupl)
            else:
                tupl = (block, block_type_paragraph)
                ret_tuple_list.append(tupl)

        elif block[0:2] == "* " or block[0:2] == "- ":
            search_flag = False
            proper_flag = False
            one_line = True

            if block.find('\n') != -1:
                one_line = False
            else:
                one_line = True
                proper_flag = True

            for i in range(0, len(block) - 1):
                if one_line:
                    break
                if not search_flag and block[i] == '\n':
                    search_flag = True
                    proper_flag = False
                    continue
                if (search_flag and 
                    (block[i:i+2] == "* " or block[i:i+2] == "- ")):
                    proper_flag = True
                    search_flag = False
                if search_flag and block[i] == ' ':
                    proper_flag = False
                    break

            if proper_flag:
                tupl = (block, block_type_unordered_list)
                ret_tuple_list.append(tupl)
            else:
                tupl = (block, block_type_paragraph)
                ret_tuple_list.append(tupl)

        elif block[0:3] == "1. ":
            search_flag = False
            proper_flag = False
            one_line = True
            cur_ind_str = "2. "
            cur_ind = 2

            if block.find('\n') != -1:
                one_line = False
            else:
                one_line = True
                proper_flag = True

            for i in range(0, len(block) - 1):
                if one_line:
                    break
                if not search_flag and block[i] == '\n':
                    search_flag = True
                    proper_flag = False
                    continue
                if search_flag and block[i:i+3] == cur_ind_str:
                    proper_flag = True
                    search_flag = False
                    cur_ind += 1
                    cur_ind_str = str(cur_ind) + ". "
                if search_flag and block[i] == ' ':
                    proper_flag = False
                    break

            if proper_flag:
                tupl = (block, block_type_ordered_list)
                ret_tuple_list.append(tupl)
            else:
                tupl = (block, block_type_paragraph)
                ret_tuple_list.append(tupl)


        else:
            tupl = (block, block_type_paragraph)
            ret_tuple_list.append(tupl)
        
    return ret_tuple_list


#Assumptions:
#   Gets passed a string that is a quote.
#Expected behaviour:
#   From that string it creates a ParentNode to contain the ChildNode(s).
#   For each '\n' character in said string there is another child (n+1 pr \n).
#Encapsulation change:
#   None.
def block_to_html_quote(block):
    quote_symbol = ">"
    children = []
    
    child_text = block.split('\n')
    new_child_text = []
    for text in child_text:
        new_child_text.append(text.lstrip(quote_symbol))

    children = []
    for text in new_child_text:
        children.append(LeafNode("p", text))

    parentNode = ParentNode("blockquote", children)
    return parentNode

#Assumptions:
#   Gets passed a string that is an unordered list.
#   That list begins either with a "* " or "- ".
#Expected behaviour:
#   From that string it creates a ParentNode to contain the ChildNode(s).
#   For each '\n' character in said string there is another child (n+1 pr \n).
#Encapsulation change:
#   None.
def block_to_html_unordered_list(block):
    unordered_list_symbol = "* "

    search_val = block.find(unordered_list_symbol)
    if search_val != 0:
        unordered_list_symbol = "- "

    children = []
    
    child_text = block.split('\n')
    new_child_text = []
    for text in child_text:
        new_child_text.append(text.lstrip(unordered_list_symbol))

    children = []
    for text in new_child_text:
        children.append(LeafNode("li", text))

    parentNode = ParentNode("ul", children)
    return parentNode

def block_to_html_ordered_list(block):
    list_line_num = 1
    list_symbol = "1. "
    children = []
    
    child_text = block.split('\n')
    new_child_text = []
    for text in child_text:
        new_child_text.append(text.lstrip(list_symbol))
        list_line_num += 1
        list_symbol = str(list_line_num) + ". "

    children = []
    for text in new_child_text:
        children.append(LeafNode("ol", text))

    parentNode = ParentNode("li", children)
    return parentNode

#Assumptions:
#  That the block parameter contains a string surrounded by "```" 
#Expected behaviour:
#  Takes the block paramter, which is a string, and turns it into
# a LeadNode class object encapsulated by a ParentNode that in turn is 
# encapsulated by another ParentNode. As an effect the returned html looks 
# like: <pre><code>block string</code></pre>
#Encapsulation change:
#  None
def block_to_html_code(block):
    code_symbol = "```"
    children = []

    block = block.lstrip(code_symbol)
    block = block.rstrip(code_symbol)
    child_text = block.split('\n')

    for child in child_text:
        children.append(LeafNode("p", child)) 

    parentNode = ParentNode("code", children)
    parentNode2 = ParentNode("pre", [parentNode])

    return parentNode2


def block_to_html_heading(block):
    header_symbol = '#'
    header_degree = 0
    children = []

    for char in block:
        if char == header_symbol:
            header_degree += 1
        else:
            break
    
    header_is = 'H' + str(header_degree)

    if header_degree == 1:
        block = block.lstrip(header_symbol)
    else:
        for i in range(0, header_degree - 1):
            block = block.lstrip(header_symbol)

    child_text = block.split('\n')

    for child in child_text:
        children.append(LeafNode("p", child))

    return ParentNode(header_is, children)

def block_to_html_paragraph(block):
    return LeafNode("p", block)


