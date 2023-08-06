API_URL = 'https://manhattan-api-rijk2jvapq-ue.a.run.app/'
EQUITIES_PUBLIC_API_KEY = "-----BEGIN EQUITIES PACKAGE POLITY PUBLIC KEY-----MIIEogIBAAKCAQB+HzZs3fL2vx8l2qnu9z0QhurriGU0vvSJbro2AHuQeBdYbQSC-----END EQUITIES PACKAGE POLITY PUBLIC KEY-----"

DATASET_NAME_DESC_QUERY = '''
    query {
        datasets{
            name
            desc
        }
    }'''

COMPANY_CIK_NAME_QUERY = '''
    query {
        companies{
            cik
            name
        }
    }'''

COMPANY_CIK_TICKER_QUERY = '''
    query {
        companies{
            cik
            ticker
        }
    }'''

EQUITIES_MESSAGES_QUERY = '''
    query {
        equitiesMessages
    }'''

DATASET_QUERY = lambda name, api_key : '''
    query {
        dataset(name:"%s","%s"){
            name
            source
            desc
            years
            results
        }
    }'''%(name,api_key)

COMPANY_QUERY = lambda cik, api_key : '''
    query {
        company(cik:"%s",apiKey : "%s"){
            name
            ticker
            sic 
            countryba
            cityba
            zipba 
            bas1
            bas2
            baph
            countryma
            stprma
            cityma
            zipma
            mas1
            mas2
            countryinc
            stprinc
            ein
            former
            changed
            income
            cash
            balance
            equity
        }
    }'''%(cik,api_key)

FINANCIAL_STATEMENT_QUERY = lambda cik, kind, api_key :'''
    query {
        company(cik:"%s",apiKey:"%s"){
            %s
        }
    }'''%(cik,api_key,kind)

CREATE_NEW_USER_MUTATION = lambda email, name, photoUrl : '''
    mutation{
    createUser(email:"%s",name:"%s",photoUrl:"%s"){ok}
    }
    '''%(email,name,photoUrl)

def take_a_sec():
    print('  - this could take a sec...')

def initialize(verbose):
    if verbose:
        print('> 🏛️\tWelcome to polity.')

def initialized(verbose):
    if verbose:
        print('> ✨\tAuth success. apis connected.')

def failed():
    print('> ☠️\tClient failed to connect to api!')

def datasets(verbose):
    if verbose:
        print('> 🛰️\tRetrieving datasets ...')

def dataset(verbose,name):
    if verbose:
        print('> 📦\tFetching dataset: %s ...'%name)

def companies(verbose):
    if verbose:
        print('> 🛰️\tRetrieving company ciks ...')

def company(verbose,cik):
    if verbose:
        print('> 📦\tFetching company: %s ...'%cik)
    
def financial_statement(verbose,name,kind):
    if verbose:
        print('> 📦\tFetching financial statement: %s for %s ...'%(kind,name))

COMPANY_SCHEMA = lambda data : {
    'name':data['name'],
    'sic':data['sic'],
    'business_address':
        {
            "country":data['countryba'],
            "city": data['cityba'],
            "zip": data['zipba'],
            "adr1": data['bas1'],
            "adr2": data['bas2'],
        },
    'mailing_address':
        {
            "country":data['countryma'],
            "city": data['cityma'],
            "zip": data['zipma'],
            "adr1": data['mas1'],
            "adr2": data['mas2'],
            "state": data['stprma']
        },
    'phone': data['baph'],
    'country_incorporated': data['countryinc'],
    'state_incorporated' : data['stprinc'],
    'ein' : data['ein'],
    'former_name': data['former'],
    'income':data['income'],
    'balance':data['balance'],
    'cash':data['cash'],
    'equity': data['equity']
}