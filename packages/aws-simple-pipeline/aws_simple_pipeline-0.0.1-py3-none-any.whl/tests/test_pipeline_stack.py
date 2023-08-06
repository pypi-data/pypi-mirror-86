import unittest
import tests.helper as hlp
from aws_cdk import core
from aws_simple_pipeline.pipeline_stack import PipelineStack

class TestPipelineStack(unittest.TestCase):
    template_manual_approval_true = None
    template_manual_approval_false = None
    token = None

    def __init__(self, *args, **kwargs):
        with open('tests/pipeline_stack_with_manual_approval_true.txt') as txt_file:
            self.template_manual_approval_true = hlp.load(txt_file)
        with open('tests/pipeline_stack_with_manual_approval_false.txt') as txt_file:
            self.template_manual_approval_false = hlp.load(txt_file)
        self.token = core.SecretValue.secrets_manager(
            "/aws-simple-pipeline/secrets/github/token",
            json_field='github-token',
        )
        unittest.TestCase.__init__(self, *args, **kwargs)

    def synth_with_manual_approval(self, app, manual_approval):
        PipelineStack(app, 
            id="test",
            github_owner="owner",
            github_repo="repo",
            github_branch="branch",
            github_token=self.token,
            notify_emails=["email"],
            policies=["policy"],
            manual_approval_exists=manual_approval
        )

    def test_synth_with_manual_approval_true(self):
        app = core.App()
        self.synth_with_manual_approval(app, True)
        template = hlp.get_template(app, "test")
        self.assertEqual(template, self.template_manual_approval_true)

    def test_synth_with_manual_approval_false(self):
        app = core.App()
        self.synth_with_manual_approval(app, False)
        template = hlp.get_template(app, "test")
        self.assertEqual(template, self.template_manual_approval_false)

    def test_synth_without_manual_approval(self):
        app = core.App()
        PipelineStack(app, 
            id="test",
            github_owner="owner",
            github_repo="repo",
            github_branch="branch",
            github_token=self.token,
            notify_emails=["email"],
            policies=["policy"]
        )
        template = hlp.get_template(app, "test")
        self.assertEqual(template, self.template_manual_approval_false)

if __name__ == '__main__':
    unittest.main()