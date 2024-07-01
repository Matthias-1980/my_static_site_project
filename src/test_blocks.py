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
print(block_to_block_type(markdown_list))



