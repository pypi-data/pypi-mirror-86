from localstack.utils.aws import aws_models
EAdmz=super
EAdmS=None
EAdmg=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  EAdmz(LambdaLayer,self).__init__(arn)
  self.cwd=EAdmS
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.EAdmg.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,EAdmg,env=EAdmS):
  EAdmz(RDSDatabase,self).__init__(EAdmg,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,EAdmg,env=EAdmS):
  EAdmz(RDSCluster,self).__init__(EAdmg,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,EAdmg,env=EAdmS):
  EAdmz(AppSyncAPI,self).__init__(EAdmg,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,EAdmg,env=EAdmS):
  EAdmz(AmplifyApp,self).__init__(EAdmg,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,EAdmg,env=EAdmS):
  EAdmz(ElastiCacheCluster,self).__init__(EAdmg,env=env)
class TransferServer(BaseComponent):
 def __init__(self,EAdmg,env=EAdmS):
  EAdmz(TransferServer,self).__init__(EAdmg,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,EAdmg,env=EAdmS):
  EAdmz(CloudFrontDistribution,self).__init__(EAdmg,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,EAdmg,env=EAdmS):
  EAdmz(CodeCommitRepository,self).__init__(EAdmg,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
