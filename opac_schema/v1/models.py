# coding: utf-8

from mongoengine import (
    Document,
    EmbeddedDocument,
    # campos:
    StringField,
    IntField,
    DateTimeField,
    ListField,
    EmbeddedDocumentField,
    EmbeddedDocumentListField,
    ReferenceField,
    BooleanField,
    URLField,
    # reverse_delete_rule:
    PULL,
    CASCADE,
)


class Resource(Document):
    _id = StringField(max_length=32, primary_key=True, required=True, unique=True)
    url = URLField(required=True)
    type = StringField(required=True)
    language = StringField()
    description = StringField()

    meta = {
        'collection': 'resource'
    }

    def __unicode__(self):
        return self.url


class UseLicense(EmbeddedDocument):
    license_code = StringField(required=True)
    reference_url = StringField()
    disclaimer = StringField()

    meta = {
        'collection': 'use_license'
    }

    def __unicode__(self):
        return self.code


class Section(EmbeddedDocument):
    order = IntField()
    subjects = EmbeddedDocumentListField('Subject')

    meta = {
        'collection': 'sections'
    }

    def __unicode__(self):
        return '<Section: %s>' % self.order


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
    sections = EmbeddedDocumentListField(Section)
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


class TranslatedTitle(EmbeddedDocument):
    name = StringField()
    language = StringField()

    meta = {
        'collection': 'translated_title'
    }

    def __unicode__(self):
        return self.name


class Sponsor(Document):
    _id = StringField(max_length=32, primary_key=True, required=True, unique=True)
    name = StringField(max_length=256, required=True, unique=True)
    url = URLField()
    logo_url = URLField()

    meta = {
        'collection': 'sponsor'
    }

    def __unicode__(self):
        return self.name


class Collection(Document):
    _id = StringField(max_length=32, primary_key=True, required=True, unique=True)
    acronym = StringField(max_length=50, required=True, unique=True)
    name = StringField(max_length=100, required=True, unique_with='acronym')

    license = EmbeddedDocumentField(UseLicense, required=True)

    sponsors = ListField(ReferenceField(Sponsor, reverse_delete_rule=PULL))

    # Address
    address1 = StringField(max_length=128)
    address2 = StringField(max_length=128)

    # logos
    logo_resource = ListField(ReferenceField(Resource, reverse_delete_rule=PULL))
    header_logo_resource = ReferenceField(Resource, reverse_delete_rule=PULL)
    footer_resource = ReferenceField(Resource, reverse_delete_rule=PULL)

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

    cover_url = StringField()

    volume = StringField()
    number = StringField()

    created = DateTimeField()
    updated = DateTimeField()

    type = StringField()  # será removido
    suppl_text = StringField()  # será removido
    spe_text = StringField()  # será removido

    start_month = IntField()  # será removido
    end_month = IntField()   # será removido

    year = IntField()
    label = StringField()
    order = IntField()
    bibliographic_legend = StringField()

    is_public = BooleanField(required=True, default=True)
    unpublish_reason = StringField()
    pid = StringField()

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
    translated_titles = EmbeddedDocumentListField(TranslatedTitle)
    section = StringField()
    sections = EmbeddedDocumentListField(Section)
    is_aop = BooleanField()
    order = IntField()
    doi = StringField()
    htmls = ListField(ReferenceField(Resource, reverse_delete_rule=PULL))
    pdfs = ListField(ReferenceField(Resource, reverse_delete_rule=PULL))
    pid = StringField()
    languages = ListField(field=StringField())
    original_language = StringField()

    domain_key = StringField()

    xml = URLField()

    created = DateTimeField()
    updated = DateTimeField()

    is_public = BooleanField(required=True, default=True)
    unpublish_reason = StringField()

    meta = {
        'collection': 'article'
    }

    def __unicode__(self):
        return self.title
