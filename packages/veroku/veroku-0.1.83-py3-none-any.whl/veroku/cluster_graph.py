from IPython.core.display import Image, display
from graphviz import Graph
import networkx as nx
import numpy as np
from tqdm.auto import tqdm
import pandas as pd
from graphviz import Source

from veroku._cg_helpers._cluster import Cluster
import veroku._cg_helpers._animation as cg_animation
from veroku.factors._factor_utils import get_subset_evidence
import matplotlib.pyplot as plt
import collections

# TODO: optimise _pass_message
# TODO: improve sepsets selection for less loopiness
# TODO: Optimisation: messages from clusters that did not receive any new messages in the previous round, do not need
#  new messages calculated.


# TODO: consider removing this
def sort_almost_sorted(a_deque, key):
    """
    Sort a deque like that where only the first element is potentially unsorted
    and should probably be last and the rest of the deque is sorted in descending order.
    """
    a_deque.append(a_deque.popleft())
    if key(a_deque[-1]) <= key(a_deque[-2]):
        return a_deque
    a_deque = collections.deque(sorted(a_deque, key=key, reverse=True))
    return a_deque


def _evidence_reduce_factors(factors, evidence):
    """
    Observe relevant evidence for each factor.
    :param factors:
    :param evidence:
    :return:
    """
    reduced_factors = []
    for i, factor in enumerate(factors):
        if evidence is not None:
            vrs, values = get_subset_evidence(all_evidence_dict=evidence,
                                              subset_vars=factor.var_names)
            if len(vrs) > 0:
                factor = factor.reduce(vrs, values)
        reduced_factors.append(factor.copy())
    return reduced_factors


def make_factor_name(factor):
    return str(factor.var_names).replace("'", '')


def _absorb_subset_factors(factors):
    """
    Absorb any factors that has a scope that is a subset of another factor into such a factor.
    :param factors:
    :return:
    """
    factors_absorbtion_dict = {i: [] for i in range(len(factors))}
    final_graph_cluster_factors = []
    # factors: possibly smaller list of factors after factors which have a scope that is a subset of another factor have
    # been absorbed by the larger one.
    factor_processed_mask = [0] * len(factors)
    for i, factor_i in enumerate(factors):
        if not factor_processed_mask[i]:
            factor_product = factor_i.copy()
            for j, factor_j in enumerate(factors):
                if i != j:
                    if not factor_processed_mask[j]:
                        if set(factor_j.var_names) < set(factor_product.var_names):
                            try:
                                factor_product = factor_product.multiply(factor_j)
                                factors_absorbtion_dict[i].append(j)
                                factor_processed_mask[j] = 1
                                factor_processed_mask[i] = 1
                            except NotImplementedError:
                                print(f'Warning: could not multiply {type(factor_product)} with {type(factor_j)} (Not Implemented)')
            if factor_processed_mask[i]:
                final_graph_cluster_factors.append(factor_product)
    for i, factor_i in enumerate(factors):  # add remaining factors
        if not factor_processed_mask[i]:
            factor_processed_mask[i] = 1
            final_graph_cluster_factors.append(factor_i)
    assert all(factor_processed_mask), 'Error: Some factors where not included during variable subset processing.'
    return final_graph_cluster_factors


def _make_subset_factor_df(subset_dict):
    """
    Make a ...
    :param subset_dict: (dict) A dictionary mapping factors to factors that have subset scopes
    :return:
    """
    keys = list(subset_dict.keys())
    values = list(subset_dict.values())
    assert(len(keys) == len(values))
    # TODO: This raises different list lengths warning (see below). Investigate this.
    #   VisibleDeprecationWarning: Creating an ndarray from ragged nested sequences...
    data = np.array([keys, values]).T
    df = pd.DataFrame(columns=['factor_index', 'subfactor_indices'],
                      data=data)
    df['num_subfactors'] = df['subfactor_indices'].apply(lambda x: len(x))
    df.sort_values(by='num_subfactors', inplace=True, ascending=False)
    return df


