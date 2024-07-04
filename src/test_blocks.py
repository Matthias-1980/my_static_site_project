from blocks import *

test_text1 = '''This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list

* This is a list
* This is a second line

* This is not a list
 * This is the second line
* This is the 3rd line

- This is a list

- This is a list
- on two lines

- This is not a list
 - This is second line
- This is the 3rd line

1. This is an ordered list

1. This is an ordered list
2.     With many many lines
3. that 
4. are 4

1. This is not an ordered list
 2. cause of this line
3. that contains a white space

###### This is a heading on one line

# This is a heading
on many many
lines.

####### This is not a heading.

```This is code text```

`` This is not code text ``

` This is not code text `

``` This is code 
text on 
many many 
lines```

>This is a quote

>This is a quotes
>this is an end of a quote

> Quote

> Not a quote
 >cause of this line

> not a quote
 >cause of this line
>here is the 3rd line
'''
print(test_text1)
markdown_list = markdown_to_blocks(test_text1)
print("------------------")
print(markdown_list)

print("------------------")
list_to_blocks = block_to_block_type(markdown_list)
print(list_to_blocks)

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"

print("------------------")
test_node = []
for item in list_to_blocks:
    if item[1] == block_type_heading:
        test_node.append(block_to_html_heading(item[0]))

for node in test_node:
    print(node.to_html())


print("-------markdown_to_html_node function--------")
parentNode = markdown_to_html_node(test_text1)
print(parentNode.to_html())
