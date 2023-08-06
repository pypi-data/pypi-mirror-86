from localstack.utils.aws import aws_models
jMOdS=super
jMOdT=None
jMOdQ=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  jMOdS(LambdaLayer,self).__init__(arn)
  self.cwd=jMOdT
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.jMOdQ.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,jMOdQ,env=jMOdT):
  jMOdS(RDSDatabase,self).__init__(jMOdQ,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,jMOdQ,env=jMOdT):
  jMOdS(RDSCluster,self).__init__(jMOdQ,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,jMOdQ,env=jMOdT):
  jMOdS(AppSyncAPI,self).__init__(jMOdQ,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,jMOdQ,env=jMOdT):
  jMOdS(AmplifyApp,self).__init__(jMOdQ,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,jMOdQ,env=jMOdT):
  jMOdS(ElastiCacheCluster,self).__init__(jMOdQ,env=env)
class TransferServer(BaseComponent):
 def __init__(self,jMOdQ,env=jMOdT):
  jMOdS(TransferServer,self).__init__(jMOdQ,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,jMOdQ,env=jMOdT):
  jMOdS(CloudFrontDistribution,self).__init__(jMOdQ,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,jMOdQ,env=jMOdT):
  jMOdS(CodeCommitRepository,self).__init__(jMOdQ,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
