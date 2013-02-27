import factory
from datetime import timedelta
from datetime import datetime
from hamster.models import Category, Fact, Tag, Activity, FactTag


class CategoryFactory(factory.Factory):
    FACTORY_FOR = Category
    name = factory.Sequence(lambda n: 'CAT{0}'.format(n))


class TagFactory(factory.Factory):
    FACTORY_FOR = Tag
    name = factory.Sequence(lambda n: 'tag-{0}'.format(n))


class ActivityFactory(factory.Factory):
    FACTORY_FOR = Activity
    name = factory.Sequence(lambda n: str(int(n) + 1))
    category = factory.SubFactory(CategoryFactory)


class RawFactFactory(factory.Factory):
    FACTORY_FOR = Fact
    activity = factory.SubFactory(ActivityFactory)
    start_time = datetime.now()

    @factory.post_generation(extract_prefix='tags')
    def details(self, create, extracted, **kwargs):
        if extracted is not None:
            for tag in extracted:
                FactTag.objects.create(tag=tag, fact=self)

    @factory.post_generation(extract_prefix='finished')
    def finished(self, create, extracted, **kwargs):
        if extracted:
            self.end_time = self.start_time + timedelta(hours=1)
            self.save()


def FactFactory(name=None, **kwargs):
    if name and '@' in name:
        name, cat = name.split('@')
        cat, _ = Category.objects.get_or_create(name=cat)
    else:
        cat = None
    kwargs.update({'activity__category': cat})
    if name:
        kwargs['activity__name'] = name
    return RawFactFactory(**kwargs)
