# coding: utf-8
from datetime import datetime
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
    DictField,
    EmailField,
    # reverse_delete_rule:
    PULL,
    CASCADE,
    # signals
    signals,
)

from legendarium.formatter import short_format
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

    meta = {
        'collection': 'news',
        'indexes': [
            'url',
            'image_url',
            'title',
            'is_public'
        ]
    }


class Pages(Document):
    _id = StringField(max_length=32, primary_key=True, required=True)
    name = StringField(required=True)
    language = StringField(max_length=5, required=True)
    content = StringField(required=True)
    journal = StringField()
    description = StringField()
    # campos de controle:
    created_at = DateTimeField()
    updated_at = DateTimeField()
    slug_name = StringField()

    meta = {
        'collection': 'pages',
        'indexes': [
            'name',
            'journal',
            'slug_name',
        ]
    }

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
        if not self.slug_name:
            self.slug_name = slugify(self.name)
        return super(Pages, self).save(*args, **kwargs)


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
        return '%s: %s' % (self.language, self.description)


class Abstract(EmbeddedDocument):
    language = StringField()
    text = StringField()

    meta = {
        'collection': 'abstract'
    }

    def __unicode__(self):
        return '%s: %s' % (self.language, self.text)


class ArticleKeyword(EmbeddedDocument):
    language = StringField()
    keywords = ListField(field=StringField())

    meta = {
        'collection': 'ArticleKeyword'
    }

    def __unicode__(self):
        return '<Keywords: %s: %s>' % (self.language, self.keywords)


