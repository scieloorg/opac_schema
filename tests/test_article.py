# coding: utf-8
from opac_schema.v1.models import Article, Journal, Issue
from .base import BaseTestCase


class TestArticleModel(BaseTestCase):
    model_class_to_delete = [Article, Issue, Journal]

    def _create_dummy_journal(self):
        journal_id = self.generate_uuid_32_string()
        journal_jid = self.generate_uuid_32_string()
        journal_data = {
            '_id': journal_id,
            'jid': journal_jid,
            'title': 'The Dummy Journal',
            'short_title': 'DummyJrnl',
            'acronym': 'dj',
            'is_public': True,
            'publisher_name': "Instituto Nacional de Pesquisas da Amazônia",
            'title': "Acta Amazonica",
            'short_title': "Acta Amaz.",
            'scielo_issn': '2179-975X'
        }

        journal_doc = Journal(**journal_data)
        return journal_doc

    def _create_dummy_issue(self, journal=None):
        if journal is None:
            journal = self._create_dummy_journal()

        issue_id = self.generate_uuid_32_string()
        issue_iid = self.generate_uuid_32_string()
        issue_data = {
            '_id': issue_id,
            'iid': issue_iid,
            'is_public': True,
            'volume': '123',
            'number': '9999',
            'year': 2018,
            'journal': journal,
            'start_month': 9
        }

        issue_doc = Issue(**issue_data)
        return issue_doc

    def test_create_only_required_fields_with_valid_journal_success(self):
        # given
        # create a journal
        journal_doc = self._create_dummy_journal()
        issue_doc = self._create_dummy_issue(journal_doc)

        _id = self.generate_uuid_32_string()
        aid = self.generate_uuid_32_string()
        article_data = {
            '_id': _id,
            'aid': aid,
            'is_public': True,
            # requerido pelo Legendarium:
            'journal': journal_doc,
            'issue': issue_doc,
        }

        # when
        article_data = Article(**article_data)
        article_data.save()

        # then
        articles_count = Article.objects.all().count()
        self.assertEqual(_id, article_data._id)
        self.assertEqual(aid, article_data.aid)
        self.assertEqual(1, articles_count)

    def test_check_article_legend_output(self):
        # given
        # create a journal
        journal_doc = self._create_dummy_journal()
        issue_doc = self._create_dummy_issue(journal_doc)

        _id = self.generate_uuid_32_string()
        aid = self.generate_uuid_32_string()
        article_data = {
            '_id': _id,
            'aid': aid,
            'is_public': True,
            # requerido pelo Legendarium:
            'journal': journal_doc,
            'issue': issue_doc,
        }

        # when
        article_doc = Article(**article_data)
        article_doc.save()

        # then
        expected_legend = u"%s, %s %s(%s)" % (
            journal_doc.short_title, issue_doc.year,
            issue_doc.volume, issue_doc.number)
        self.assertEqual(expected_legend, article_doc.legend)

    def test_check_article_url_with_elocation(self):
        # given
        # create a journal
        journal_doc = self._create_dummy_journal()
        issue_doc = self._create_dummy_issue(journal_doc)

        _id = self.generate_uuid_32_string()
        aid = self.generate_uuid_32_string()
        article_data = {
            '_id': _id,
            'aid': aid,
            'is_public': True,
            # requerido pelo Legendarium:
            'journal': journal_doc,
            'issue': issue_doc,
            'fpage_sequence': 'FPAGE_SEQ',
            'fpage': 'FPAGE',
            'lpage': 'LPAGE',
            'elocation': 'ELOCATION',
            'doi': 'DOI',
            'order': 1111,
        }

        # when
        article_doc = Article(**article_data)
        article_doc.save()

        # then
        self.assertEqual('ELOCATION', article_doc.url)

    def test_check_article_url_with_fpage(self):
        # given
        # create a journal
        journal_doc = self._create_dummy_journal()
        issue_doc = self._create_dummy_issue(journal_doc)

        _id = self.generate_uuid_32_string()
        aid = self.generate_uuid_32_string()
        article_data = {
            '_id': _id,
            'aid': aid,
            'is_public': True,
            # requerido pelo Legendarium:
            'journal': journal_doc,
            'issue': issue_doc,
            'fpage': 'FPAGE',
            'lpage': 'LPAGE',
            'doi': 'DOI',
            'order': 1111,
        }

        # when
        article_doc = Article(**article_data)
        article_doc.save()

        # then
        self.assertEqual('FPAGE-LPAGE', article_doc.url)

    def test_check_article_url_with_fpage_sequence(self):
        # given
        # create a journal
        journal_doc = self._create_dummy_journal()
        issue_doc = self._create_dummy_issue(journal_doc)

        _id = self.generate_uuid_32_string()
        aid = self.generate_uuid_32_string()
        article_data = {
            '_id': _id,
            'aid': aid,
            'is_public': True,
            # requerido pelo Legendarium:
            'journal': journal_doc,
            'issue': issue_doc,
            'fpage_sequence': 'FPAGE_SEQ',
            'fpage': 'FPAGE',
            'lpage': 'LPAGE',
            'doi': 'DOI',
            'order': 1111,
        }

        # when
        article_doc = Article(**article_data)
        article_doc.save()

        # then
        self.assertEqual('FPAGE_FPAGE_SEQ-LPAGE', article_doc.url)

    def test_check_article_url_with_DOI(self):
        # given
        # create a journal
        journal_doc = self._create_dummy_journal()
        issue_doc = self._create_dummy_issue(journal_doc)

        _id = self.generate_uuid_32_string()
        aid = self.generate_uuid_32_string()
        article_data = {
            '_id': _id,
            'aid': aid,
            'is_public': True,
            # requerido pelo Legendarium:
            'journal': journal_doc,
            'issue': issue_doc,
            'doi': 'DOI',
            'order': 1111,
        }

        # when
        article_doc = Article(**article_data)
        article_doc.save()

        # then
        self.assertEqual('DOI', article_doc.url)

    def test_check_article_url_with_order(self):
        # given
        # create a journal
        journal_doc = self._create_dummy_journal()
        issue_doc = self._create_dummy_issue(journal_doc)

        _id = self.generate_uuid_32_string()
        aid = self.generate_uuid_32_string()
        article_data = {
            '_id': _id,
            'aid': aid,
            'is_public': True,
            # requerido pelo Legendarium:
            'journal': journal_doc,
            'issue': issue_doc,
            'order': 1111,
        }

        # when
        article_doc = Article(**article_data)
        article_doc.save()

        # then
        self.assertEqual('o1111', article_doc.url)

    def test_check_article_scielo_pids(self):
        # given
        # create a journal
        journal_doc = self._create_dummy_journal()
        issue_doc = self._create_dummy_issue(journal_doc)

        _id = self.generate_uuid_32_string()
        aid = self.generate_uuid_32_string()
        article_data = {
            '_id': _id,
            'aid': aid,
            'is_public': True,
            # requerido pelo Legendarium:
            'journal': journal_doc,
            'issue': issue_doc,
            'order': 1111,
            'scielo_pids': {
                "v1": "S0101-0202(98)01100123",
                "v2": "S0101-02022019000300001",
                "v3": "azEglOE290cWcmloijsd",
            },
        }

        # when
        article_doc = Article(**article_data)
        article_doc.save()

        # then
        self.assertEqual(
            article_doc.scielo_pids,
            {
                "v1": "S0101-0202(98)01100123",
                "v2": "S0101-02022019000300001",
                "v3": "azEglOE290cWcmloijsd",
            }
        )

    def test_check_article_pid(self):
        # given
        # create a journal
        journal_doc = self._create_dummy_journal()
        issue_doc = self._create_dummy_issue(journal_doc)

        _id = self.generate_uuid_32_string()
        aid = self.generate_uuid_32_string()
        article_data = {
            '_id': _id,
            'aid': aid,
            'is_public': True,
            # requerido pelo Legendarium:
            'journal': journal_doc,
            'issue': issue_doc,
            'order': 1111,
            'scielo_pids': {
                "v1": "S0101-0202(98)01100123",
                "v2": "S0101-02022019000300001",
                "v3": "azEglOE290cWcmloijsd",
            },
        }

        # when
        article_doc = Article(**article_data)
        article_doc.save()

        # then
        self.assertEqual(article_doc.pid, "S0101-02022019000300001")

    def test_check_article_pid_already_set(self):
        # given
        # create a journal
        journal_doc = self._create_dummy_journal()
        issue_doc = self._create_dummy_issue(journal_doc)

        _id = self.generate_uuid_32_string()
        aid = self.generate_uuid_32_string()
        article_data = {
            '_id': _id,
            'aid': aid,
            'is_public': True,
            # requerido pelo Legendarium:
            'journal': journal_doc,
            'issue': issue_doc,
            'order': 1111,
            'pid': "S0101-02022019000300123",
            'scielo_pids': {
                "v1": "S0101-0202(98)01100123",
                "v2": "S0101-02022019000300001",
                "v3": "azEglOE290cWcmloijsd",
            },
        }

        # when
        article_doc = Article(**article_data)
        article_doc.save()

        # then
        self.assertEqual(article_doc.pid, "S0101-02022019000300123")

    def test_if_display_full_text_is_true_by_default(self):
        journal_doc = self._create_dummy_journal()
        issue_doc = self._create_dummy_issue(journal_doc)
        article_data = {
            '_id': self.generate_uuid_32_string(),
            'aid': self.generate_uuid_32_string(),
            'is_public': True,
            'journal': journal_doc,
            'issue': issue_doc,
            'order': 1111,
            'pid': "S0101-02022019000300123"
        }
        article_doc = Article(**article_data)
        article_doc.save()
        self.assertTrue(article_doc.display_full_text)

    def test_if_display_full_text_could_be_setted_as_false(self):
        journal_doc = self._create_dummy_journal()
        issue_doc = self._create_dummy_issue(journal_doc)
        article_data = {
            '_id': self.generate_uuid_32_string(),
            'aid': self.generate_uuid_32_string(),
            'is_public': True,
            'journal': journal_doc,
            'issue': issue_doc,
            'order': 1111,
            'pid': "S0101-02022019000300123",
            'display_full_text': False
        }
        article_doc = Article(**article_data)
        article_doc.save()
        self.assertFalse(article_doc.display_full_text)

    def test_if_possible_set_author_meta_attribute(self):
        journal_doc = self._create_dummy_journal()
        issue_doc = self._create_dummy_issue(journal_doc)

        author_meta = [
            {
                "name": "Thales Silva Coutinho",
                "affiliation": "Universidade Federal de Pernambuco",
                "orcid": "0000-0002-2173-4340",
            },
            {
                "name": "Matheus Colli-Silva",
                "affiliation": "Universidade de São Paulo",
                "orcid": "0000-0001-7130-3920",
            },
        ]

        article_data = {
            '_id': self.generate_uuid_32_string(),
            'aid': self.generate_uuid_32_string(),
            'is_public': True,
            'journal': journal_doc,
            'issue': issue_doc,
            'order': 1111,
            'pid': "S0101-02022019000300123",
            'display_full_text': False,
            'authors_meta': author_meta,
        }

        article_doc = Article(**article_data)
        article_doc.save()
        self.assertTrue(article_doc.authors_meta)

    def test_if_possible_set_related_articles_attribute(self):
        journal_doc = self._create_dummy_journal()
        issue_doc = self._create_dummy_issue(journal_doc)

        related_articles = [
            {
                "ref_id": "9LzVjQrYQF7BvkYWnJw9sDy",
                "doi": "10.1590/S0103-50532006000200015",
                "related_type": "corrected-article"
            },
            {
                "ref_id": "3LzVjQrOIEJYUSvkYWnJwsDy",
                "doi": "10.1590/S0103-5053200600020098983",
                "related_type": "addendum"
            },
            {
                "ref_id": "6LzVjQrKOIJAKSJUIOAKKODy",
                "doi": "10.1590/S0103-50532006000200015",
                "related_type": "retraction"
            },
        ]

        article_data = {
            '_id': self.generate_uuid_32_string(),
            'aid': self.generate_uuid_32_string(),
            'is_public': True,
            'journal': journal_doc,
            'issue': issue_doc,
            'order': 1111,
            'pid': "S0101-02022019000300123",
            'display_full_text': False,
            'related_articles': related_articles,
        }

        article_doc = Article(**article_data)
        article_doc.save()
        self.assertTrue(article_doc.related_articles)

    def test_if_possible_set_doi_with_lang_attribute(self):
        journal_doc = self._create_dummy_journal()
        issue_doc = self._create_dummy_issue(journal_doc)

        doi_with_lang = [
            {
                "doi": "10.1590/S0103-50532006000200015",
                "language": "en"
            },
            {
                "doi": "10.1590/S0103-5053200600020098983",
                "language": "es"
            },
            {
                "doi": "10.1590/S0103-50532006000200015",
                "language": "pt"
            },
            {
                "doi": "10.1590/S0103-60532706000706012",
                "language": "uk"
            },
        ]

        article_data = {
            '_id': self.generate_uuid_32_string(),
            'aid': self.generate_uuid_32_string(),
            'is_public': True,
            'journal': journal_doc,
            'issue': issue_doc,
            'order': 1111,
            'pid': "S0101-02022019000300123",
            'display_full_text': False,
            'doi_with_lang': doi_with_lang,
        }

        article_doc = Article(**article_data)
        article_doc.save()
        self.assertTrue(article_doc.doi_with_lang)

    def test_use_of_get_doi_by_lang_on_article(self):
        journal_doc = self._create_dummy_journal()
        issue_doc = self._create_dummy_issue(journal_doc)

        doi_with_lang = [
            {
                "doi": "10.1590/S0103-50532006000200015",
                "language": "en"
            },
            {
                "doi": "10.1590/S0103-5053200600020098983",
                "language": "es"
            },
            {
                "doi": "10.1590/S0103-50532006000200015",
                "language": "pt"
            },
            {
                "doi": "10.1590/S0103-60532706000706012",
                "language": "uk"
            },
        ]

        article_data = {
            '_id': self.generate_uuid_32_string(),
            'aid': self.generate_uuid_32_string(),
            'is_public': True,
            'journal': journal_doc,
            'issue': issue_doc,
            'order': 1111,
            'pid': "S0101-02022019000300123",
            'display_full_text': False,
            'doi_with_lang': doi_with_lang,
        }
        article_doc = Article(**article_data)
        article_doc.save()
        self.assertEqual(article_doc.get_doi_by_lang(
            'en'), "10.1590/S0103-50532006000200015")
        self.assertEqual(article_doc.get_doi_by_lang(
            'uk'), "10.1590/S0103-60532706000706012")
        self.assertEqual(article_doc.get_doi_by_lang(
            'pt'), "10.1590/S0103-50532006000200015")
        self.assertEqual(article_doc.get_doi_by_lang(
            'bla'), None)

    def test_if_possible_set_mat_suppl_lang_attribute(self):
        journal_doc = self._create_dummy_journal()
        issue_doc = self._create_dummy_issue(journal_doc)

        mat_suppl = [
            {
                "ref_id": "suppl01",
                "lang": "10.1590/S0103-50532006000200001",
                "url": "https://minio.scielo.br/documentstore/2237-9622/d6DyD7CHXbpTJbLq7NQQNdq/5d88e2211c5357e2a9d8caeac2170f4f3d1305d1.pdf",
                "filename": "suppl01.pdf",
            },
            {
                "ref_id": "suppl02",
                "lang": "10.1590/S0103-505320060002000002",
                "url": "https://minio.scielo.br/documentstore/2237-9622/d6DyD7CHXbpTJbLq7NQQNdq/5d88e2211c5357e2a9d8caeac2170f4f3d1305d2.pdf",
                "filename": "suppl02.pdf",
            },
            {
                "ref_id": "suppl03",
                "lang": "10.1590/S0103-50532006000200003",
                "url": "https://minio.scielo.br/documentstore/2237-9622/d6DyD7CHXbpTJbLq7NQQNdq/5d88e2211c5357e2a9d8caeac2170f4f3d1305d3.pdf",
                "filename": "suppl03.pdf",
            },
        ]

        article_data = {
            '_id': self.generate_uuid_32_string(),
            'aid': self.generate_uuid_32_string(),
            'is_public': True,
            'journal': journal_doc,
            'issue': issue_doc,
            'order': 1111,
            'pid': "S0101-02022019000300123",
            'display_full_text': False,
            'mat_suppl': mat_suppl,
        }

        article_doc = Article(**article_data)
        article_doc.save()
        self.assertTrue(article_doc.mat_suppl)

    def test_if_csl_json_property_return_correct_items(self):
        journal_doc = self._create_dummy_journal()
        issue_doc = self._create_dummy_issue(journal_doc)

        article_data = {
            '_id': "2918f62938de499ba0af74932d0fbee5",
            'aid': "2918f62938de499ba0af74932d0fbee5",
            'is_public': True,
            'title': "Nephrotic syndrome associated with primary atypical hemolytic uremic syndrome",
            'type': "case-report",
            'doi': "10.1590/2175-8239-JBN-2020-0050",
            'journal': journal_doc,
            'issue': issue_doc,
            'pid': "S0101-02022019000300123",
            'elocation': "@location",
            'authors': [
                "Miola, Brígida",
                "Frota, Maria Myrian Melo",
                "Oliveira, André Gadelha de",
                "Uchôa, Kênio Monteles",
                "Leandro Filho, Francisco de Assis"
            ]
        }

        article_doc = Article(**article_data)
        article_doc.save()
        
        self.assertEqual(article_doc.csl_json(), [{'id': '2918f62938de499ba0af74932d0fbee5', 'DOI': '10.1590/2175-8239-JBN-2020-0050', 'URL': 'https://doi.org/10.1590/2175-8239-JBN-2020-0050', 'ISSN': '2179-975X', 'author': [{'family': 'Miola', 'given': 'Brígida'}, {'family': 'Frota', 'given': 'Maria Myrian Melo'}, {'family': 'Oliveira', 'given': 'André Gadelha de'}, {'family': 'Uchôa', 'given': 'Kênio Monteles'}, {'family': 'Leandro Filho', 'given': 'Francisco de Assis'}], 'container-title': 'Acta Amazonica', 'container-title-short': 'Acta Amaz.', 'issue': 'Acta Amaz., 2018 123(9999)', 'issued': {'date-parts': [[2018, 9]]}, 'page': '@location', 'publisher': 'Instituto Nacional de Pesquisas da Amazônia', 'title': 'Nephrotic syndrome associated with primary atypical hemolytic uremic syndrome', 'type': 'article-journal', 'volume': '123'}])

    def test_if_csl_json_property_return_correct_without_common_on_authors(self):
        journal_doc = self._create_dummy_journal()
        issue_doc = self._create_dummy_issue(journal_doc)
        
        article_data = {
            '_id': "2918f62938de499ba0af74932d0fbee5",
            'aid': "2918f62938de499ba0af74932d0fbee5",
            'is_public': True,
            'title': "Nephrotic syndrome associated with primary atypical hemolytic uremic syndrome",
            'type': "case-report",
            'doi': "10.1590/2175-8239-JBN-2020-0050",
            'journal': journal_doc,
            'issue': issue_doc,
            'pid': "S0101-02022019000300123",
            'elocation': "@location",
            'authors': [
                "Miola Brígida",
                "Frota Maria Myrian Melo",
                "Oliveira André Gadelha de",
                "Uchôa Kênio Monteles",
                "Leandro Filho Francisco de Assis"
            ]
        }
        
        article_doc = Article(**article_data)
        
        self.assertEqual(article_doc.csl_json(), [{'id': '2918f62938de499ba0af74932d0fbee5', 'DOI': '10.1590/2175-8239-JBN-2020-0050', 'URL': 'https://doi.org/10.1590/2175-8239-JBN-2020-0050', 'ISSN': '2179-975X', 'author': [{'family': 'Miola Brígida', 'given': 'Miola Brígida'}, {'family': 'Frota Maria Myrian Melo', 'given': 'Frota Maria Myrian Melo'}, {'family': 'Oliveira André Gadelha de', 'given': 'Oliveira André Gadelha de'}, {'family': 'Uchôa Kênio Monteles', 'given': 'Uchôa Kênio Monteles'}, {'family': 'Leandro Filho Francisco de Assis', 'given': 'Leandro Filho Francisco de Assis'}], 'container-title': 'Acta Amazonica', 'container-title-short': 'Acta Amaz.', 'issue': 'Acta Amaz., 2018 123(9999)', 'issued': {'date-parts': [[2018, 9]]}, 'page': '@location', 'publisher': 'Instituto Nacional de Pesquisas da Amazônia', 'title': 'Nephrotic syndrome associated with primary atypical hemolytic uremic syndrome', 'type': 'article-journal', 'volume': '123'}])

    def test_if_csl_json_property_return_correct_without_authors(self):
        journal_doc = self._create_dummy_journal()
        issue_doc = self._create_dummy_issue(journal_doc)
        
        article_data = {
            '_id': "2918f62938de499ba0af74932d0fbee5",
            'aid': "2918f62938de499ba0af74932d0fbee5",
            'is_public': True,
            'title': "Nephrotic syndrome associated with primary atypical hemolytic uremic syndrome",
            'type': "case-report",
            'doi': "10.1590/2175-8239-JBN-2020-0050",
            'journal': journal_doc,
            'issue': issue_doc,
            'pid': "S0101-02022019000300123",
            'elocation': "@location",
            'authors': []
        }
        
        article_doc = Article(**article_data)
        
        self.assertEqual(article_doc.csl_json(), [{'id': '2918f62938de499ba0af74932d0fbee5', 'DOI': '10.1590/2175-8239-JBN-2020-0050', 'URL': 'https://doi.org/10.1590/2175-8239-JBN-2020-0050', 'ISSN': '2179-975X', 'author': [], 'container-title': 'Acta Amazonica', 'container-title-short': 'Acta Amaz.', 'issue': 'Acta Amaz., 2018 123(9999)', 'issued': {'date-parts': [[2018, 9]]}, 'page': '@location', 'publisher': 'Instituto Nacional de Pesquisas da Amazônia', 'title': 'Nephrotic syndrome associated with primary atypical hemolytic uremic syndrome', 'type': 'article-journal', 'volume': '123'}])

    def test_if_csl_json_property_return_correct_with_empty_authors(self):
        journal_doc = self._create_dummy_journal()
        issue_doc = self._create_dummy_issue(journal_doc)
        
        article_data = {
            '_id': "2918f62938de499ba0af74932d0fbee5",
            'aid': "2918f62938de499ba0af74932d0fbee5",
            'is_public': True,
            'title': "Nephrotic syndrome associated with primary atypical hemolytic uremic syndrome",
            'type': "case-report",
            'doi': "10.1590/2175-8239-JBN-2020-0050",
            'journal': journal_doc,
            'issue': issue_doc,
            'pid': "S0101-02022019000300123",
            'elocation': "@location",
            'authors': ["", ""]
        }
        
        article_doc = Article(**article_data)
        
        self.assertEqual(article_doc.csl_json(), [{'id': '2918f62938de499ba0af74932d0fbee5', 'DOI': '10.1590/2175-8239-JBN-2020-0050', 'URL': 'https://doi.org/10.1590/2175-8239-JBN-2020-0050', 'ISSN': '2179-975X', 'author': [{'family': '', 'given': ''}, {'family': '', 'given': ''}], 'container-title': 'Acta Amazonica', 'container-title-short': 'Acta Amaz.', 'issue': 'Acta Amaz., 2018 123(9999)', 'issued': {'date-parts': [[2018, 9]]}, 'page': '@location', 'publisher': 'Instituto Nacional de Pesquisas da Amazônia', 'title': 'Nephrotic syndrome associated with primary atypical hemolytic uremic syndrome', 'type': 'article-journal', 'volume': '123'}])

    def test_if_csl_json_property_return_preferably_elocation_on_page(self):
        journal_doc = self._create_dummy_journal()
        issue_doc = self._create_dummy_issue(journal_doc)
        
        article_data = {
            '_id': "2918f62938de499ba0af74932d0fbee5",
            'aid': "2918f62938de499ba0af74932d0fbee5",
            'is_public': True,
            'title': "Nephrotic syndrome associated with primary atypical hemolytic uremic syndrome",
            'type': "case-report",
            'doi': "10.1590/2175-8239-JBN-2020-0050",
            'journal': journal_doc,
            'issue': issue_doc,
            'pid': "S0101-02022019000300123",
            'elocation': "e123",
            'authors': [
                "Miola Brígida",
                "Frota Maria Myrian Melo",
                "Oliveira André Gadelha de",
                "Uchôa Kênio Monteles",
                "Leandro Filho Francisco de Assis"
            ]
        }
        
        article_doc = Article(**article_data)
        
        self.assertEqual(article_doc.csl_json(), [{'id': '2918f62938de499ba0af74932d0fbee5', 'DOI': '10.1590/2175-8239-JBN-2020-0050', 'URL': 'https://doi.org/10.1590/2175-8239-JBN-2020-0050', 'ISSN': '2179-975X', 'author': [{'family': 'Miola Brígida', 'given': 'Miola Brígida'}, {'family': 'Frota Maria Myrian Melo', 'given': 'Frota Maria Myrian Melo'}, {'family': 'Oliveira André Gadelha de', 'given': 'Oliveira André Gadelha de'}, {'family': 'Uchôa Kênio Monteles', 'given': 'Uchôa Kênio Monteles'}, {'family': 'Leandro Filho Francisco de Assis', 'given': 'Leandro Filho Francisco de Assis'}], 'container-title': 'Acta Amazonica', 'container-title-short': 'Acta Amaz.', 'issue': 'Acta Amaz., 2018 123(9999)', 'issued': {'date-parts': [[2018, 9]]}, 'page': 'e123', 'publisher': 'Instituto Nacional de Pesquisas da Amazônia', 'title': 'Nephrotic syndrome associated with primary atypical hemolytic uremic syndrome', 'type': 'article-journal', 'volume': '123'}])

    def test_if_csl_json_property_return_empty_page_with_empty_elocation_fpage_lpage(self):
        journal_doc = self._create_dummy_journal()
        issue_doc = self._create_dummy_issue(journal_doc)
        
        article_data = {
            '_id': "2918f62938de499ba0af74932d0fbee5",
            'aid': "2918f62938de499ba0af74932d0fbee5",
            'is_public': True,
            'title': "Nephrotic syndrome associated with primary atypical hemolytic uremic syndrome",
            'type': "case-report",
            'doi': "10.1590/2175-8239-JBN-2020-0050",
            'journal': journal_doc,
            'issue': issue_doc,
            'pid': "S0101-02022019000300123",
            'authors': [
                "Miola Brígida",
                "Frota Maria Myrian Melo",
                "Oliveira André Gadelha de",
                "Uchôa Kênio Monteles",
                "Leandro Filho Francisco de Assis"
            ]
        }
        
        article_doc = Article(**article_data)
        
        self.assertEqual(article_doc.csl_json(), [{'id': '2918f62938de499ba0af74932d0fbee5', 'DOI': '10.1590/2175-8239-JBN-2020-0050', 'URL': 'https://doi.org/10.1590/2175-8239-JBN-2020-0050', 'ISSN': '2179-975X', 'author': [{'family': 'Miola Brígida', 'given': 'Miola Brígida'}, {'family': 'Frota Maria Myrian Melo', 'given': 'Frota Maria Myrian Melo'}, {'family': 'Oliveira André Gadelha de', 'given': 'Oliveira André Gadelha de'}, {'family': 'Uchôa Kênio Monteles', 'given': 'Uchôa Kênio Monteles'}, {'family': 'Leandro Filho Francisco de Assis', 'given': 'Leandro Filho Francisco de Assis'}], 'container-title': 'Acta Amazonica', 'container-title-short': 'Acta Amaz.', 'issue': 'Acta Amaz., 2018 123(9999)', 'issued': {'date-parts': [[2018, 9]]}, 'page': '', 'publisher': 'Instituto Nacional de Pesquisas da Amazônia', 'title': 'Nephrotic syndrome associated with primary atypical hemolytic uremic syndrome', 'type': 'article-journal', 'volume': '123'}])

    def test_if_csl_json_property_return_empty_page_with_empty_elocation_lpage(self):
        journal_doc = self._create_dummy_journal()
        issue_doc = self._create_dummy_issue(journal_doc)
        
        article_data = {
            '_id': "2918f62938de499ba0af74932d0fbee5",
            'aid': "2918f62938de499ba0af74932d0fbee5",
            'is_public': True,
            'title': "Nephrotic syndrome associated with primary atypical hemolytic uremic syndrome",
            'type': "case-report",
            'doi': "10.1590/2175-8239-JBN-2020-0050",
            'journal': journal_doc,
            'issue': issue_doc,
            'fpage': '100',
            'pid': "S0101-02022019000300123",
            'authors': [
                "Miola Brígida",
                "Frota Maria Myrian Melo",
                "Oliveira André Gadelha de",
                "Uchôa Kênio Monteles",
                "Leandro Filho Francisco de Assis"
            ]
        }
        
        article_doc = Article(**article_data)
        
        self.assertEqual(article_doc.csl_json(), [{'id': '2918f62938de499ba0af74932d0fbee5', 'DOI': '10.1590/2175-8239-JBN-2020-0050', 'URL': 'https://doi.org/10.1590/2175-8239-JBN-2020-0050', 'ISSN': '2179-975X', 'author': [{'family': 'Miola Brígida', 'given': 'Miola Brígida'}, {'family': 'Frota Maria Myrian Melo', 'given': 'Frota Maria Myrian Melo'}, {'family': 'Oliveira André Gadelha de', 'given': 'Oliveira André Gadelha de'}, {'family': 'Uchôa Kênio Monteles', 'given': 'Uchôa Kênio Monteles'}, {'family': 'Leandro Filho Francisco de Assis', 'given': 'Leandro Filho Francisco de Assis'}], 'container-title': 'Acta Amazonica', 'container-title-short': 'Acta Amaz.', 'issue': 'Acta Amaz., 2018 123(9999)', 'issued': {'date-parts': [[2018, 9]]}, 'page': '100', 'publisher': 'Instituto Nacional de Pesquisas da Amazônia', 'title': 'Nephrotic syndrome associated with primary atypical hemolytic uremic syndrome', 'type': 'article-journal', 'volume': '123'}])

    def test_if_csl_json_property_return_empty_page_with_empty_elocation_fpage(self):
        journal_doc = self._create_dummy_journal()
        issue_doc = self._create_dummy_issue(journal_doc)
        
        article_data = {
            '_id': "2918f62938de499ba0af74932d0fbee5",
            'aid': "2918f62938de499ba0af74932d0fbee5",
            'is_public': True,
            'title': "Nephrotic syndrome associated with primary atypical hemolytic uremic syndrome",
            'type': "case-report",
            'doi': "10.1590/2175-8239-JBN-2020-0050",
            'journal': journal_doc,
            'issue': issue_doc,
            'lpage': '200',
            'pid': "S0101-02022019000300123",
            'authors': [
                "Miola Brígida",
                "Frota Maria Myrian Melo",
                "Oliveira André Gadelha de",
                "Uchôa Kênio Monteles",
                "Leandro Filho Francisco de Assis"
            ]
        }
        
        article_doc = Article(**article_data)
        
        self.assertEqual(article_doc.csl_json(), [{'id': '2918f62938de499ba0af74932d0fbee5', 'DOI': '10.1590/2175-8239-JBN-2020-0050', 'URL': 'https://doi.org/10.1590/2175-8239-JBN-2020-0050', 'ISSN': '2179-975X', 'author': [{'family': 'Miola Brígida', 'given': 'Miola Brígida'}, {'family': 'Frota Maria Myrian Melo', 'given': 'Frota Maria Myrian Melo'}, {'family': 'Oliveira André Gadelha de', 'given': 'Oliveira André Gadelha de'}, {'family': 'Uchôa Kênio Monteles', 'given': 'Uchôa Kênio Monteles'}, {'family': 'Leandro Filho Francisco de Assis', 'given': 'Leandro Filho Francisco de Assis'}], 'container-title': 'Acta Amazonica', 'container-title-short': 'Acta Amaz.', 'issue': 'Acta Amaz., 2018 123(9999)', 'issued': {'date-parts': [[2018, 9]]}, 'page': '200', 'publisher': 'Instituto Nacional de Pesquisas da Amazônia', 'title': 'Nephrotic syndrome associated with primary atypical hemolytic uremic syndrome', 'type': 'article-journal', 'volume': '123'}])

    def test_if_csl_json_property_return_empty_page_with_empty_elocation(self):
        journal_doc = self._create_dummy_journal()
        issue_doc = self._create_dummy_issue(journal_doc)
        
        article_data = {
            '_id': "2918f62938de499ba0af74932d0fbee5",
            'aid': "2918f62938de499ba0af74932d0fbee5",
            'is_public': True,
            'title': "Nephrotic syndrome associated with primary atypical hemolytic uremic syndrome",
            'type': "case-report",
            'doi': "10.1590/2175-8239-JBN-2020-0050",
            'journal': journal_doc,
            'issue': issue_doc,
            'fpage': '100',
            'lpage': '200',
            'pid': "S0101-02022019000300123",
            'authors': [
                "Miola Brígida",
                "Frota Maria Myrian Melo",
                "Oliveira André Gadelha de",
                "Uchôa Kênio Monteles",
                "Leandro Filho Francisco de Assis"
            ]
        }
        
        article_doc = Article(**article_data)
        
        self.assertEqual(article_doc.csl_json(), [{'id': '2918f62938de499ba0af74932d0fbee5', 'DOI': '10.1590/2175-8239-JBN-2020-0050', 'URL': 'https://doi.org/10.1590/2175-8239-JBN-2020-0050', 'ISSN': '2179-975X', 'author': [{'family': 'Miola Brígida', 'given': 'Miola Brígida'}, {'family': 'Frota Maria Myrian Melo', 'given': 'Frota Maria Myrian Melo'}, {'family': 'Oliveira André Gadelha de', 'given': 'Oliveira André Gadelha de'}, {'family': 'Uchôa Kênio Monteles', 'given': 'Uchôa Kênio Monteles'}, {'family': 'Leandro Filho Francisco de Assis', 'given': 'Leandro Filho Francisco de Assis'}], 'container-title': 'Acta Amazonica', 'container-title-short': 'Acta Amaz.', 'issue': 'Acta Amaz., 2018 123(9999)', 'issued': {'date-parts': [[2018, 9]]}, 'page': '100-200', 'publisher': 'Instituto Nacional de Pesquisas da Amazônia', 'title': 'Nephrotic syndrome associated with primary atypical hemolytic uremic syndrome', 'type': 'article-journal', 'volume': '123'}])

    def test_if_csl_json_property_return_empty_page_with_elocation_fpage_lpage(self):
        journal_doc = self._create_dummy_journal()
        issue_doc = self._create_dummy_issue(journal_doc)
        
        article_data = {
            '_id': "2918f62938de499ba0af74932d0fbee5",
            'aid': "2918f62938de499ba0af74932d0fbee5",
            'is_public': True,
            'title': "Nephrotic syndrome associated with primary atypical hemolytic uremic syndrome",
            'type': "case-report",
            'doi': "10.1590/2175-8239-JBN-2020-0050",
            'journal': journal_doc,
            'issue': issue_doc,
            'elocation': 'e987',
            'fpage': '100',
            'lpage': '200',
            'pid': "S0101-02022019000300123",
            'authors': [
                "Miola Brígida",
                "Frota Maria Myrian Melo",
                "Oliveira André Gadelha de",
                "Uchôa Kênio Monteles",
                "Leandro Filho Francisco de Assis"
            ]
        }
        
        article_doc = Article(**article_data)
        
        self.assertEqual(article_doc.csl_json(), [{'id': '2918f62938de499ba0af74932d0fbee5', 'DOI': '10.1590/2175-8239-JBN-2020-0050', 'URL': 'https://doi.org/10.1590/2175-8239-JBN-2020-0050', 'ISSN': '2179-975X', 'author': [{'family': 'Miola Brígida', 'given': 'Miola Brígida'}, {'family': 'Frota Maria Myrian Melo', 'given': 'Frota Maria Myrian Melo'}, {'family': 'Oliveira André Gadelha de', 'given': 'Oliveira André Gadelha de'}, {'family': 'Uchôa Kênio Monteles', 'given': 'Uchôa Kênio Monteles'}, {'family': 'Leandro Filho Francisco de Assis', 'given': 'Leandro Filho Francisco de Assis'}], 'container-title': 'Acta Amazonica', 'container-title-short': 'Acta Amaz.', 'issue': 'Acta Amaz., 2018 123(9999)', 'issued': {'date-parts': [[2018, 9]]}, 'page': 'e987', 'publisher': 'Instituto Nacional de Pesquisas da Amazônia', 'title': 'Nephrotic syndrome associated with primary atypical hemolytic uremic syndrome', 'type': 'article-journal', 'volume': '123'}])