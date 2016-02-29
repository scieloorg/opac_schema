# coding: utf-8

from mongoengine import *


class UseLicense(EmbeddedDocument):
    license_code = StringField(required=True)
    reference_url = StringField()
    disclaimer = StringField()

    meta = {
        'collection': 'use_license'
    }

    def __unicode__(self):
        return self.code


class Timeline(EmbeddedDocument):
    since = DateTimeField()
    reason = StringField()
    status = StringField()

    meta = {
        'collection': 'timeline'
    }

    def __unicode__(self):
        return '%s - %s' % (self.status, self.since)


class SocialNetwork(EmbeddedDocument):
    account = StringField()
    network = StringField()

    meta = {
        'collection': 'social_network'
    }

    def __unicode__(self):
        return self.account


class OtherTitle(EmbeddedDocument):
    title = StringField()
    category = StringField()

    meta = {
        'collection': 'other_title'
    }

    def __unicode__(self):
        return self.title


class Mission(EmbeddedDocument):
    language = StringField()
    description = StringField()

    meta = {
        'collection': 'mission'
    }

    def __unicode__(self):
        return '<Mission: %s>' % (self.language)


class LastIssue(EmbeddedDocument):
    volume = StringField()
    number = StringField()
    year = IntField()
    label = StringField()
    start_month = IntField()
    end_month = IntField()
    sections = ListField(field=StringField())
    cover_url = StringField()
    iid = StringField()
    bibliographic_legend = StringField()

    meta = {
        'collection': 'last_issue'
    }

    def __unicode__(self):
        return self.label


class Subject(EmbeddedDocument):
    name = StringField()
    language = StringField()

    meta = {
        'collection': 'subjects'
    }

    def __unicode__(self):
        return self.name


class Section(EmbeddedDocument):
    order = IntField()
    subjects = EmbeddedDocumentListField(Subject)

    meta = {
        'collection': 'sections'
    }

    def __unicode__(self):
        return '<Section: %s>' % self.order


class ArticleHTML(EmbeddedDocument):
    language = StringField()
    source = StringField()

    meta = {
        'collection': 'article_html'
    }

    def __unicode__(self):
        return '<ArticleHTML: %s>' % self.language


class Sponsor(Document):
    _id = StringField(max_length=32, primary_key=True, required=True, unique=True)
    name = StringField(max_length=256, required=True, unique=True)
    url = StringField()
    logo_url = StringField()

    meta = {
        'collection': 'sponsor'
    }

    def __unicode__(self):
        return self.name


class Collection(Document):
    _id = StringField(max_length=32, primary_key=True, required=True, unique=True)
    acronym = StringField(max_length=50, required=True, unique=True)
    name = StringField(max_length=100, required=True, unique_with='acronym')
    logo_url = StringField()
    license_code = StringField(max_length=10, required=True)
    sponsors = ListField(ReferenceField(Sponsor, reverse_delete_rule=PULL))

    meta = {
        'collection': 'collection'
    }

    def __unicode__(self):
        return self.acronym


class Journal(Document):
    _id = StringField(max_length=32, primary_key=True, required=True, unique=True)
    jid = StringField(max_length=32, required=True, unique=True, )
    collection = ReferenceField(Collection, reverse_delete_rule=CASCADE)
    use_licenses = EmbeddedDocumentField(UseLicense)
    timeline = EmbeddedDocumentListField(Timeline)
    subject_categories = ListField(field=StringField())
    study_areas = ListField(field=StringField())
    social_networks = EmbeddedDocumentListField(SocialNetwork)
    title = StringField()
    title_iso = StringField()
    short_title = StringField()
    created = DateTimeField()
    updated = DateTimeField()
    acronym = StringField()
    scielo_issn = StringField()
    print_issn = StringField()
    eletronic_issn = StringField()
    subject_descriptors = ListField(field=StringField())
    copyrighter = StringField()
    online_submission_url = StringField()
    cover_url = StringField()
    logo_url = StringField()
    previous_journal_ref = StringField()
    other_titles = EmbeddedDocumentListField(OtherTitle)
    publisher_name = StringField()
    publisher_country = StringField()
    publisher_state = StringField()
    publisher_city = StringField()
    publisher_address = StringField()
    publisher_telephone = StringField()
    current_status = StringField()

    mission = EmbeddedDocumentListField(Mission)
    index_at = ListField(field=StringField())
    sponsors = ListField(field=StringField())
    issue_count = IntField()
    last_issue = EmbeddedDocumentField(LastIssue)

    is_public = BooleanField(required=True, default=True)
    unpublish_reason = StringField()

    meta = {
        'collection': 'journal'
    }

    def __unicode__(self):
        return self.acronym or 'undefined acronym'


class Issue(Document):

    _id = StringField(max_length=32, primary_key=True, required=True, unique=True)
    iid = StringField(max_length=32, required=True, unique=True)
    journal = ReferenceField(Journal, reverse_delete_rule=CASCADE)

    sections = EmbeddedDocumentListField(Section)
    use_licenses = EmbeddedDocumentField(UseLicense)

    cover_url = StringField()

    volume = StringField()
    number = StringField()
    created = DateTimeField()
    updated = DateTimeField()

    type = StringField()
    suppl_text = StringField()
    spe_text = StringField()
    start_month = IntField()
    end_month = IntField()
    year = IntField()
    label = StringField()
    order = IntField()
    bibliographic_legend = StringField()

    is_public = BooleanField(required=True, default=True)
    unpublish_reason = StringField()

    meta = {
        'collection': 'issue'
    }

    def __unicode__(self):
        return self.label


class Article(Document):
    _id = StringField(max_length=32, primary_key=True, required=True, unique=True)
    aid = StringField(max_length=32, required=True, unique=True)

    issue = ReferenceField(Issue, reverse_delete_rule=CASCADE)
    journal = ReferenceField(Journal, reverse_delete_rule=CASCADE)

    title = StringField()
    section = StringField()
    is_aop = BooleanField()
    created = DateTimeField()
    updated = DateTimeField()
    htmls = EmbeddedDocumentListField(ArticleHTML)

    domain_key = StringField()

    xml = StringField()
    is_public = BooleanField(required=True, default=True)
    unpublish_reason = StringField()

    meta = {
        'collection': 'article'
    }

    def __unicode__(self):
        return self.title
