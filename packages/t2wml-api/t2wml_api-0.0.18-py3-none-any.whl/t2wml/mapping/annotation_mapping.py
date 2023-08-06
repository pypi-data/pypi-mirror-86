from t2wml.spreadsheets.conversions import cell_range_str_to_tuples


test_case= [
            {
                "indices": [
                    [
                        3,
                        3
                    ],
                    [
                        3,
                        0
                    ],
                    [
                        4,
                        3
                    ],
                    [
                        4,
                        0
                    ],
                    [
                        5,
                        3
                    ],
                    [
                        5,
                        0
                    ],
                    [
                        6,
                        3
                    ],
                    [
                        6,
                        0
                    ],
                    [
                        7,
                        3
                    ],
                    [
                        7,
                        0
                    ],
                    [
                        8,
                        3
                    ],
                    [
                        8,
                        0
                    ],
                    [
                        9,
                        3
                    ],
                    [
                        9,
                        0
                    ],
                    [
                        10,
                        3
                    ],
                    [
                        10,
                        0
                    ],
                    [
                        11,
                        3
                    ],
                    [
                        11,
                        0
                    ],
                    [
                        12,
                        3
                    ],
                    [
                        12,
                        0
                    ],
                    [
                        13,
                        3
                    ],
                    [
                        13,
                        0
                    ],
                    [
                        14,
                        3
                    ],
                    [
                        14,
                        0
                    ],
                    [
                        15,
                        3
                    ],
                    [
                        15,
                        0
                    ],
                    [
                        16,
                        3
                    ],
                    [
                        16,
                        0
                    ],
                    [
                        17,
                        3
                    ],
                    [
                        17,
                        0
                    ],
                    [
                        18,
                        3
                    ],
                    [
                        18,
                        0
                    ]
                ],
                "type": "qualifier"
            },
            {
                "indices": [
                    [
                        3,
                        2
                    ],
                    [
                        4,
                        2
                    ],
                    [
                        5,
                        2
                    ],
                    [
                        6,
                        2
                    ],
                    [
                        7,
                        2
                    ],
                    [
                        8,
                        2
                    ],
                    [
                        9,
                        2
                    ],
                    [
                        10,
                        2
                    ],
                    [
                        11,
                        2
                    ],
                    [
                        12,
                        2
                    ],
                    [
                        13,
                        2
                    ],
                    [
                        14,
                        2
                    ],
                    [
                        15,
                        2
                    ],
                    [
                        16,
                        2
                    ],
                    [
                        17,
                        2
                    ],
                    [
                        18,
                        2
                    ]
                ],
                "type": "mainSubject"
            },
            {
                "indices": [
                    [
                        3,
                        4
                    ],
                    [
                        4,
                        4
                    ],
                    [
                        5,
                        4
                    ],
                    [
                        6,
                        4
                    ],
                    [
                        7,
                        4
                    ],
                    [
                        8,
                        4
                    ],
                    [
                        9,
                        4
                    ],
                    [
                        10,
                        4
                    ],
                    [
                        11,
                        4
                    ],
                    [
                        12,
                        4
                    ],
                    [
                        13,
                        4
                    ],
                    [
                        14,
                        4
                    ],
                    [
                        15,
                        4
                    ],
                    [
                        16,
                        4
                    ],
                    [
                        17,
                        4
                    ],
                    [
                        18,
                        4
                    ]
                ],
                "type": "dependentVariable"
            },
            {
                "indices": [
                    [
                        3,
                        1
                    ],
                    [
                        4,
                        1
                    ],
                    [
                        5,
                        1
                    ],
                    [
                        6,
                        1
                    ],
                    [
                        7,
                        1
                    ],
                    [
                        8,
                        1
                    ],
                    [
                        9,
                        1
                    ],
                    [
                        10,
                        1
                    ],
                    [
                        11,
                        1
                    ],
                    [
                        12,
                        1
                    ],
                    [
                        13,
                        1
                    ],
                    [
                        14,
                        1
                    ],
                    [
                        15,
                        1
                    ],
                    [
                        16,
                        1
                    ],
                    [
                        17,
                        1
                    ],
                    [
                        18,
                        1
                    ]
                ],
                "type": "property"
            }
        ]


# some basic rules for yaml formation:

# Qualifiers (purple):
# 1. a qualifier with a single cell is applied to every single statement
# 2. a qualifier with a continuous single-column or single-row region will iterate with dependent variable that follows that region
# 3. a qualifier with split single-column or single-row regions will look for similarly split dependent variable
# 4. a qualifier with split single-cells will follow the -n strategy either leftwards or upwards

# Main subject (blue):
# Other than being required, and limited to only one per statement it should be that main subject has the same issues as qualifier (?)

# Properties (orange):
# 1. any indicated property is going to attempt to find the matching qualifier, main subject, or dependent variable to which it belongs 
# (properties do not exist as standalone objects, without a match they are meaningless)

# Dependent variable (green):
# 1. The dependent variable is simply the region in the yaml. 
# 2. The easiest way to do the dependent variable is simply to leave it the way it was input 
# 3. [ranges + cells - requires change to cell functionality]:
#              selecting cells takes precedence over all skip methods
#              skipping empty cells needs to take place outside of region
# 4. the only interesting challenges related to the dependent variable are relatively linking it to other fields, 
#      whether it's really two dependent variables globbed together
#      or one sparse variable whose spatiral relationships are many steps away



