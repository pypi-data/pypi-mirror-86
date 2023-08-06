"""
This module contains an abstract parent class, defining the minimum functions that all factors should have
"""

from abc import ABCMeta, abstractmethod
import copy

from veroku.factors import _factor_utils


class Factor:
    """
    An abstract parent class.
    """
    __metaclass__ = ABCMeta

    def __init__(self, var_names):
        """
        A super class constructor that should be called from the base class constructor.
        Variable sets explanation:
        #TODO: expand explanation.
        """
        if len(set(var_names)) != len(var_names):
            raise ValueError('duplicate variables in var_names: ', var_names)
        self._var_names = _factor_utils.make_list(var_names)
        self._dim = len(var_names)

    @property
    def var_names(self):
        """
        Get the factor's variable names.
        :return: the var_names parameter.
        """
        return copy.deepcopy(self._var_names)

    @property
    def dim(self):
        """
        Get the factor's dimensionality.
        :return: the dim parameter.
        """
        return self._dim

    def get_marginal_vars(self, vrs, keep=False):
        """
        A helper function (for marginalize) that returns the variables that should be marginalised out (keep=False)
        or kept (keep=True).
        :param vrs: (list) the variables
        :param keep: Whether these variables are to be kept or summed out.
        :return: The variables to be kept or summed out.
        """
        if keep:
            return vrs.copy()
        return list(set(self.var_names) - set(vrs))

    @abstractmethod
    def copy(self):
        """
        An abstract function for copying a factor that should be implemented in the base class.
        :return: a copy of the factor
        """

    @abstractmethod
    def marginalize(self, vrs, keep=False):
        """
        An abstract function for performing factor marginalisation that should be implemented in the base class.
        :return: the resulting marginal factor.
        :param vrs: (list) a subset of variables in the factor's scope
        :param keep: Whether to keep or sum out vrs
        :return: The resulting factor marginal.
        """

    @abstractmethod
    def multiply(self, factor):
        """
        An abstract function for performing factor multiplication that should be implemented in the base class.
        :param factor: The factor to be multiplied with.
        :return: The resulting product
        """

    def absorb(self, factor):
        return self.multiply(factor)

    @abstractmethod
    def divide(self, factor):
        """
        An abstract function for performing factor division that should be implemented in the base class.
        :param factor: The factor to be divided by.
        :return: The resulting quotient
        """
    def cancel(self, factor):
        return self.divide(factor)

    @abstractmethod
    def reduce(self, vrs, values):
        """
        An abstract function for performing the observation (a.k.a conditioning) operation that should be implemented
        in the base class.
        :return: the resulting reduced factor.
        :param vrs: (list) a subset of variables in the factor's scope
        :param values: The values of vars.
        :return: The resulting reduced factor.
        """
    def observe(self, vrs, values):
        return self.reduce(vrs, values)

    @abstractmethod
    def normalize(self):
        """
        An abstract function for performing factor normalization that should be implemented in the base class.
        :return: The normalized factor.
        """
    #@property
    #def is_vacuous(self):
    #    return False

    @abstractmethod
    def show(self):
        """
        An abstract function for printing the parameters of the factor that should be implemented in the base class.
        """

    @property
    def joint_distribution(self):
        return self.copy()

    def __mul__(self, other):
        return self.multiply(other)

    def __div__(self, other):
        return self.divide(other)

    def __eq__(self, other):
        return self.equals(other)

    def __ne__(self, other):
        return not self.__eq__(other)

