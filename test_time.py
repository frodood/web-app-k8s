from datetime import datetime
from pytz import timezone

format = "%Y-%m-%d %H:%M:%S %Z%z"

now_utc = datetime.now(timezone('Europe/Lisbon'))
print now_utc.strftime(format)
