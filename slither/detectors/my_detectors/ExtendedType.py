from collections import defaultdict
import os
import sys
script_dir = os.path.dirname( __file__ )
sys.path.append(script_dir)
#USAGE: file containing the structure representing an Extended type instance
#       Extended types have two main subclasses: token types and business types
#       Token types follow the default token structure of:
#           - numerator type(s)
#           - denominator type(s)
#           - normalization amt
#           - linked contract (for addresses)
#           - fields          (for objects)
#       Business types (usually one) are categorical, i.e. (fee, balance, ...) and their relations will be defined here

from tcheck_parser import f_type_name, f_type_num

class ExtendedType():
    def __init__(self):
        #Initialized an 'undefined' data type
        self._name: Optional[str] = None
        self._function_name: Optional[str] = None
        self._contract_name: Optional[str] = None
        #Token type
        self._num_token_types = []
        self._den_token_types = []
        self._base_decimals = 0
        self._norm = 'u'
        self._linked_contract = None
        self._fields = []
        self._reference_root = None
        self._reference_field = None
        #Business type
        self._finance_type = None

    #Getters and setters for the fields
    @property
    def name(self):
        return(self._name)

    @name.setter
    def name(self, sname):
        self._name = sname

    @property
    def ref_root(self):
        return(self._reference_root)

    @property
    def ref_field(self):
        return(self._reference_field)
    
    def ref(self, ref):
        self._reference_root = ref[0]
        self._reference_field = ref[1]

    @property
    def function_name(self):
        return(self._function_name)

    @function_name.setter
    def function_name(self, fname):
        self._function_name = fname

    @property
    def contract_name(self):
        return(self._contract_name)
    
    @contract_name.setter
    def contract_name(self, cname):
        self._contract_name = cname
    
    @property
    def num_token_types(self):
        return(self._num_token_types)

    def add_num_token_type(self, token_type):
        if(token_type == -1):
            if(len(self._num_token_types) != 0 or token_type in self._num_token_types):
                return
            self._num_token_types.append(token_type)
        else:
            if(token_type in self._den_token_types):
                self._den_token_types.remove(token_type)
            else:
                if(-1 in self._num_token_types):
                    self._num_token_types.remove(-1)
                self._num_token_types.append(token_type)

    def clear_num(self):
        self._num_token_types.clear()

    @property
    def den_token_types(self):
        return(self._den_token_types)

    def add_den_token_type(self, token_type):
        if(token_type == -1):
            if(len(self._den_token_types) != 0 or token_type in self._den_token_types):
                return
            self._den_token_types.append(token_type)
        else:
            if(token_type in self._num_token_types):
                self._num_token_types.remove(token_type)
            else:
                if(-1 in self._den_token_types):
                    self._den_token_types.remove(-1)
                self._den_token_types.append(token_type)
    
    def clear_den(self):
        self._den_token_types.clear()

    @property
    def norm(self):
        return self._norm

    @norm.setter
    def norm(self, a):
        self._norm = a
    
    @property
    def base_decimals(self):
        return self._base_decimals

    @base_decimals.setter
    def base_decimals(self, a):
        self._base_decimals = a

    def total_decimals(self):
        if(self._norm == "*"):
            return "*"
        else:
            return(self._base_decimals + self._norm)

    @property
    def linked_contract(self):
        return self._linked_contract

    @linked_contract.setter
    def linked_contract(self, a):
        self._linked_contract = a

    @property
    def fields(self):
        return self._fields

    def add_field(self, new_field):
        for field in self._fields:
            if(field.name == new_field.name):
                self._fields.remove(field)
                break
        self._fields.append(new_field)

    def print_fields(self):
        print(f"{self._name} Fields:")
        for field in self._fields:
            print(f"{field.name}")
        print("^^^")


    def is_undefined(self) -> bool:
        if(len(self._num_token_types) == 0 and len(self._den_token_types) == 0):
            return True
        return False

    def is_constant(self) -> bool:
        if(len(self._num_token_types) == 1 and len(self._den_token_types) == 1 and self._num_token_types[0] == -1 and self._den_token_types[0] == -1):
            return True
        return False

    def token_type_clear(self):
        self.clear_num()
        self.clear_den()
        self.norm = 'u'
        self.link_function = None

    def init_constant(self):
        if not(self.is_undefined()):
            print("[W] Initializing defined variable to constant")
        self.token_type_clear()
        self.add_num_token_type(-1)
        self.add_den_token_type(-1)
        self.norm = 'u';

    @property
    def finance_type(self):
        return self._finance_type

    @finance_type.setter
    def finance_type(self, f_type):
        self._finance_type = f_type

    def __str__(self):
        num_token_types_str = ", ".join(str(elem) for elem in self._num_token_types)
        den_token_types_str = ", ".join(str(elem) for elem in self._den_token_types)
        fields_str = ", ".join(str(elem.name) for elem in self._fields)
        return (
            f"\n"
            f"Name: {self._name} Function: {self._function_name}\n"
            f"Num: {num_token_types_str}\n"
            f"Den: {den_token_types_str}\n"
            f"Norm: {self._norm}\n"
            f"LF: {self._linked_contract}\n"
            f"Fields: {fields_str}\n"
            f"Finance Type: {self._finance_type}"
        )
 
        
