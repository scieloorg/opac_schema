========================
SciELO OPAC Schema
========================

This is part of the SciELO Site Project define the schema of the index to provide data do Site SciELO.

This schema is based on MongoEngine Schema, more detail: http://mongoengine.org/

.. image:: https://travis-ci.org/scieloorg/opac_schema.svg
    :target: https://travis-ci.org/scieloorg/opac_schema

========================================
Where is schema on the architecture?
========================================

.. image:: https://github.com/scieloorg/documents/blob/master/scielo_site/architecture_schema.png


========================================
Model and entities with special attributes:
========================================

.. code-block::


        +++++++
        +  J  +  Key: jid
    ----+  O  +  issue_count
    |   +  R  +
    |   +  N  +
    |   +  A  +
    |   +  L  +
    |   +++++++
    |      |
  J |      |  journal_jid
  O |      |
  R |   +++++++
  N |   +  I  +  Key: iid
  A |   +  S  +  Relation Key: journal_jid
  L |   +  S  +
  _ |   +  U  +
  J |   +  E  +
  I |   +++++++
  D |      |
    |      |  issue_iid
    |      |
    |   +++++++
    |   +  A  +  Key: aid
    |   +  R  +  Relation Key: issue_iid
    |   +  T  +  Relation Key: journal_jid
    ----+  I  +
        +  C  +
        +  L  +
        +  E  +
        +++++++


===========
Instalation
===========

.. code-block::

  pip install -e git+git@github.com:scieloorg/opac_schema.git#egg=opac_schema

ou com https:

.. code-block::

  pip install -e https://github.com/scieloorg/opac-schema#egg=opac_schema

