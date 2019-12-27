
class SheetParser:

    COL_VISIT = 0
    COL_FORM = 1
    COL_ASSESS = 2
    COL_NUM = 3
    COL_REF = 4
    COL_DATE = 5
    COL_HEART = 9
    COL_RR = 10
    COL_P = 11
    COL_PR = 12
    COL_QRS = 13
    COL_QT = 14
    COL_QTCF = 15
    # COL_QRS = 16 # QRS Axis

    def __init__(self, meta):
        self.meta = meta
        self.data = dict.fromkeys(self.meta['forms'])
    
    def parseRow(self, row, formname, subject):
        '''
        Assuming external sorting on a per subject basis
        '''
        if self.data[formname] is None:
            self.data[formname] = dict.fromkeys(self.meta['visits']) # VISITS WILL CONTAIN UNIQUE DICTIONARY ENTRY
        
        visit = row[self.COL_VISIT]
        if self.data[formname][visit] is None:
            self.data[formname][visit] = {
                'SubjectID': subject,
                'Form': formname,
                'Visit': visit,
            }

        # object
        self.data[formname][visit][f'DatTim_{row[self.COL_NUM]}'] = row[self.COL_DATE]
        self.data[formname][visit][f'Ref_{row[self.COL_NUM]}'] = row[self.COL_REF]
        self.data[formname][visit][f'Heart_{row[self.COL_NUM]}'] = row[self.COL_HEART]
        self.data[formname][visit][f'RR_{row[self.COL_NUM]}'] = row[self.COL_RR]
        self.data[formname][visit][f'PR_{row[self.COL_NUM]}'] = row[self.COL_PR]
        self.data[formname][visit][f'QRS_{row[self.COL_NUM]}'] = row[self.COL_QRS]
        self.data[formname][visit][f'QT_{row[self.COL_NUM]}'] = row[self.COL_QT]
        self.data[formname][visit][f'QTcF_{row[self.COL_NUM]}'] = row[self.COL_QTCF]
        self.data[formname][visit][f'Assess_{row[self.COL_NUM]}'] = row[self.COL_ASSESS]
    
    def toCSV(self):
        return None
    
    def getFormData(self, formname):
        return self.data[formname]