class ClusterGraph(object):
    
    def __init__(self, factors, evidence=None, special_evidence=dict(),
                 make_animation_gif=False, disable_tqdm=False, verbose=False):
        """
        Construct a Cluster graph from a list of factors
        :param factors: (list of factors) The factors to construct the graph from
        :param evidence: (dict) evidence dictionary (mapping variable names to values) that should be used to reduce
            factors before building the cluster graph.
        :param special_evidence: (dict) evidence dictionary (mapping variable names to values) that should be used in
            the calculation of messages, and not to reduce factors. This allows factor approximations - such as the
            non-linear Gaussian to be iteratively refined.
        """
        # TODO: see if evidence and special_evidence can be replaced by a single variable.
        self.num_messages_passed = 0
        self.make_animation_gif = make_animation_gif
        self.special_evidence = special_evidence
        self.disable_tqdm = disable_tqdm
        self.last_passed_message_factors_dict = dict()
        self.verbose = verbose
        # new
        self.last_sent_message_dict = {}  # {(rec_cluster_id1, rec_cluster_id1): msg1, ...}

        self.sync_message_passing_max_distances = []

        all_evidence_vars = set(self.special_evidence.keys())
        if evidence is not None:
            evidence_vars = set(evidence.keys())
            all_evidence_vars = all_evidence_vars.union(evidence_vars)
        all_factors_copy = _evidence_reduce_factors(factors, evidence)
        final_graph_cluster_factors = _absorb_subset_factors(all_factors_copy)

        clusters = [Cluster(factor, cluster_name_prefix=f'c{i}#') for i, factor in
                    enumerate(final_graph_cluster_factors)]

        self._set_non_rip_sepsets_dict(clusters, all_evidence_vars)
        self._clusters = clusters

        # Add special evidence to factors
        for cluster in self._clusters:
            cluster_special_evidence_vars, cluster_special_evidence_values = get_subset_evidence(self.special_evidence, cluster.var_names)
            cluster_special_evidence = dict(zip(cluster_special_evidence_vars, cluster_special_evidence_values))
            cluster.add_special_evidence(cluster_special_evidence)

        self.graph_message_paths = collections.deque([])
        self._build_graph()

        # TODO: consolidate these two, if possible
        self.message_passing_log_df = None
        self.message_passing_animation_frames = []

    def _set_non_rip_sepsets_dict(self, clusters, all_evidence_vars):
        """
        Calculate the preliminary sepsets dict before the RIP property is enforced.
        :param clusters:
        :param all_evidence_vars:
        :return:
        """
        self._non_rip_sepsets = {}
        for i in tqdm(range(len(clusters)), disable=self.disable_tqdm):
            vars_i = clusters[i].var_names
            for j in range(i + 1, len(clusters)):
                vars_j = clusters[j].var_names
                sepset = set(vars_j).intersection(set(vars_i)) - all_evidence_vars
                self._non_rip_sepsets[(i, j)] = sepset
                self._non_rip_sepsets[(j, i)] = sepset

    def _build_graph(self):
        """
        Add the cluster sepsets, graphviz graph and animation graph (for message_passing visualisation).
        """
        # Check for non-unique cluster_ids (This should never be the case)
        cluster_ids = [cluster.cluster_id for cluster in self._clusters]
        if len(set(cluster_ids)) != len(cluster_ids):
            raise ValueError(f'Non-unique cluster ids: {cluster_ids}')

        self._conditional_print('Info: Building graph.')
        self._graph = Graph(format='png')
        rip_sepsets_dict = self._get_running_intersection_sepsets()

        # TODO: see why this is necessary, remove if not
        for i in tqdm(range(len(self._clusters)), disable=self.disable_tqdm):
            self._clusters[i].remove_all_neighbours()

        self._conditional_print(f'Debug: number of clusters: {len(self._clusters)}')
        for i in tqdm(range(len(self._clusters)), disable=self.disable_tqdm):

            node_i_name = self._clusters[i]._cluster_id
            self._graph.node(name=node_i_name, label=node_i_name, style='filled', fillcolor='white', color='black')
            for j in range(i + 1, len(self._clusters)):

                if (i, j) in rip_sepsets_dict:
                    sepset = rip_sepsets_dict[(i, j)]
                    assert len(sepset) > 0, 'Error: empty sepset'
                    self._clusters[i].add_neighbour(self._clusters[j], sepset=sepset)
                    self._clusters[j].add_neighbour(self._clusters[i], sepset=sepset)

                    gmp_ij = _GraphMessagePath(self._clusters[i], self._clusters[j])
                    gmp_ji = _GraphMessagePath(self._clusters[j], self._clusters[i])
                    self.graph_message_paths.append(gmp_ij)
                    self.graph_message_paths.append(gmp_ji)
                    self._clusters[i].add_outward_message_path(gmp_ij)
                    self._clusters[j].add_outward_message_path(gmp_ji)

                    # Graph animation
                    node_j_name = self._clusters[j]._cluster_id
                    sepset_node_label = ','.join(sepset)
                    sepset_node_name = cg_animation.make_sepset_node_name(node_i_name, node_j_name)
                    self._graph.node(name=sepset_node_name, label=sepset_node_label, shape='rectangle')
                    self._graph.edge(node_i_name, sepset_node_name, color='black', penwidth='2.0')
                    self._graph.edge(sepset_node_name, node_j_name, color='black', penwidth='2.0')
        print('num self.graph_message_paths: ', len(self.graph_message_paths))

    def _conditional_print(self, message):
        if self.verbose:
            print(message)

    def plot_next_messages_info_gain(self, legend_on=False, figsize=[15, 5]):
        """
        Plot the information gained by a receiving new messages over sebsequent iterations for all message paths in the
            graph.
        :param bool legend_on: Whether or not to show the message paths (specified by connected cluster pairs) in the
            plot legend.
        :param list figsize: The matplotlib figure size.
        """
        plt.figure(figsize=figsize)
        all_paths_information_gains_with_iters = [gmp.information_gains_with_iters for gmp in self.graph_message_paths]
        for paths_information_gains_with_iters in all_paths_information_gains_with_iters:
            plt.plot(paths_information_gains_with_iters)
        plt.title('Information Gain of Messages along Graph Message Paths')
        plt.xlabel('iteration')
        plt.ylabel('D_KL(prev_msg||msg)')
        if legend_on:
            legend = [f"{gmp.sender_cluster.cluster_id}->{gmp.receiver_cluster.cluster_id}" for gmp in
                      self.graph_message_paths]
            plt.legend(legend)

    def plot_message_convergence(self, log=False, figsize=[15, 5]):
        """
        Plot the the KL-divergence between the messages and their previous instances to indicate the message passing
        convergence.
        """

        mp_max_dists = self.sync_message_passing_max_distances
        if log:
            mp_max_dists = np.log(mp_max_dists)
        from matplotlib.lines import Line2D
        # here we tile an flatten to prevent the plot omission of values with inf on either side.
        mp_max_dists = np.tile(mp_max_dists, [2, 1]).flatten(order='F')
        num_iterations = len(mp_max_dists)

        iterations = np.array(list(range(num_iterations))) / 2  # divide by 2 to correct for tile and flatten
        non_inf_max_distances = [d for d in mp_max_dists if d != np.inf]
        max_non_inf = max(non_inf_max_distances)
        new_inf_value = max_non_inf * 1.5
        max_distances_replaces_infs = np.array([v if v != np.inf else new_inf_value for v in mp_max_dists])
        inf_values = np.ma.masked_where(max_distances_replaces_infs != new_inf_value, max_distances_replaces_infs)
        plt.figure(figsize=figsize)
        plt.plot(iterations, max_distances_replaces_infs)
        plt.plot(iterations, inf_values, c='r', linewidth=2)
        if len(non_inf_max_distances) != len(mp_max_dists):
            custom_lines = [Line2D([0], [0], color='r', lw=4)]
            plt.legend(custom_lines, ['infinity'])
        plt.title('Message Passing Convergence')
        plt.xlabel('iteration')
        plt.ylabel('log max D_KL(prev_msg||msg)')
        plt.show()

    def _get_unique_vars(self):
        all_vars = []
        for cluster in self._clusters:
            all_vars += (cluster.var_names)
        unique_vars = list(set(all_vars))
        return unique_vars

    def _get_vars_min_spanning_trees(self):
        all_vars = self._get_unique_vars()
        var_graphs = {var: nx.Graph() for var in all_vars}
        num_clusters = len(self._clusters)
        for i in range(num_clusters):
            for j in range(i + 1, num_clusters):
                sepset = self._non_rip_sepsets[(i, j)]
                for var in sepset:
                    var_graphs[var].add_edge(i, j, weight=1)
        var_spanning_trees = dict()
        for var in all_vars:
            var_graph = var_graphs[var]
            var_spanning_trees[var] = nx.minimum_spanning_tree(var_graph)
        return var_spanning_trees

    def _get_running_intersection_sepsets(self):
        edge_sepset_dict = {}
        unique_vars = self._get_unique_vars()
        min_span_trees = self._get_vars_min_spanning_trees()
        self._conditional_print("Info: Getting unique variable spanning trees.")
        for i in tqdm(range(len(unique_vars)), disable=self.disable_tqdm):
            var = unique_vars[i]
            min_span_tree = min_span_trees[var]
            for edge in min_span_tree.edges():
                if edge in edge_sepset_dict:
                    edge_sepset_dict[edge].append(var)
                else:
                    edge_sepset_dict[edge] = [var]
        return edge_sepset_dict

    def show(self):
        """
        Show the cluster graph.
        """
        self._graph.render('/tmp/test.gv', view=False)
        image = Image('/tmp/test.gv.png')
        display(image)

    def save_graph_image(self, filename):
        """
        Save image of the graph.
        :param filename: The filename of the file.
        """
        # Source(self._graph, filename="/tmp/test.gv", format="png")
        Source(self._graph, filename=filename, format="png")

    def get_marginal(self, vrs):
        """
        Search the graph for a specific variable and get that variables marginal (posterior marginal if process_graph
        has been run previously).
        :return: The marginal
        """
        for cluster in self._clusters:
            if set(vrs) <= set(cluster.var_names):
                factor = cluster._factor.copy()
                evidence_vrs, evidence_values = get_subset_evidence(self.special_evidence, factor.var_names)
                if len(evidence_vrs) > 0:
                    factor = factor.reduce(evidence_vrs, evidence_values)
                marginal = factor.marginalize(vrs, keep=True)
                return marginal
        raise ValueError(f'No cluster with variables containing {vrs}')

    def get_posterior_joint(self):
        """
        Get the posterior joint distribution.
        """
        # TODO: add functionality for efficiently getting a posterior marginal over any subset of variables and replace
        #  the get_marginal function above.
        cluster_product = self._clusters[0]._factor.joint_distribution
        for cluster in self._clusters[1:]:
            cluster_product = cluster_product.multiply(cluster._factor.joint_distribution)
        last_passed_message_factors = list(self.last_passed_message_factors_dict.values())
        if len(last_passed_message_factors) == 0:
            assert self.num_messages_passed == 0
            return cluster_product
        message_product = last_passed_message_factors[0]
        for message_factor in last_passed_message_factors[1:]:
            message_product = message_product.multiply(message_factor)
        joint = cluster_product.cancel(message_product)
        return joint

    def process_graph(self, tol=1e-3, max_iter=50, debug=False):
        """
        Perform synchronous message passing until convergence (or maximum iterations).
        """

        # for debugging and testing
        self.messages_passed = []

        self.sync_message_passing_max_distances = []
        if len(self._clusters) == 1:
            # The Cluster Graph contains only single cluster. Message passing not possible or necessary.
            self._clusters[0]._factor = self._clusters[0]._factor.reduce(vrs=self.special_evidence.keys(),
                                                                         values=self.special_evidence.values())
            return

        # TODO: see if the definition of max_iter can be improved
        key_func = lambda x: x.next_information_gain
        max_message_passes = max_iter*len(self.graph_message_paths)

        self.graph_message_paths = collections.deque(sorted(self.graph_message_paths, key=key_func, reverse=True))

        for _ in tqdm(range(max_message_passes), disable=self.disable_tqdm):
            sender_cluster_id = self.graph_message_paths[0].sender_cluster.cluster_id
            receiver_cluster_id = self.graph_message_paths[0].receiver_cluster.cluster_id

            # for debugging and testing
            if debug:
                self.messages_passed.append(self.graph_message_paths[0].next_message.copy())
                data = [(gmp.sender_cluster._cluster_id, gmp.receiver_cluster._cluster_id, gmp.next_information_gain) for
                        gmp in self.graph_message_paths]
                df = pd.DataFrame(data=data, columns=['sender', 'receiver', 'info'])

            self.graph_message_paths[0].pass_next_message()
            self.graph_message_paths = collections.deque(sorted(self.graph_message_paths, key=key_func, reverse=True))
            # self.graph_message_paths = sort_almost_sorted(self.graph_message_paths, key=key_func)

            max_next_information_gain = self.graph_message_paths[0].next_information_gain
            self.sync_message_passing_max_distances.append(max_next_information_gain)
            if max_next_information_gain <= tol:
                return

            if self.make_animation_gif:
                cg_animation.add_message_pass_animation_frames(graph=self._graph,
                                                               frames=self.message_passing_animation_frames,
                                                               node_a_name=sender_cluster_id,
                                                               node_b_name=receiver_cluster_id)

    def _make_message_passing_animation_gif(self):
        print('Making message passing animation.')
        self.message_passing_animation_frames[0].save(fp='./graph_animation.gif',
                                                      format='GIF',
                                                      append_images=self.message_passing_animation_frames[1:],
                                                      save_all=True, duration=400, loop=0)


