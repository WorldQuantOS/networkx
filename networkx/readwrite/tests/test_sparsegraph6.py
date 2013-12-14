#!/usr/bin/env python
from nose.tools import *
import networkx as nx
import networkx.readwrite.sparsegraph6 as sg6
import os,tempfile

class TestGraph6Utils(object):

    def test_n_data_n_conversion(self):
        for i in [0, 1, 42, 62, 63, 64, 258047, 258048, 7744773, 68719476735]:
            assert_equal(sg6.data_to_n(sg6.n_to_data(i))[0], i)
            assert_equal(sg6.data_to_n(sg6.n_to_data(i))[1], [])
            assert_equal(sg6.data_to_n(sg6.n_to_data(i) + [42, 43])[1],
                         [42, 43])

    def test_data_sparse6_data_conversion(self):
        for data in [[], [0], [63], [63, 63], [0]*42,
                     [0, 1, 62, 42, 3, 11, 0, 11]]:
            assert_equal(sg6.graph6_to_data(sg6.data_to_graph6(data)), data)
            assert_equal(len(sg6.data_to_graph6(data)), len(data))


class TestGraph6(object):

    def test_parse_graph6(self):
        data="""DF{"""
        G=nx.parse_graph6(data)
        assert_equal(sorted(G.nodes()),[0, 1, 2, 3, 4])
        assert_equal([e for e in sorted(G.edges())],
                     [(0, 3), (0, 4), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)])

    def test_read_graph6(self):
        data="""DF{"""
        G=nx.parse_graph6(data)
        (fd,fname)=tempfile.mkstemp()
        fh=open(fname,'w')
        b=fh.write(data)
        fh.close()
        Gin=nx.read_graph6(fname)
        assert_equal(sorted(G.nodes()),sorted(Gin.nodes()))
        assert_equal(sorted(G.edges()),sorted(Gin.edges()))
        os.close(fd)
        os.unlink(fname)

    def test_read_many_graph6(self):
        # Read many graphs into list
        data="""DF{\nD`{\nDqK\nD~{\n"""
        (fd,fname)=tempfile.mkstemp()
        fh=open(fname,'w')
        b=fh.write(data)
        fh.close()
        glist=nx.read_graph6_list(fname)
        assert_equal(len(glist),4)
        for G in glist:
            assert_equal(sorted(G.nodes()),[0, 1, 2, 3, 4])
        os.close(fd)
        os.unlink(fname)

    def test_generate_graph6(self):
        assert_equal(nx.generate_graph6(nx.empty_graph(0)), '>>graph6<<?')
        assert_equal(nx.generate_graph6(nx.empty_graph(1)), '>>graph6<<@')

        G1 = nx.complete_graph(4)
        assert_equal(nx.generate_graph6(G1, header=True), '>>graph6<<C~')
        assert_equal(nx.generate_graph6(G1, header=False), 'C~')

        G2 = nx.complete_bipartite_graph(6,9)
        assert_equal(nx.generate_graph6(G2, header=False),
                     'N??F~z{~Fw^_~?~?^_?') # verified by Sage

        G3 = nx.complete_graph(67)
        assert_equal(nx.generate_graph6(G3, header=False),
                     '~?@B' + '~' * 368 + 'w')

    def test_write_graph6(self):
        try:
            (fd, fname) = tempfile.mkstemp()
            os.close(fd)
            G = nx.complete_bipartite_graph(6,9)
            nx.write_graph6(G, fname)

            fh = open(fname,'rt')
            data = fh.read()
            fh.close()
            assert_equal(data, '>>graph6<<N??F~z{~Fw^_~?~?^_?\n')

        finally:
            os.unlink(fname)

    def test_write_many_graph6(self):
        try:
            (fd, fname) = tempfile.mkstemp()
            os.close(fd)
            Gs = [nx.complete_bipartite_graph(i, i + 1) for i in [0, 1, 3, 5]]
            nx.write_graph6_list(Gs, fname, header=False)

            fh = open(fname,'rt')
            data = fh.read()
            fh.close()
            assert_equal(data, '@\nBo\nFFzf?\nJ?B~vrw}Fo?\n')

        finally:
            os.unlink(fname)

    def test_generate_and_parse_graph6(self):
        for i in list(range(13)) + [31, 47, 62, 63, 64, 72]:
            g = nx.random_graphs.gnm_random_graph(i, i * i // 4, seed=i)
            gstr = nx.generate_graph6(g, header=False)
            assert_equal(len(gstr),
                         ((i-1) * i // 2 + 5) // 6 + (1 if i < 63 else 4))
            g2 = nx.parse_graph6(gstr)
            assert_equal(g2.order(), g.order())
            assert_equal(sorted(g2.edges()), sorted(g.edges()))

    @raises(nx.NetworkXError)
    def directed_error(self):
        nx.generate_graph6(nx.DiGraph())


class TestSparseGraph6(object):

    def test_parse_sparse6(self):
        data=""":Q___eDcdFcDeFcE`GaJ`IaHbKNbLM"""
        G=nx.parse_sparse6(data)
        assert_equal(sorted(G.nodes()),
                     [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                      10, 11, 12, 13, 14, 15, 16, 17])
        assert_equal([e for e in sorted(G.edges())],
                     [(0, 1), (0, 2), (0, 3), (1, 12), (1, 14), (2, 13),
                      (2, 15), (3, 16), (3, 17), (4, 7), (4, 9), (4, 11),
                      (5, 6), (5, 8), (5, 9), (6, 10), (6, 11), (7, 8),
                      (7, 10), (8, 12), (9, 15), (10, 14), (11, 13),
                      (12, 16), (13, 17), (14, 17), (15, 16)])


    def test_read_sparse6(self):
        data=""":Q___eDcdFcDeFcE`GaJ`IaHbKNbLM"""
        G=nx.parse_sparse6(data)
        (fd,fname)=tempfile.mkstemp()
        fh=open(fname,'w')
        b=fh.write(data)
        fh.close()
        Gin=nx.read_sparse6(fname)
        assert_equal(sorted(G.nodes()),sorted(Gin.nodes()))
        assert_equal(sorted(G.edges()),sorted(Gin.edges()))
        os.close(fd)
        os.unlink(fname)

    def test_read_many_graph6(self):
        # Read many graphs into list
        data=""":Q___eDcdFcDeFcE`GaJ`IaHbKNbLM\n:Q___dCfDEdcEgcbEGbFIaJ`JaHN`IM"""
        (fd,fname)=tempfile.mkstemp()
        fh=open(fname,'w')
        b=fh.write(data)
        fh.close()
        glist=nx.read_sparse6_list(fname)
        assert_equal(len(glist),2)
        for G in glist:
            assert_equal(sorted(G.nodes()),
                         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                          10, 11, 12, 13, 14, 15, 16, 17])
        os.close(fd)
        os.unlink(fname)

    def test_generate_sparse6(self):
        # Checked against sage encoder
        assert_equal(nx.generate_sparse6(nx.empty_graph(0)), '>>sparse6<<:?')
        assert_equal(nx.generate_sparse6(nx.empty_graph(1)), '>>sparse6<<:@')
        assert_equal(nx.generate_sparse6(nx.empty_graph(5)), '>>sparse6<<:D')
        assert_equal(nx.generate_sparse6(nx.empty_graph(68)),
                     '>>sparse6<<:~?@C')
        assert_equal(nx.generate_sparse6(nx.empty_graph(258049)),
                     '>>sparse6<<:~~???~?@')

        G1 = nx.complete_graph(4)
        assert_equal(nx.generate_sparse6(G1, header=True),
                     '>>sparse6<<:CcKI')
        assert_equal(nx.generate_sparse6(G1, header=False), ':CcKI')

        # Padding testing
        assert_equal(nx.generate_sparse6(nx.path_graph(4), header=False),
                     ':Cdv')
        assert_equal(nx.generate_sparse6(nx.path_graph(5), header=False),
                     ':DaYn')
        assert_equal(nx.generate_sparse6(nx.path_graph(6), header=False),
                     ':EaYnN')
        assert_equal(nx.generate_sparse6(nx.path_graph(7), header=False),
                     ':FaYnL')
        assert_equal(nx.generate_sparse6(nx.path_graph(8), header=False),
                     ':GaYnLz')

    def test_write_sparse6(self):
        try:
            (fd, fname) = tempfile.mkstemp()
            os.close(fd)
            G = nx.complete_bipartite_graph(6,9)
            nx.write_sparse6(G, fname)

            fh = open(fname,'rt')
            data = fh.read()
            fh.close()
            assert_equal(data,
                         '>>sparse6<<:Nk?G`cJ?G`cJ?G`cJ?G`'+
                         'cJ?G`cJ?G`cJ?G`cJ?G`cJ?G`cJ\n')
            # Compared with sage

        finally:
            os.unlink(fname)

    def test_write_many_sparse6(self):
        try:
            (fd, fname) = tempfile.mkstemp()
            os.close(fd)
            Gs = [nx.complete_bipartite_graph(i, i + 1)
                  for i in [0, 1, 2, 3, 5]]
            nx.write_sparse6_list(Gs, fname, header=False)

            fh = open(fname,'rt')
            data = fh.read()
            fh.close()
            assert_equal(data,
                         ':@\n:Bc\n:Dg@_WF\n:Fk@I@I@I@J\n:Ji?G`'+
                         'c_COqOAGXG@CKc?aEQ?PBH\n')
            # Compared with sage

        finally:
            os.unlink(fname)

    def test_generate_and_parse_sparse6(self):
        for i in list(range(13)) + [31, 47, 62, 63, 64, 72]:
            m = min(2 * i, i * i // 2)
            g = nx.random_graphs.gnm_random_graph(i, m, seed=i)
            gstr = nx.generate_sparse6(g, header=False)
            g2 = nx.parse_sparse6(gstr)
            assert_equal(g2.order(), g.order())
            assert_equal(sorted(g2.edges()), sorted(g.edges()))

    @raises(nx.NetworkXError)
    def directed_error(self):
        nx.generate_sparse6(nx.DiGraph())
