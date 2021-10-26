# coding: utf-8
from opac_schema.v2.models import ArticleFiles
from .base import BaseTestCase
from mongoengine.errors import NotUniqueError


class TestArticleFilesModel(BaseTestCase):
    model_class_to_delete = [ArticleFiles]

    def test_create_article_files(self):
        aid = self.generate_uuid_32_string()
        aid_doc_pkgs_count = ArticleFiles.objects(aid=aid).count()

        data = {
            'aid': aid,
            'version': aid_doc_pkgs_count + 1,
        }

        article_files_1 = ArticleFiles(**data)
        article_files_1.save()

        new_aid_doc_pkgs_count = ArticleFiles.objects(aid=aid).count()

        self.assertEqual(aid_doc_pkgs_count + 1, new_aid_doc_pkgs_count)
        self.assertEqual(aid, article_files_1.aid)

    def test_create_two_article_files(self):
        aid1 = self.generate_uuid_32_string()
        aid_doc_pkgs_count = ArticleFiles.objects(aid=aid1).count()

        data = {
            'aid': aid1,
            'version': aid_doc_pkgs_count + 1,
        }

        # create first article_files with aid1
        article_files_1 = ArticleFiles(**data)
        article_files_1.save()

        data.update({'version': ArticleFiles.objects(aid=aid1).count() + 1})

        # create second article_files with the same aid1
        article_files_2 = ArticleFiles(**data)
        article_files_2.save()

        # create third article_files with a different aid
        data.update({'aid': self.generate_uuid_32_string(), 'version': 1})
        article_files_3 = ArticleFiles(**data)
        article_files_3.save()

        # count the number of article_files (doc_pkg) related to aid1
        total_aid1_doc_pkgs = ArticleFiles.objects(aid=aid1).count()

        self.assertEqual(aid1, article_files_1.aid)
        self.assertEqual(aid1, article_files_2.aid)
        self.assertEqual(total_aid1_doc_pkgs, 2)
        self.assertEqual(1, article_files_1.version)
        self.assertEqual(2, article_files_2.version)
        self.assertEqual(1, article_files_3.version)
