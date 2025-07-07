#import the dependencies
#import xml.etree.ElementTree as ET

# Load and parse the TGML file
#tree = ET.parse(r'C:\Users\kambica\Desktop\DDC-37\DDC-14(1) B1 Main Electrical Room.tgml')
#root = tree.getroot()

"""
#root 
print(root.tag)
print(len(root))


#Access root child
print(root[0].tag)
print(len(root[0]))
"""
"""
#Loop over root children
for child in root:
    print(child[0].tag)
    print(child[0].text)
"""

"""
#Root grandchildren 
print(root[0][0].tag)   
print(root[0][0].text)   
print(root[0][1].tag)   
print(root[0][1].text) 


#get an attribute
print(root.attrib)
"""
"""
#loop over 'tag name'
for name in root.iter('name'):
    print(name.text)  """
    

#change name & remove 
#root[0][2].text="label"
#root[1].remove(root[1][3])
#tree.write('C:\Users\kambica\Desktop\DDC-37\DDC-14(4).tgml')

"""
# Loop through all <Text> elements
for text in root.findall('.//Text'):
    name = text.get('Name')
    label = text.text.strip() if text.text else ''
    if name:   # Only print if Name attribute exists
        print(f"Name: {name}, Label: {label}")
"""

"""
#find children with 'name' tag
print(len(root[0].findall('name')))
print(root[0].findall('name')[0].text) 


for elem in root.iter():
    name = elem.get('Name')
    if name:      
        #print(f"Tag: {elem.tag}, Name: {name}")
        print(f"Name: {name}")

------------------------------------------------------------------------------------------------------------
"""

import xml.etree.ElementTree as ET
import sys
 
def extract_text_bind_pairs_from_group(xml_file, query_name=None):
    try:
        context = ET.iterparse(xml_file, events=("start", "end"))
        _, root = next(context)
 
        group_stack = []
        current_text = None
        pairs = []
 
        for event, elem in context:
            if event == "start":
                if elem.tag == "Group":
                    group_stack.append(True)
                elif elem.tag == "Text" and group_stack:
                    current_text = elem.attrib.get("Name", "")
                elif elem.tag == "Bind" and group_stack and current_text is not None:
                    bind_name = elem.attrib.get("Name", "")
                    pairs.append((current_text, bind_name))
 
            elif event == "end":
                if elem.tag == "Group":
                    group_stack.pop()
                elif elem.tag == "Text":
                    current_text = None
                elem.clear()
 
        # If a query is provided, search for it
        if query_name:
            found = False
            for text, bind in pairs:
                if query_name == text:
                    print(f"Bind Name for Text '{text}': {bind}")
                    found = True
                elif query_name == bind:
                    print(f"Text Name for Bind '{bind}': {text}")
                    found = True
            if not found:
                print(f"No match found for: {query_name}")
        else:
            # If no query, print all pairs
            for text, bind in pairs:
                print(f"Text Name: {text}, Bind Name: {bind}")
 
    except Exception as e:
        print(f"Error: {e}")
 
# Command-line usage
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_pairs.py <xml_file> [text_or_bind_name]")
    else:
        xml_path = sys.argv[1]
        name_query = sys.argv[2] if len(sys.argv) == 3 else None
        extract_text_bind_pairs_from_group(xml_path, name_query)
