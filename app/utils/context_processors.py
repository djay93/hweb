class ContextProcessors:
    
    @staticmethod
    def get_navigation_items():
        return [
            {
                'label': 'Dashboard',
                'class': 'home',
                'subpages': [
                    {'label': 'Overview', 'url': 'dashboard.overview', 'external': False},
                    {'label': 'Recent Activities', 'url': 'dashboard.activities', 'external': False},
                    {'label': 'Data Preparation Status', 'url': 'dashboard.data_prep_status', 'external': False},
                ]
            },
            {
                'label': 'Compliance Management',
                'class': 'iPlugin',
                'subpages': [
                    {'label': 'Scenario Management', 'url': 'compliance.test_scenarios', 'external': False},
                    {'label': 'Test Library', 'url': 'compliance.test_library', 'external': False},
                    {'label': 'Schedule Tests', 'url': 'compliance.schedule_tests', 'external': False},
                    {'label': 'Test Calendar', 'url': 'compliance.test_calendar', 'external': False},
                    {'label': 'Issue Tracker', 'url': 'compliance.issue_tracker', 'external': False},
                ]
            },
            {
                'label': 'Test Runs & Results',
                'class': 'play',
                'subpages': [
                    {'label': 'Execute Test', 'url': 'test_runs.execute_tests', 'external': False},
                    {'label': 'Test Progress', 'url': 'test_runs.test_progress', 'external': False},
                    {'label': 'Test Results', 'url': 'test_runs.test_results', 'external': False},
                ]
            },
            {
                'label': 'Data Preparation',
                'class': 'invoices',
                'subpages': [
                    {'label': 'HMDA', 'url': 'hmda.list_hmda_jobs', 'external': False},
                    {'label': 'Data Prep Flows', 'url': 'data_prep.data_prep_flows', 'external': False},
                ]
            },
            {
                'label': 'Reports',
                'class': 'graphs',
                'subpages': [
                    {'label': 'Compliance Test Reports', 'url': 'reports.compliance_reports', 'external': False},
                    {'label': 'Outcome Analysis', 'url': 'reports.outcome_analysis', 'external': False},
                    {'label': 'Audit Logs', 'url': 'reports.audit_logs', 'external': False},
                ]
            },
            {
                'label': 'Settings',
                'class': 'settings',
                'subpages': [
                    {'label': 'Policy Configuration', 'url': 'workflows.list_workflows', 'external': False},
                    {'label': 'Permissions & Roles', 'url': 'workflows.new_workflow', 'external': False},
                    {'label': 'Application Settings', 'url': 'workflows.new_workflow', 'external': False},
                ]
            },
            {
                'label': 'Help',
                'class': 'help',
                'subpages': [
                    {'label': 'Documentation', 'url': 'dashboard.index', 'external': False},
                    {'label': 'FAQs', 'url': 'help.faqs', 'external': False},
                    {'label': 'Contact Support', 'url': 'help.contact_support', 'external': False},
                    {'label': 'Report a Bug', 'url': 'https://test.com', 'external': True},
                ]
            },
        ]
    
    @staticmethod
    def inject_nav_items():
        return {'nav_items': ContextProcessors.get_navigation_items()}
    
    @staticmethod
    def get_breadcrumb_data():
        breadcrumb_map = {
            'dashboard.overview': [
                {'label': 'Dashboard', 'url': 'dashboard.overview'}
            ],
            'data_prep.data_prep_flows': [
                {'label': 'Home', 'url': 'dashboard.overview'},
                {'label': 'Data Preparation', 'url': 'data_prep.data_prep_flows'}
            ],
            'hmda.list_hmda_jobs': [
                {'label': 'Home', 'url': 'dashboard.overview'},
                {'label': 'Data Preparation', 'url': 'data_prep.data_prep_flows'},
                {'label': 'HMDA Jobs', 'url': 'hmda.list_hmda_jobs'}
            ],
            'hmda.view_hmda_job': [
                {'label': 'Home', 'url': 'dashboard.overview'},
                {'label': 'Data Preparation', 'url': 'data_prep.data_prep_flows'},
                {'label': 'HMDA Jobs', 'url': 'hmda.list_hmda_jobs'},
                {'label': 'View Process', 'url': None}
            ],
            # Add more routes as needed
        }

        return {'breadcrumb_map': breadcrumb_map}
