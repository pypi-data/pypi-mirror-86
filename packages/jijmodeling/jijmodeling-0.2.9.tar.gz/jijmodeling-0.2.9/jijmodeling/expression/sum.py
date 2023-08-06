
from jijmodeling.expression.from_serializable import from_serializable
from jijmodeling.expression.expression import Add, Expression, _latex_repr

class Sum(Expression):
    """Class that represents the sum.

    Args:
        indices (dict): subscript to take the sum.
        term (:class:`Expression`): term to be summed.

    Attributes:
        indices (dict): subscript to take the sum.
        index_set (list): set of indices.
        condition (:class:`Condition`): conditions of summation.

    Example:
        Create :math:`\sum_{i=0}^n d_i x_i`

        >>> from jijmodeling import PlaceholderArray, BinaryArray, Sum
        >>> d = PlaceholderArray('d', dim=1)
        >>> n = d.shape[0]
        >>> x = BinaryArray('x', shape=n)
        >>> Sum({'i': n}, d['i']*x['i'])
        Σ_{i}(d[i]x[i])

    """
    def __init__(self, indices: dict, term, condition=None):
        super().__init__(children=[term])
        
        self.indices = indices
        def extract_index(ind):
            if isinstance(ind, str):
                return ind.split(' ')[0]
            return ind
        index_keys = [extract_index(ind) for ind in indices.keys()]
        self.index_set = [ind for ind in self.index_set if ind not in index_keys]
        # The boundary condition of the sum index may depend on the outer index, 
        # so check it and add it to index_set.
        from jijmodeling.variables.element import Element
        for _ind_bound in indices.values():
            ind_bound = _ind_bound if isinstance(_ind_bound, tuple) else (_ind_bound, )
            for ind_b in ind_bound:
                if isinstance(ind_b, Expression):
                    self.index_set = self.index_set + ind_b.index_set
        self.index_set = list(set(self.index_set))
        self.condition = condition

    def __repr__(self):
        repr_str = 'Σ_{'
        for i in self.indices.keys():
            repr_str += str(i) + ', '
        term = self.children[0]
        repr_str = repr_str[:-2] + '}}({})'.format(term.__repr__()) 
        return repr_str

    def __make_latex__(self):
        ind_str = ""
        ind_end = ""
        for ind, ind_set in self.indices.items():
            ind_latex = _latex_repr(ind)
            ind_conds = []
            if len(ind_latex.split(' ')) == 3:
                ind_conds = ind_latex.split(' ')[1:]
                ind_latex = ind_latex.split(' ')[0]
            from jijmodeling.variables.array import Array
            if isinstance(ind_set, Array):
                ind_str += "{} \in {}, ".format(ind_latex, _latex_repr(ind_set))
            elif isinstance(ind_set, tuple):
                iset0 = _latex_repr(ind_set[0])
                ind_end += _latex_repr(ind_set[1]) + '- 1' + ", "
                ind_str += "{} = {}".format(ind_latex, iset0) + ", "
            else:
                ind_end += _latex_repr(ind_set) + '- 1' + ", "
                ind_str += "{} = 0".format(ind_latex) + ", "

            if len(ind_conds) > 0:
                cond_latex = {'!=': '\\neq', '==': '=', '<=': '\leq', '>=': '\geq', '<': '<', '>': '>'}
                ind_str = ind_str[:-2]
                ind_str += '({} {} {}), '.format(ind_latex, cond_latex[ind_conds[0]], ind_conds[1])

        if isinstance(self.children[0], Add):
            term = _latex_repr(self.children[0])
        else:
            term = _latex_repr(self.children[0], False)

        return  "\sum_{{{}}}^{{{}}} {}".format(ind_str[:-2], ind_end[:-2], term)
        

    @classmethod
    def from_serializable(cls, serializable: dict):
        indices:dict = from_serializable(serializable['attributes']['indices'])
        term = from_serializable(serializable['attributes']['children'])[0]
        return cls(indices, term)