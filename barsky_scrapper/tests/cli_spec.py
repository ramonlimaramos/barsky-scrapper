

class ScrapperDealerRaterCLISpec:

    def when_execute_cli(self):
        raise NotImplementedError()
    
    def assert_triggered_with_code(self, exit_code):
        raise NotImplementedError()
    
    def assert_suspicious_triggered(self):
        raise NotImplementedError()
    
    def test_001_executes_help_option(self):
        self.when_execute_cli('-h')
        self.assert_triggered_with_code(0)
    
    def test_002_executes_suspicious_option(self):
        self.when_execute_cli('-m', 'buick')
        self.assert_triggered_with_code(1)