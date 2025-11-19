class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag      = tag
        self.value    = value
        self.children = children
        self.props    = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        str = ""
        if self.props:
            for prop in self.props.items():
                str += f' {prop[0]}="{prop[1]}"'
        return str
    
    def __repr__(self, level=0):
        indent = ''
        for _ in range (1, level+1):
            indent += '    '
        str = "HTMLNode {"
        if self.tag is None:
            str += f'\n{indent}  tag: {self.tag}'
        else:
            str += f'\n{indent}  tag: "{self.tag}"'
        if self.value is None:
            str += f'\n{indent}  value: {self.value}'
        else:
            str += f'\n{indent}  value: "{self.value}"'
        if self.children is None:
            str += f'\n{indent}  children: {self.children}'
        else:
            str += f'\n{indent}  children: ['
            for child in self.children:
                str += f'\n{indent}    {child.__repr__(level+1)},'
            str += f'\n{indent}  ]'
        if self.props is None:
            str += f'\n{indent}  props: {self.props}'
        else:
            str += f'\n{indent}  props: '
            str += '{'
            for prop in self.props.items():
                str += f'\n{indent}    {prop[0]}: "{prop[1]}",'
            str += f'\n{indent}'
            str += '  }'
        str += f"\n{indent}"
        str += "}"
        return str

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Missing 'value' property")
        
        if self.tag is None:
            return self.value
        if self.value is None or len(self.value) == 0:
            return f'<{self.tag}{self.props_to_html()}/>'
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("Missing 'tag' property")
        if self.children is None:
            raise ValueError("Missing 'children' property")
        
        str = f'<{self.tag}{self.props_to_html()}>'
        for child in self.children:
            str += child.to_html()
        str += f'</{self.tag}>'
        return str
    
def append_child(parent, child):
    if not isinstance(parent, ParentNode):
        raise TypeError("Invalid type: Parnet must be a ParentNode")
    parent.children.append(child)
