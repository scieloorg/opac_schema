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
    # signals
    signals,
)

from legendarium.legendarium import Legendarium
from legendarium.urlegendarium import URLegendarium

from slugify import slugify


class News(Document):
    _id = StringField(max_length=32, primary_key=True, required=True)
    url = URLField(required=True)
    image_url = URLField(required=False)
    publication_date = DateTimeField(required=True)
    title = StringField(max_length=256, required=True)
    description = StringField(required=True)
    language = StringField(max_length=5, required=True)
    is_public = BooleanField(required=True, default=True)


class Pages(Document):
    _id = StringField(max_length=32, primary_key=True, required=True)
    name = StringField(required=True)
    language = StringField(max_length=5, required=True)
    content = StringField(required=True)
    journal = StringField()
    description = StringField()

    meta = {
        'collection': 'pages'
    }

    def __unicode__(self):
        return self.name


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
    sections = EmbeddedDocumentListField('TranslatedSection')
    cover_url = StringField()
    iid = StringField()
    url_segment = StringField()

    meta = {
        'collection': 'last_issue'
    }

    def __unicode__(self):
        return self.label


class TranslatedSection(EmbeddedDocument):
    name = StringField()
    language = StringField()

    meta = {
        'collection': 'translated_section'
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


class CollectionMetrics(EmbeddedDocument):
    total_journal = IntField(default=0)
    total_issue = IntField(default=0)
    total_article = IntField(default=0)
    total_citation = IntField(default=0)

    def __unicode__(self):
        return '%s - %s - %s - %s' % (self.total_journal, self.total_issue,
                                      self.total_article, self.total_citation)


class JounalMetrics(EmbeddedDocument):
    total_h5_index = IntField(default=0)
    total_h5_median = IntField(default=0)

    def __unicode__(self):
        return '%s - %s' % (self.total_h5_index, self.total_h5_median)


class Sponsor(Document):
    _id = StringField(max_length=32, primary_key=True, required=True)
    name = StringField(max_length=256, required=True, unique=True)
    url = URLField()
    logo_url = URLField()

    meta = {
        'collection': 'sponsor'
    }

    def __unicode__(self):
        return self.name


class Collection(Document):
    _id = StringField(max_length=32, primary_key=True, required=True)
    acronym = StringField(max_length=50, required=True, unique=True)
    name = StringField(max_length=100, required=True, unique_with='acronym')

    sponsors = ListField(ReferenceField(Sponsor, reverse_delete_rule=PULL))
    about = ListField(ReferenceField(Pages, reverse_delete_rule=PULL))

    # Address
    address1 = StringField(max_length=128)
    address2 = StringField(max_length=128)

    # Logo da home da coleção nos 3 idiomas
    home_logo_pt = URLField()
    home_logo_es = URLField()
    home_logo_en = URLField()

    # Logo do cabeçalho da página do periódico, grade, toc, articulo
    header_logo_pt = URLField()
    header_logo_es = URLField()
    header_logo_en = URLField()

    # Logo sem tradução do menu suspenso
    logo_drop_menu = URLField()

    # Logo do menu superior "hamburger" no canto esquerdo
    menu_logo_pt = URLField()
    menu_logo_es = URLField()
    menu_logo_en = URLField()

    # Logo do footer no canto inferiror esquerdo
    logo_footer = URLField()

    metrics = EmbeddedDocumentField(CollectionMetrics)

    meta = {
        'collection': 'collection'
    }

    def __unicode__(self):
        return self.acronym


class Journal(Document):
    _id = StringField(max_length=32, primary_key=True, required=True)
    jid = StringField(max_length=32, required=True, unique=True, )
    collection = ReferenceField(Collection, reverse_delete_rule=CASCADE)
    timeline = EmbeddedDocumentListField(Timeline)
    subject_categories = ListField(field=StringField())
    study_areas = ListField(field=StringField())
    social_networks = EmbeddedDocumentListField(SocialNetwork)
    title = StringField()
    title_iso = StringField()
    short_title = StringField()
    title_slug = StringField()
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
    url_segment = StringField()

    metrics = EmbeddedDocumentField(JounalMetrics)

    meta = {
        'collection': 'journal'
    }

    @property
    def legend_last_issue(self):
        leg_dict = {'acron_title': self.title_iso,
                    'year_pub': self.last_issue.year,
                    'volume': self.last_issue.volume,
                    'number': self.last_issue.number}

        return Legendarium(**leg_dict).stamp

    @property
    def url_last_issue(self):
        leg_dict = {'acron': self.acronym,
                    'year_pub': self.last_issue.year,
                    'volume': self.last_issue.volume,
                    'number': self.last_issue.number}

        return URLegendarium(**leg_dict).url_issue

    @property
    def legend(self):
        leg_dict = {'acron_title': self.title_iso}

        return Legendarium(**leg_dict).stamp

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        document.title_slug = slugify(document.title)

        leg_dict = {'acron': document.acronym}
        document.url_segment = URLegendarium(**leg_dict).get_journal_seg()

    def __unicode__(self):
        return self.legend or 'Journal: %s' % self._id

    def get_mission_by_lang(self, lang):
        """
        Retorna a missão por idioma, caso não encontra retorna ``None``.
        """

        for mission in self.mission:
            if mission.language == lang:
                return mission.description

    @property
    def url(self):
        leg_dict = {
                'acron': self.journal.acronym,
                'year_pub': self.year
        }

        return URLegendarium(**leg_dict).url_journal

signals.pre_save.connect(Journal.pre_save, sender=Journal)


class Issue(Document):

    _id = StringField(max_length=32, primary_key=True, required=True)
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

    is_public = BooleanField(required=True, default=True)
    unpublish_reason = StringField()
    pid = StringField()
    url_segment = StringField()

    meta = {
        'collection': 'issue'
    }

    def __unicode__(self):
        if self.journal:
            return self.legend or 'Issue: %s' % self._id
        else:
            return 'Issue: %s' % self._id

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        leg_dict = {
                'year_pub': document.year,
                'volume': document.volume,
                'number': document.number
        }

        document.url_segment = URLegendarium(**leg_dict).get_issue_seg()

    @property
    def legend(self):
        leg_dict = {'acron_title': self.journal.title_iso,
                    'year_pub': self.year,
                    'volume': self.volume,
                    'number': self.number}

        return Legendarium(**leg_dict).stamp

    @property
    def url(self):
        leg_dict = {
                'acron': self.journal.acronym,
                'year_pub': self.year,
                'volume': self.volume,
                'number': self.number
        }

        return URLegendarium(**leg_dict).url_issue

signals.pre_save.connect(Issue.pre_save, sender=Issue)


class Article(Document):

    _id = StringField(max_length=32, primary_key=True, required=True)
    aid = StringField(max_length=32, required=True, unique=True)

    issue = ReferenceField(Issue, reverse_delete_rule=CASCADE)
    journal = ReferenceField(Journal, reverse_delete_rule=CASCADE)

    title = StringField()
    translated_titles = EmbeddedDocumentListField(TranslatedTitle)
    section = StringField()
    sections = EmbeddedDocumentListField(TranslatedSection)
    authors = ListField(field=StringField())
    abstract = StringField()  # O abstract é sempre em Inglês.
    is_aop = BooleanField()
    order = IntField()
    doi = StringField()
    pid = StringField()
    languages = ListField(field=StringField())
    abstract_languages = ListField(field=StringField())
    original_language = StringField()

    domain_key = StringField()

    xml = StringField()

    htmls = ListField(field=DictField())
    pdfs = ListField(field=DictField())

    created = DateTimeField()
    updated = DateTimeField()

    is_public = BooleanField(required=True, default=True)
    unpublish_reason = StringField()

    elocation = StringField()
    fpage = StringField()
    lpage = StringField()
    url_segment = StringField()

    meta = {
        'collection': 'article'
    }

    def __unicode__(self):
        if self.issue and self.journal:
            return '%s - %s' % (self.legend, self.title)
        else:
            return 'Article: %s' % self._id

    def get_title_by_lang(self, lang):
        """
        Retorna o título do artigo por idioma, caso não encontre o idioma
        retorna o título original, caso não tenha título original retorna ``None``.

        O parâmetro ``lang`` é o acrônimo do idioma, ex.: en, es, pt.
        """

        for title in self.translated_titles:
            if title.language == lang:
                return title.name

        return self.title

    def get_section_by_lang(self, lang):
        """
        Retorna a seção por idioma, caso não encontre retorna o atributo:
        ``article.section``, caso o artigo não tenha o atributo ``section``,
        retorna ``None``.
        """

        for section in self.sections:
            if section.language == lang:
                return section.name

        return self.section

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        leg_dict = {
                'acron': document.journal.acronym,
                'year_pub': document.issue.year,
                'volume': document.issue.volume,
                'number': document.issue.number,
                'fpage': document.fpage,
                'lpage': document.lpage,
                'article_id': document.elocation
        }

        document.url_segment = URLegendarium(**leg_dict).get_article_seg()


    @property
    def legend(self):
        leg_dict = {
                'acron_title': self.journal.title_iso,
                'year_pub': self.issue.year,
                'volume': self.issue.volume,
                'number': self.issue.number,
                'fpage': self.fpage,
                'lpage': self.lpage,
                'article_id': self.elocation
        }

        return Legendarium(**leg_dict).stamp


    @property
    def url(self):
        leg_dict = {
                'acron': self.journal.acronym,
                'year_pub': self.issue.year,
                'volume': self.issue.volume,
                'number': self.issue.number,
                'fpage': self.fpage,
                'lpage': self.lpage,
                'article_id': self.elocation
        }

        return URLegendarium(**leg_dict).url_article

signals.pre_save.connect(Article.pre_save, sender=Article)


class PressRelease(Document):

    _id = StringField(max_length=32, primary_key=True, required=True)
    journal = ReferenceField(Journal, reverse_delete_rule=CASCADE)
    issue = ReferenceField(Issue, reverse_delete_rule=CASCADE)
    article = ReferenceField(Article, reverse_delete_rule=CASCADE)

    title = StringField(max_length=512, required=True)
    language = StringField(max_length=5, required=True)
    content = StringField(required=True)
    doi = StringField(max_length=256)

    publication_date = DateTimeField(required=True)

    created = DateTimeField()
    updated = DateTimeField()

    meta = {
        'collection': 'pressrelease'
    }

    def __unicode__(self):
        return self.title or 'PressRelease: %s' % self._id
