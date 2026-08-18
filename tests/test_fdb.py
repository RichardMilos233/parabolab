"""Faa di Bruno combinatorics: known counts + golden cross-check against
the authors' deep_branching/fdb.py."""

import pathlib
import sys

import pytest

from parabolab.fdb import fdb_terms

AUTHORS_REPO = pathlib.Path("/Users/michael/Desktop/NTU/fyp/deep_branching")


def test_single_argument_counts_are_partition_numbers():
    # one inner function: terms <-> integer partitions of k
    for k, p in [(1, 1), (2, 2), (3, 3), (4, 5), (5, 7), (6, 11)]:
        assert len(fdb_terms(1, k)) == p


def test_single_argument_coeffs_sum_to_bell_numbers():
    # sum of coefficients = number of set partitions (Bell numbers)
    for k, bell in [(1, 1), (2, 2), (3, 5), (4, 15), (5, 52)]:
        assert sum(t.coeff for t in fdb_terms(1, k)) == bell


def test_term_invariants():
    for m, k in [(2, 3), (3, 2), (5, 4)]:
        for term in fdb_terms(m, k):
            assert term.coeff >= 1
            assert len(term.lam) == m
            # lam counts blocks per argument
            assert sum(term.lam) == sum(mult for _, _, mult in term.blocks)
            # block sizes weighted by multiplicity sum to k
            assert sum(l * mult for l, _, mult in term.blocks) == k
            assert all(mult >= 1 and l >= 1 and 0 <= q < m
                       for l, q, mult in term.blocks)


def _normalize_ours(terms):
    return sorted((t.coeff, t.lam, t.blocks) for t in terms)


def _normalize_theirs(terms):
    out = []
    for t in terms:
        blocks = []
        for ll, k_arr in t.l_and_k.items():
            l = ll[0] if isinstance(ll, tuple) else ll
            for q, mult in enumerate(k_arr):
                if mult:
                    blocks.append((l, q, mult))
        out.append((t.coeff, tuple(t.lamb), tuple(sorted(blocks))))
    return sorted(out)


@pytest.mark.skipif(not AUTHORS_REPO.exists(),
                    reason="authors' deep_branching repo not available")
@pytest.mark.parametrize("m,k", [(1, 1), (1, 3), (1, 5), (2, 1), (2, 2),
                                 (2, 4), (3, 3), (5, 2), (5, 3)])
def test_golden_cross_check_against_authors_fdb(m, k):
    sys.path.insert(0, str(AUTHORS_REPO))
    try:
        from fdb import fdb_nd  # the authors' implementation
    finally:
        sys.path.pop(0)
    ours = _normalize_ours(fdb_terms(m, k))
    theirs = _normalize_theirs(fdb_nd(m, (k,)))
    assert ours == theirs
