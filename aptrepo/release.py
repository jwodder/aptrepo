from email.utils import parsedate_to_datetime
from .index      import IndexFile

class ReleaseFile(IndexFile):
    @classmethod
    def parse(cls, obj):
        rf = super().parse(obj)
        if 'components' in rf.fields:
            rf.fields["components"] = rf.fields["components"].split()
        elif 'component' in rf.fields:
            rf.fields["components"] = rf.fields.pop("component").split()
        if 'architectures' in rf.fields:
            rf.fields["architectures"] = rf.fields["architectures"].split()
        ### TODO: Split Signed-By field
        for f in ('acquire-by-hash', 'notautomatic', 'butautomaticupgrades'):
            if f in rf.fields and rf.fields[f].lower() in ('no', 'yes'):
                rf.fields[f] = (rf.fields[f].lower() == 'yes')
        for f in ('date', 'valid-until'):
            if f in rf.fields:
                try:
                    rf.fields[f] = parsedate_to_datetime(rf.fields[f])
                except (TypeError, ValueError):
                    pass
        return rf
