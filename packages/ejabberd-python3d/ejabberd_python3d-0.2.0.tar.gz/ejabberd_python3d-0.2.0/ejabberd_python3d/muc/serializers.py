# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ..serializers import EnumSerializer
from .enums import MUCRoomOption, AllowVisitorPrivateMessage, Affiliation


class MUCRoomOptionSerializer(EnumSerializer):
    enum_class = MUCRoomOption


class AllowVisitorPrivateMessageSerializer(EnumSerializer):
    enum_class = AllowVisitorPrivateMessage


class AffiliationSerializer(EnumSerializer):
    enum_class = Affiliation
