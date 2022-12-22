
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = "ADD_OP BLOCKNAME IDENTIFIER MUL_OP NUMBER WHILEprogramme : statement\n                    | statement ';' programmestatement : assignement\n                | while\n                | block  assignement : IDENTIFIER '=' expression while : WHILE expression '{' programme '}'  block : BLOCKNAME '(' listP ')'  listP : expression \n                | expression ',' listP expression : NUMBER \n                | IDENTIFIERexpression : '(' expression ')' expression : expression ADD_OP expression \n                | expression MUL_OP expression "
    
_lr_action_items = {'IDENTIFIER':([0,7,9,10,14,15,18,19,20,29,],[6,13,6,13,13,13,6,13,13,13,]),'WHILE':([0,9,18,],[7,7,7,]),'BLOCKNAME':([0,9,18,],[8,8,8,]),'$end':([1,2,3,4,5,12,13,16,17,25,26,27,28,30,],[0,-1,-3,-4,-5,-11,-12,-2,-6,-14,-15,-13,-8,-7,]),'}':([2,3,4,5,12,13,16,17,24,25,26,27,28,30,],[-1,-3,-4,-5,-11,-12,-2,-6,30,-14,-15,-13,-8,-7,]),';':([2,3,4,5,12,13,17,25,26,27,28,30,],[9,-3,-4,-5,-11,-12,-6,-14,-15,-13,-8,-7,]),'=':([6,],[10,]),'NUMBER':([7,10,14,15,19,20,29,],[12,12,12,12,12,12,12,]),'(':([7,8,10,14,15,19,20,29,],[14,15,14,14,14,14,14,14,]),'{':([11,12,13,25,26,27,],[18,-11,-12,-14,-15,-13,]),'ADD_OP':([11,12,13,17,21,23,25,26,27,],[19,-11,-12,19,19,19,19,19,-13,]),'MUL_OP':([11,12,13,17,21,23,25,26,27,],[20,-11,-12,20,20,20,20,20,-13,]),')':([12,13,21,22,23,25,26,27,31,],[-11,-12,27,28,-9,-14,-15,-13,-10,]),',':([12,13,23,25,26,27,],[-11,-12,29,-14,-15,-13,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'programme':([0,9,18,],[1,16,24,]),'statement':([0,9,18,],[2,2,2,]),'assignement':([0,9,18,],[3,3,3,]),'while':([0,9,18,],[4,4,4,]),'block':([0,9,18,],[5,5,5,]),'expression':([7,10,14,15,19,20,29,],[11,17,21,23,25,26,23,]),'listP':([15,29,],[22,31,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> programme","S'",1,None,None,None),
  ('programme -> statement','programme',1,'p_programme','parser.py',16),
  ('programme -> statement ; programme','programme',3,'p_programme','parser.py',17),
  ('statement -> assignement','statement',1,'p_statement','parser.py',24),
  ('statement -> while','statement',1,'p_statement','parser.py',25),
  ('statement -> block','statement',1,'p_statement','parser.py',26),
  ('assignement -> IDENTIFIER = expression','assignement',3,'p_assignement','parser.py',30),
  ('while -> WHILE expression { programme }','while',5,'p_while','parser.py',35),
  ('block -> BLOCKNAME ( listP )','block',4,'p_block','parser.py',39),
  ('listP -> expression','listP',1,'p_listP','parser.py',43),
  ('listP -> expression , listP','listP',3,'p_listP','parser.py',44),
  ('expression -> NUMBER','expression',1,'p_expression_num_or_var','parser.py',59),
  ('expression -> IDENTIFIER','expression',1,'p_expression_num_or_var','parser.py',60),
  ('expression -> ( expression )','expression',3,'p_expression_paren','parser.py',64),
  ('expression -> expression ADD_OP expression','expression',3,'p_expression_op','parser.py',68),
  ('expression -> expression MUL_OP expression','expression',3,'p_expression_op','parser.py',69),
]
