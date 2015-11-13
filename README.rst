========================
SciELO OPAC Schema
========================

This is part of the SciELO Site Project define the schema of the index to provide data do Site SciELO.

This schema is based on ElasticSearch Mapping, more detail: https://www.elastic.co/guide/en/elasticsearch/guide/current/mapping-intro.html 

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
    |   +  R  +  last_issue: year, volume, number,
    |   +  N  +              label, sections, iid,
    |   +  A  +              start_month, end_month,
    |   +  L  +              cover_url, bibliographic_legend
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
        +  C  +  journal: title, publisher_name,
        +  L  +           print_issn, scielo_issn,
        +  E  +           eletronic_issn, study_areas
        +++++++
                 issue: year, volume, number
