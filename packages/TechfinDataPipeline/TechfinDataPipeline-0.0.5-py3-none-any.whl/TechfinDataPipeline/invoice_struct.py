
class InvoiceStruct():
    def __init__(self):
        self.struct = {}
        self.predicted_codes = ['02','03', '12', '13', '14', '15']
        self.accomplished_codes = ['06', '17']
        self.anticipation = ['90', '91', '95', '96']
    
    
    def add_organization(self, org_id):
        if org_id not in self.struct.keys():
            self.struct.update({org_id:{}})
    
    
    def add_invoice(self, org_id, invoice_id):
        self.add_organization(org_id)
        
        if invoice_id not in self.struct[org_id].keys():
            self.struct[org_id].update({invoice_id:{}})
        
        
    def add_installment(self, org_id, invoice_id, installment_id):
        self.add_invoice(org_id, invoice_id)
        
        if installment_id not in self.struct[org_id][invoice_id].keys():
            self.struct[org_id][invoice_id].update({installment_id:{'value':0,
                                                            'balance':0,
                                                            'anticipated':False,
                                                            'duedate':None,
                                                            'paymentdate':None,
                                                            'late_days':None,
                                                            'sequence_code':None,
                                                            'discount':False,
                                                            'docissue':None}})
    
    
    def add_payment(self, org_id, invoice_id, installment_id, value, code, sequence_code, docissue, duedate=None, paymentdate=None):
        self.add_installment(org_id, invoice_id, installment_id)
        
        if code in self.predicted_codes:
            actual_value = self.struct[org_id][invoice_id][installment_id]['value']
            actual_value += value
            
            actual_balance = self.struct[org_id][invoice_id][installment_id]['balance']
            actual_balance += value
            
            discount = self.struct[org_id][invoice_id][installment_id]['discount']
            
            if code == '12':
                discount = True
            elif code == '14':
                discount = False
            
            self.struct[org_id][invoice_id][installment_id].update({'value':actual_value,
                                                            'balance':actual_balance,
                                                            'duedate':duedate,
                                                            'sequence_code':sequence_code,
                                                            'discount':discount,
                                                            'docissue':docissue})
            
        elif code in self.accomplished_codes:
            actual_balance = self.struct[org_id][invoice_id][installment_id]['balance']
            actual_balance += value
            
            late_days = (paymentdate - duedate).days
            
            if late_days < 0:
                late_days = 0
            self.struct[org_id][invoice_id][installment_id].update({'balance':actual_balance,
                                                            'paymentdate':paymentdate,
                                                            'late_days':late_days,
                                                            'sequence_code':sequence_code,
                                                            'docissue':docissue})
            
        elif code in self.anticipation:
            if code in ['90', '95']:
                self.struct[org_id][invoice_id][installment_id].update({'anticipated':True})
            elif code in ['91', '96']:
                self.struct[org_id][invoice_id][installment_id].update({'anticipated':False})
            