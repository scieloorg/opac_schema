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

