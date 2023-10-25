from store.enums.base_enum import BaseEnum


class UpperMaterialType(BaseEnum):
    GENUINE_LEATHER = "Genuine leather", "Натуральная кожа"


class LiningMaterialType(BaseEnum):
    NATURAL_FUR = "Natural fur", "Натуральный мех"
    BAIZE = "Baize", "Байка"


class CompletenessType(BaseEnum):
    AVERAGE = "Average", "Средняя"


class TrueToSizeType(BaseEnum):
    EXACT_SIZE = "Exact size", "Размер в размер"