class _GraphMessagePath:
    """
    A specific path (direction along an edge) in a graph along which a message can be passed.
    """
    def __init__(self, sender_cluster, receiver_cluster):
        """
        The initialiser.
        :param sender_cluster: The cluster that defines the starting point of the path.
        :param receiver_cluster: The cluster that defines the end point of the path.
        """
        self.sender_cluster = sender_cluster
        self.receiver_cluster = receiver_cluster
        self.previously_sent_message = None
        self.next_message = self.sender_cluster.make_message(self.receiver_cluster._cluster_id)
        self.next_information_gain = None
        self.information_gains_with_iters = []
        self.update_next_information_gain()

    def update_next_information_gain(self):
        if self.previously_sent_message is None:
            self.next_information_gain = self.next_message.distance_from_vacuous()
        else:
            # "In the context of machine learning, KL(P||Q) is often called the information gain achieved if Q is
            # used instead of P." - wikipedia
            # We typically want to know which new message (Q) will result in the largest information gain if it replaces
            # the message (P)
            # message: previous_message (P)
            # factor: next message (Q)
            # P.kl_divergence(Q)
            self.next_information_gain = self.previously_sent_message.kl_divergence(self.next_message)
        self.information_gains_with_iters.append(self.next_information_gain)

    def recompute_next_message(self):
        """
        Recompute the next message.
        """
        new_next_message = self.sender_cluster.make_message(self.receiver_cluster._cluster_id)
        self.next_message = new_next_message.copy()
        self.update_next_information_gain()

    def pass_next_message(self):
        """
        Pass the next message along this path.
        """
        self.receiver_cluster.receive_message(self.next_message)
        # we 'recompute' the next message - but it will be the same
        self.previously_sent_message = self.next_message.copy()
        self.next_information_gain = 0.0
        self.information_gains_with_iters.append(self.next_information_gain)

        for gmp in self.receiver_cluster._outward_message_paths:
            gmp.recompute_next_message()