class ValueArgs:
    def __init__(self, string=None, cell=None, range=None, use_item=False):
        if string is None and cell is None and range is None:
            raise ValueError("must specify one of: string, cell, range")
        self.string=string
        self.cell=cell
        self.range=range
        self.use_item=use_item

    def get_expression(self, relative_node, use_q=False):
        if self.string is not None:
            return self.string
        
        if self.use_item:
            return_string= "=item[{indexer}]"
        else:
            return_string= "=value[{indexer}]"
        

        if self.cell is not None:
            cell_str = self.cell[0] + ", " + self.cell[1]
            return return_string.format(indexer=cell_str)

        #insert complex logic for matching between ranges here, 
        # for now let's do the simple case of perfectly matched along one dimension

        relative_range=relative_node.value_args.range
        if not relative_range:
            raise ValueError("No idea how to do many-to-one matching")
            
        (rel_start_col, rel_start_row), (rel_end_col, rel_end_row) = cell_range_str_to_tuples(relative_range)
        (self_start_col, self_start_row), (self_end_col, self_end_row) = cell_range_str_to_tuples(self.range)
        
        row_var = ", $qrow" if use_q else ", $row"
        col_var= "$qcol, " if use_q else "$col, "

        if (rel_start_row, rel_end_row) == (self_start_row, self_end_row):
            if self_start_col==self_end_col:
                col=self.range[0]
                return return_string.format(indexer=col+row_var)
            else:
                raise ValueError("don't know how to handle multi-dimensional matching yet")
        if (rel_start_col, rel_end_col) == (self_start_col, self_end_col):
            if self_start_row==self_end_row:
                return return_string.format(indexer=col_var+str(self_start_row+1))
            else:
                raise ValueError("don't know how to handle multi-dimensional matching yet")
        

class Node:  
    def __init__(self, value_args):
        self.value_args=value_args
    
    def get_expression(self, relative_node, use_q=False):
        return self.value_args.get_expression(relative_node, use_q)


class ExpandedNode(Node):
    def __init__(self, value_args, property, optionals=None):
        super().__init__(value_args)
        self.property = property
        self.optionals = optionals or {}#{key string: Node} #eg {unit: Node, calendar: Node}

    def expand(self):
        pass


class MainNode(ExpandedNode):
    def __init__(self, value_args, property, mainSubject, qualifiers=None, optionals=None):
        super().__init__(value_args, property, optionals)
        self.mainSubject = mainSubject
        self.qualifiers = qualifiers or []
    
    def get_qualifier_yaml(self, qualifier):
        propertyLine=qualifier.property.get_expression(qualifier, use_q=True) #relative to qualifier
        valueLine=qualifier.get_expression(self) #relative to statement
        optionalsLines=""
        for key in qualifier.optionals:
            line= key+": "+qualifier.optionals[key].get_expression(self)
            optionalsLines+=line
        qualifier_string = """
                    - property: {propertyLine}
                      value: {valueLine}
                      {optionalsLines}""".format(propertyLine=propertyLine, valueLine=valueLine, optionalsLines=optionalsLines)
        return qualifier_string


    def get_region(self):
        if self.value_args.range:
            return "range: "+self.value_args.range
        else:
            raise ValueError("Not handling anything else yet")

    def get_yaml(self):
        region=self.get_region()
        mainSubjectLine=self.mainSubject.get_expression(self)
        propertyLine=self.property.get_expression(self)
        qualifierLines=""
        for qualifier in self.qualifiers:
            qualifierLines+=self.get_qualifier_yaml(qualifier)
        optionalsLines=""
        for key in self.optionals:
            line= key+": "+self.optionals[key].get_expression(self)
            optionalsLines+=line

        yaml="""statementMapping:
            region:
                - {region}
            template:
                subject: {mainSubjectLine}
                property: {propertyLine}
                value: =value[$col, $row]
                {optionalsLines}
                qualifier:
                    {qualifierLines}""".format(region=region, mainSubjectLine=mainSubjectLine, propertyLine=propertyLine, optionalsLines=optionalsLines, qualifierLines=qualifierLines)
        return yaml




q1=ExpandedNode(value_args=ValueArgs(range="A4:A11", use_item=True), 
                property=Node(value_args=ValueArgs(cell="A3", use_item=True)))
q2=ExpandedNode(value_args=ValueArgs(range="D3:E3", use_item=False), 
                property=Node(value_args=ValueArgs(string="P585", use_item=True)),
                optionals={"precision": Node(value_args=ValueArgs(string="year"))})

annotatedGraph=MainNode(
    value_args=ValueArgs(range="D4:E11", use_item=False),
    property=Node(value_args=ValueArgs(range="B4:B11", use_item=True)),
    mainSubject=Node(value_args=ValueArgs(range="C4:C11", use_item=True)),
    qualifiers=[q1, q2],
    optionals= {"unit": Node(value_args=ValueArgs(string="units"))}
)

print(annotatedGraph.get_yaml())