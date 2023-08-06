import logging

import requests
from gitlab import Gitlab

from devcli import DevCliContext


class GitlabClient(Gitlab):

    def __init__(self, ctx: DevCliContext):
        self.token = ctx.config.get('gitlab.token')
        self.host = ctx.config.get('gitlab.host', 'https://gitlab.com')
        self.ctx =ctx
        logging.info(f'gitlab client configured with  {self.token}  and {self.host}')

        super().__init__(url=self.host, private_token=self.token)
        self.graphql_headers = {"Authorization": f"Bearer {self.token}"}


    def graphql(self, query):
        request = requests.post(f'{self.host}/api/graphql', json={'query': query}, headers=self.graphql_headers)
        if request.status_code == 200:
            return request.json()
        else:
            raise Exception()

    def get_projects(self, group_path):
        query = f'''
          query {{
          group(fullPath: "{group_path}") {{
            id
            name
            projects(includeSubgroups: true) {{
              nodes {{
                id
                name
                fullPath
                sshUrlToRepo
              }}
            }}
          }}
        }}'''

        response = self.graphql(query)
        logging.info(f'response for group: {group_path}: {response}')
        return response['data']['group']['projects']['nodes']
