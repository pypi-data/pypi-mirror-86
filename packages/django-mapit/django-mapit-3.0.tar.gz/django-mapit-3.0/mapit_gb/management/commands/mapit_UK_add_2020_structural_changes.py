# coding=utf8

from __future__ import print_function
from django.core.management.base import BaseCommand
from mapit.models import Area, Generation, Type, Country, NameType, CodeType


class Command(BaseCommand):
    help = "Sort out boundaries for 2020 council changes"

    def add_arguments(self, parser):
        parser.add_argument('--commit', action='store_true')

    def handle(self, *args, **options):
        self.commit = options['commit']
        self.g = Generation.objects.current()
        self.gn = Generation.objects.new()
        self.name_type = NameType.objects.get(code='O')
        self.code_type = CodeType.objects.get(code='gss')
        self.country = Country.objects.get(code='E')

        self.raise_generation_on_everything_else()

        self.areas = Area.objects.filter(generation_low_id__lte=self.g, generation_high_id__gte=self.g)

        self.get_existing()
        self.create_buckinghamshire()

    def _exclude_councils_and_wards(self, qs, names, type_p, type_c):
        areas = Area.objects.filter(type__code=type_p, name__in=names, generation_high=self.g)
        wards = Area.objects.filter(type__code=type_c, parent_area__in=areas, generation_high=self.g)
        qs = qs.exclude(id__in=areas).exclude(id__in=wards)
        return qs

    def raise_generation_on_everything_else(self):
        qs = Area.objects.filter(generation_high=self.g)
        print('%d areas in database' % qs.count())
        qs = self._exclude_councils_and_wards(qs, ('Buckinghamshire County Council',), 'CTY', 'CED')
        qs = self._exclude_councils_and_wards(
            qs, ('Aylesbury Vale District Council', 'South Bucks District Council',
                 'Wycombe District Council', 'Chiltern District Council'), 'DIS', 'DIW')

        if self.commit:
            print('Raising gen high on %d areas' % qs.count())
            updated = qs.update(generation_high=self.gn)
            print('Raised gen high on %d areas' % updated)
        else:
            print('Would raise gen high on %d areas' % qs.count())

    def get_existing(self):
        self.buckinghamshire = Area.objects.get(type__code='CTY', name='Buckinghamshire County Council')

    def _create(self, name, typ, area, gss=None):
        assert(area.polygons.count() == 1)
        geom = area.polygons.get().polygon
        m = Area(
            name=name, type=Type.objects.get(code=typ), country=self.country,
            generation_low=self.gn, generation_high=self.gn,
        )
        if self.commit:
            m.save()
            m.names.update_or_create(type=self.name_type, defaults={'name': name})
            if gss:
                m.codes.update_or_create(type=self.code_type, defaults={'code': gss})
            m.polygons.create(polygon=geom)
        else:
            print('Would create', name, typ)

    def create_buckinghamshire(self):
        """New Buckinghamshire areas are the existing county electoral divisions"""
        self._create('Buckinghamshire Council', 'UTA', self.buckinghamshire, 'E06000060')
        for area in self.areas.filter(type__code='CED', parent_area=self.buckinghamshire):
            self._create(area.name, 'UTW', area)
