import datetime as dt
import json
import gql
import ast
import socket
from gql.transport.requests import RequestsHTTPTransport
import urllib3; urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import pandas as pd
from polity import static
from polity.static import (
    CREATE_NEW_USER_MUTATION,
    DATASET_NAME_DESC_QUERY,
    COMPANY_CIK_NAME_QUERY,
    COMPANY_CIK_TICKER_QUERY,
    FINANCIAL_STATEMENT_QUERY,
    DATASET_QUERY,
    COMPANY_QUERY,
    EQUITIES_MESSAGES_QUERY,
    API_URL,
    EQUITIES_PUBLIC_API_KEY,
    COMPANY_SCHEMA    
)
import matplotlib.pyplot as plt 

class Client():

    def __init__(self,api_key,verbose=False,dev=False):

        def invert_dict(to_invert):
            return {v:k for k,v in to_invert.items()}

        self.api_url = API_URL
        self.api_key = api_key
        self.verbose = verbose

        static.initialize(self.verbose)
        
        if dev:
            self.api_key = EQUITIES_PUBLIC_API_KEY
        try:
            self.graphql = self._connect_graphql()
            self.dataset_to_desc = self._fetch_dataset_to_desc_map()
            self.cik_to_name = self._fetch_cik_to_name_map()
            self.cik_to_ticker = self._fetch_cik_to_ticker_map()
            self.name_to_cik = invert_dict(self.cik_to_name)
            self.ticker_to_cik = invert_dict(self.cik_to_ticker)
            static.initialized(self.verbose)
        except Exception as e:
            static.failed()
            print("Exception: %s"%str(e))
            pass

    def _connect_graphql(self):
        transport = RequestsHTTPTransport(
            url=self.api_url,
            use_json=True,
            headers={
                "Content-type": "application/json",
            },
            verify=False,
            retries=3,
        )
        graphql = gql.Client(
            transport=transport,
            fetch_schema_from_transport=True,
        )
        # new user 

        hostname = socket.gethostname()
        ip_addr  = socket.gethostbyname(hostname)
        current_time = str(dt.datetime.now()))

        graphql.execute(
            CREATE_NEW_USER_MUTATION(hostname,ip_addr,current_time)
        )
        return graphql

    def _test(self):
        for cik in self.ciks()[560:565]:
            c = self.company(cik,df=True)
            c['income'].T.plot(kind='bar',stacked=True)
        plt.show()

    def _fetch_equities_messages(self):
        query = gql.gql(EQUITIES_MESSAGES_QUERY)
        return self.graphql.execute(query)['equitiesMessages']

    def _fetch_dataset_to_desc_map(self):
        query = gql.gql(DATASET_NAME_DESC_QUERY)
        return {ds['name']:ds['desc'] for ds in 
            self.graphql.execute(query)['datasets']}

    def _fetch_cik_to_name_map(self):
        query = gql.gql(COMPANY_CIK_NAME_QUERY)
        return {c['cik']:c['name'] for c in 
            self.graphql.execute(query)['companies']}

    def _fetch_cik_to_ticker_map(self):
        query = gql.gql(COMPANY_CIK_TICKER_QUERY)
        return {c['cik']:c['ticker'] for c in 
            self.graphql.execute(query)['companies']}

    def _is_ticker(self,ticker_or_cik):
        return ticker_or_cik.lower().replace(' ','') in self.ticker_to_cik.keys()

    def get_cik_from_ticker(self,ticker):
        return self.ticker_to_cik[ticker.lower().replace(' ','')]

    def dataset(self,name):
        static.dataset(self.verbose,name)
        query = gql.gql(DATASET_QUERY(name,self.api_key))
        return self.graphql.execute(query)['dataset'][0]

    def datasets(self):
        static.datasets(self.verbose)
        return list(self._fetch_dataset_to_desc_map().keys())

    def company(self,ticker_or_cik,df=False):
        def to_df(statement):
            import json 
            statement_df = pd.DataFrame(dict(json.loads(statement)))
            return statement_df.reindex(sorted(statement_df.columns),axis=1)
        
        if self._is_ticker(ticker_or_cik):
            cik = self.get_cik_from_ticker(ticker_or_cik)
        else:
            cik = ticker_or_cik
        
        static.company(self.verbose,cik)
        query = gql.gql(COMPANY_QUERY(cik,self.api_key))
        data = self.graphql.execute(query)['company'][0]
        if df: 
            if data['income']: data['income'] = to_df(data['income'])
            if data['balance']: data['balance'] = to_df(data['balance']) 
            if data['cash']: data['cash'] = to_df(data['cash'])
            if data['equity']: data['equity'] = to_df(data['equity'])
        return COMPANY_SCHEMA(data)

    def ciks(self):
        static.companies(self.verbose)
        return list(self.cik_to_name.keys())

    def company_names(self):
        static.companies(self.verbose)
        return list(self.name_to_cik.keys())
        
    def financial_statement(self,cik,kind,df=False):
        static.financial_statement(self.verbose,self.cik_to_name[cik],kind)
        query = gql.gql(FINANCIAL_STATEMENT_QUERY(cik,kind,self.api_key))
        statement = self.graphql.execute(query)['company'][0][kind]
        statement = pd.DataFrame.from_dict(json.loads(statement))
        if df: return statement.reindex(sorted(statement.columns),axis=1)
        else: return statement
