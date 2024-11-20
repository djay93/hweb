class ContextProcessors:
    
    @staticmethod
    def get_navigation_items():
        return [
            {
                'label': 'HMDA',
                'class': 'graphs',
                'subpages': [
                    {'label': 'View HMDA Jobs', 'url': 'hmda.list_hmda_jobs', 'external': False},
                    {'label': 'Create HMDA Job', 'url': 'hmda.new_hmda_job', 'external': False},
                ]
            },
            {
                'label': 'Workflows',
                'class': 'iPlugin',
                'subpages': [
                    {'label': 'View Workflows', 'url': 'workflows.list_workflows', 'external': False},
                    {'label': 'Create Workflow', 'url': 'workflows.new_workflow', 'external': False},
                ]
            },
            {
                'label': 'Help',
                'class': 'help',
                'subpages': [
                    {'label': 'Documentation', 'url': 'home.index'},
                    {'label': 'Report a Bug', 'url': 'https://test.com', 'external': True},
                ]
            },
        ]
    
    @staticmethod
    def inject_nav_items():
        return {'nav_items': ContextProcessors.get_navigation_items()}