class LastIssue(EmbeddedDocument):
    volume = StringField()
    number = StringField()
    year = IntField()
    label = StringField()
    type = StringField()
    suppl_text = StringField()
    start_month = IntField()
    end_month = IntField()
    sections = EmbeddedDocumentListField('TranslatedSection')
    cover_url = StringField()
    iid = StringField()
    url_segment = StringField()

    meta = {
        'collection': 'last_issue',
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
    h5_metric_year = IntField(default=0)

    def __unicode__(self):
        return '(%s) %s - %s' % (self.h5_metric_year, self.total_h5_index, self.total_h5_median)


class Sponsor(Document):
    _id = StringField(max_length=32, primary_key=True, required=True)
    order = IntField(default=0, required=True, unique=True)
    name = StringField(max_length=256, required=True, unique=True)
    url = URLField()
    logo_url = URLField()

    meta = {
        'collection': 'sponsor',
        'indexes': [
            'name',
            'url',
            'logo_url',
        ]
    }

    def __unicode__(self):
        return self.name


class AOPUrlSegments(EmbeddedDocument):
    url_seg_article = StringField()
    url_seg_issue = StringField()

    def __unicode__(self):
        return "%s/%s" % (self.url_seg_issue, self.url_seg_article)


class Collection(Document):
    _id = StringField(max_length=32, primary_key=True, required=True)
    acronym = StringField(max_length=50, required=True, unique=True)
    name = StringField(max_length=100, required=True, unique_with='acronym')

    name_pt = StringField(max_length=100, default='')
    name_es = StringField(max_length=100, default='')
    name_en = StringField(max_length=100, default='')

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
        'collection': 'collection',
        'indexes': ['acronym', 'name']
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
    next_title = StringField()
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
    editor_email = EmailField()
    enable_contact = BooleanField(default=False)

    mission = EmbeddedDocumentListField(Mission)
    index_at = ListField(field=StringField())
    sponsors = ListField(field=StringField())
    issue_count = IntField()
    last_issue = EmbeddedDocumentField(LastIssue)

    is_public = BooleanField(required=True, default=True)
    unpublish_reason = StringField()
    url_segment = StringField()

    metrics = EmbeddedDocumentField(JounalMetrics)
    scimago_id = StringField()

    meta = {
        'collection': 'journal',
        'indexes': [
            'jid',
            'title',
            'title_slug',
            'acronym',
            'is_public',
            'url_segment',
            'issue_count',
            'current_status',
            'scimago_id',
        ]
    }

    @property
    def legend_last_issue(self):
        leg_dict = {
            'title': self.title,
            'pubdate': str(self.last_issue.year),
            'short_title': self.short_title,
            'volume': self.last_issue.volume,
            'number': self.last_issue.number,
            'suppl': self.last_issue.suppl_text
        }

        return short_format(**leg_dict)

    @property
    def url_last_issue(self):
        leg_dict = {'acron': self.acronym,
                    'year_pub': self.last_issue.year,
                    'volume': self.last_issue.volume,
                    'number': self.last_issue.number,
                    'suppl_number': self.last_issue.suppl_text}

        return URLegendarium(**leg_dict).url_issue

    @property
    def legend(self):
        return self.title_iso

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        document.title_slug = slugify(document.title)
        leg_dict = {'acron': document.acronym}
        document.url_segment = URLegendarium(**leg_dict).get_journal_seg()

    def __unicode__(self):
        return self.legend or 'Journal: %s' % self._id

    def get_mission_by_lang(self, lang):
        """
        Retorna a missão por idioma do param lang, caso não exista damos
        preferência para o Inglês.

        Caso não exista o Inglês devemos retornar a missão em qualquer idioma.

        Caso não exista nenhuma missão cadastrada retornamos None.

        "mission" : [
            {
                "language" : "en",
                "description" : "To publish original articles..."
            },
            {
                "language" : "pt",
                "description" : "Publicar artigos originais..."
            },
            {
                "language" : "es",
                "description" : "Publicar artículos originales..."
            }
        ]
        """

        dict_mission = {m['language']: m['description'] for m in self.mission}

        try:
            return dict_mission[lang]
        except KeyError:
            try:
                return dict_mission['en']
            except KeyError:
                if len(dict_mission) > 0:
                    return next(dict_mission.values())

    @property
    def url(self):
        leg_dict = {
            'acron': self.journal.acronym,
            'year_pub': self.year
        }

        return URLegendarium(**leg_dict).url_journal


    @property
    def url_next_journal(self):
        url_next_journal = ""
        if self.next_title:
            next_journal = self.__class__.objects(
                title_slug=slugify(self.next_title)
            ).first()
            if next_journal:
                url_next_journal = URLegendarium(**{'acron': next_journal.acronym}).get_journal_seg()

        return url_next_journal

    @property
    def url_previous_journal(self):
        url_previous_journal = ""
        if self.previous_journal_ref:
            previous_journal = self.__class__.objects(
                title_slug=slugify(self.previous_journal_ref)
            ).first()
            if previous_journal:
                url_previous_journal = URLegendarium(**{'acron': previous_journal.acronym}).get_journal_seg()

        return url_previous_journal


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

    type = StringField()
    suppl_text = StringField()
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

    assets_code = StringField()

    meta = {
        'collection': 'issue',
        'indexes': [
            'iid',
            'pid',
            'journal',
            'volume',
            'number',
            'year',
            'type',
            'is_public',
            'url_segment',
        ]
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
            'number': document.number,
            'suppl_number': document.suppl_text
        }
        document.url_segment = URLegendarium(**leg_dict).get_issue_seg()

    @property
    def legend(self):
        leg_dict = {
            'title': self.journal.title,
            'pubdate': str(self.year),
            'short_title': self.journal.short_title,
            'volume': self.volume,
            'number': self.number,
            'suppl': self.suppl_text
        }
        return short_format(**leg_dict)

    @property
    def url(self):
        leg_dict = {
            'acron': self.journal.acronym,
            'year_pub': self.year,
            'volume': self.volume,
            'number': self.number,
            'suppl_number': self.suppl_text
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
    abstract = StringField()
    abstracts = EmbeddedDocumentListField(Abstract)
    is_aop = BooleanField()
    order = IntField()
    doi = StringField()
    pid = StringField()
    aop_pid = StringField()
    languages = ListField(field=StringField())
    abstract_languages = ListField(field=StringField())
    original_language = StringField()

    publication_date = StringField()
    type = StringField()
    keywords = EmbeddedDocumentListField(ArticleKeyword)

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
    fpage_sequence = StringField()
    lpage = StringField()
    url_segment = StringField()
    aop_url_segs = EmbeddedDocumentField(AOPUrlSegments)
    scielo_pids = DictField()

    meta = {
        'collection': 'article',
        'indexes': [
            'pid',
            'aop_pid',
            'aid',
            'journal',
            'issue',
            'type',
            'title',
            'order',
            'doi',
            'is_public',
            'fpage',
            'fpage_sequence',
            'lpage',
            'url_segment',
            'elocation',
            'scielo_pids',
        ]
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

    def get_abstract_by_lang(self, lang):
        """
        Retorna a resumo por idioma do param lang.

        Caso não exista nenhum resumo cadastrado retornamos None.

        "abstract" : [
            {
                "language" : "en",
                "text" : "Original articles..."
            },
            {
                "language" : "pt",
                "text" : "Artigos originais..."
            },
            {
                "language" : "es",
                "text" : "Artículos originales..."
            }
        ]
        """

        dict_abstract = {m['language']: m['text'] for m in self.abstracts}

        try:
            return dict_abstract[lang]
        except KeyError:
            return None

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        leg_dict = {
            'acron': document.journal.acronym,
            'year_pub': document.issue.year,
            'volume': document.issue.volume,
            'number': document.issue.number,
            'suppl_number': document.issue.suppl_text,
            'fpage': document.fpage,
            'fpage_sequence': document.fpage_sequence,
            'lpage': document.lpage,
            'article_id': document.elocation,
            'doi': document.doi,
            'order': str(document.order)
        }

        document.url_segment = URLegendarium(**leg_dict).get_article_seg()
        if document.pid is None or len(document.pid) == 0:
            document.pid = document.scielo_pids.get("v2")

    @property
    def legend(self):
        leg_dict = {
            'title': self.journal.title,
            'short_title': self.journal.short_title,
            'pubdate': str(self.issue.year),
            'volume': self.issue.volume,
            'number': self.issue.number,
            'suppl': self.issue.suppl_text
        }
        return short_format(**leg_dict)

    @property
    def url(self):
        return self.url_segment


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
    url = URLField(required=True)

    publication_date = DateTimeField(required=True)

    created = DateTimeField()
    updated = DateTimeField()

    meta = {
        'collection': 'pressrelease',
        'indexes': [
            'journal',
            'issue',
            'article',
        ]
    }

    def __unicode__(self):
        return self.title or 'PressRelease: %s' % self._id


class AuditLogEntry(Document):
    action_choices = {
        'ADD': 'Add',
        'UPD': 'Update',
        'DEL': 'Delete',
    }

    _id = StringField(max_length=32, primary_key=True, required=True)
    user = StringField(max_length=256)
    action = StringField(max_length=3, choices=action_choices.keys())
    created_at = DateTimeField()
    object_class_name = StringField(max_length=128)
    object_pk = StringField(max_length=32)
    description = StringField()
    fields_data = DictField()

    meta = {
        'collection': 'auditlog_entry',
        'indexes': [
            'user',
            'action',
            'created_at',
            'object_class_name',
            'object_pk'
        ]
    }

    @property
    def get_action_value(self):
        if self.action:
            return self.action_choices[self.action]
        else:
            'No action'

    def __unicode__(self):
        return '<AuditLogEntry: %s>' % self._id

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.now()
        return super(AuditLogEntry, self).save(*args, **kwargs)
