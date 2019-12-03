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
            'is_public': True
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
            'journal': journal
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

