import boto3, json

class EncryptorClient:
  def __init__(self, stackName= 'villa-wallet-dev', user=None, pw=None, sessionToken=None, region='ap-southeast-1'):
    self.lambda_ = boto3.client('lambda',
                      aws_access_key_id = user,
                      aws_secret_access_key = pw,
                      aws_session_token = sessionToken,
                      region_name = region )
    self.stackName = stackName
  def createFunctionName(self, inputFunctionName=None, suffix=''):
    if inputFunctionName:
      functionName = inputFunctionName
    else:
      functionName = self.stackName + suffix
    return functionName

  def invoke(self, functionName = '', suffix = 'suffix', payload=None):
    invokeFunctionName = self.createFunctionName(functionName, suffix)
    response = self.lambda_.invoke(
      FunctionName = invokeFunctionName ,
      InvocationType= 'RequestResponse',
      LogType = 'Tail',
      Payload = json.dumps(payload).encode()
    )
    if 'Payload' in response.keys():
      responsePayload = json.loads(response.get('Payload').read())
      return responsePayload
    return response

  def test(self, payload = {'test': 'test'}, functionName = '', suffix='-test'):
    return self.invoke(functionName=functionName,
                       suffix= suffix,
                       payload= payload)

  def encrypt(self, payload = {}, functionName = '', suffix = '-encryptor'):
    return self.invoke(functionName=functionName,
                       suffix= suffix,
                       payload= payload)

  def decrypt(self, payload = {},
              functionName = '',
              suffix = '-decryptor'
              ):
    return self.invoke(functionName=functionName,
                       suffix= suffix,
                       payload= payload)

  def hash(self, payload = {},
              functionName = '',
           suffix = '-phonehasher'
           ):
    return self.invoke(functionName=functionName,
                       suffix= suffix,
                       payload= payload)

  def setDefault(self, payload = {},
              functionName = '',
                 suffix = '-set-default'):
    return self.invoke(functionName=functionName,
                       suffix= suffix,
                       payload= payload)

