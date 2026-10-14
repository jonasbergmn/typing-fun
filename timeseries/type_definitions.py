from collections.abc import Mapping
from datetime import datetime
from decimal import Decimal

type Number = int | Decimal
type Points = Mapping[datetime, Number]
