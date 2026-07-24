"""
Tests resolver bootstrap.
"""

from autosar_codegen.resolver.bootstrap import (
    bootstrap_resolvers,
)



def test_bootstrap_execution():

    registry = bootstrap_resolvers()


    assert registry is not None



def test_default_resolvers_registered():

    registry = bootstrap_resolvers()


    resolvers = registry.all()


    assert len(
        resolvers
    ) > 0