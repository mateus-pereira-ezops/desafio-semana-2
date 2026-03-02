# Desafio semana 2

Semana 2 – Redes e segurança básica

CloudFormation + API Gateway + Lambda para criar uma API simples, totalmente usando IaC e ambiente Serverless 

## Desafio:
Criar uma API Serverless de “Hello”

Objetivo:
- Implementar uma API REST com o endpoint: GET /hello?name=Ezops

### Resumo
Estudei sobre proxies reversos e API Gateways, para entender suas diferenças e aplicabilidades;

Estudei sobre AWS Lambda, e compreendi o funcionamento do modelo serverless;

Revisei o conceito de infraestrutura como código e seus benefícios, com foco no cloudformation da AWS.

# Serverless Hello API – AWS (CloudFormation + HTTP API + Lambda)

| Serviço                   | Responsabilidade                       |
| ------------------------- | -------------------------------------- |
| Lambda                    | Executar o código Python               |
| API Gateway (HTTP API v2) | Expor endpoint público HTTP            |
| IAM Role                  | Permitir execução da Lambda            |
| CloudWatch Logs           | Armazenar logs                         |
| CloudFormation            | Criar toda a infraestrutura via código |

---

# Estrutura da Infraestrutura (CloudFormation)

O template cria automaticamente:

- IAM Role para Lambda
    
- Função Lambda em Python
    
- HTTP API (v2)
    
- Integration (API → Lambda)
    
- Route `GET /hello`
    
- Stage `$default` com AutoDeploy
    
- Permissão para API Gateway invocar Lambda
    
- Output com URL final
    
---

# Template CloudFormation

Salvar como:

cloudformation-lambda-template.yaml

```yaml
AWSTemplateFormatVersion: "2010-09-09"
Description: Serverless Hello API using HTTP API v2 and Lambda

Resources:
  HelloLambdaRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: hello-lambda-role-mateus-pereira
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

  HelloLambda:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: hello-lambda-iac-mateus-pereira
      Runtime: python3.12
      Handler: index.lambda_handler
      Role: !GetAtt HelloLambdaRole.Arn
      Code:
        ZipFile: |
          import json
          def lambda_handler(event, context):
              query = event.get("queryStringParameters") or {}
              name = query.get("name", "world")
              response = {"message": f"Hello, {name}!"}
              return {
                  "statusCode": 200,
                  "headers": {"Content-Type": "application/json"},
                  "body": json.dumps(response)
              }

  HelloApi:
    Type: AWS::ApiGatewayV2::Api
    Properties:
      Name: hello-http-api
      ProtocolType: HTTP

  HelloIntegration:
    Type: AWS::ApiGatewayV2::Integration
    Properties:
      ApiId: !Ref HelloApi
      IntegrationType: AWS_PROXY
      IntegrationUri: !GetAtt HelloLambda.Arn
      PayloadFormatVersion: "2.0"

  HelloRoute:
    Type: AWS::ApiGatewayV2::Route
    Properties:
      ApiId: !Ref HelloApi
      RouteKey: "GET /hello"
      Target: !Sub "integrations/${HelloIntegration}"

  HelloStage:
    Type: AWS::ApiGatewayV2::Stage
    Properties:
      ApiId: !Ref HelloApi
      StageName: "$default"
      AutoDeploy: true

  LambdaPermission:
    Type: AWS::Lambda::Permission
    Properties:
      FunctionName: !Ref HelloLambda
      Action: lambda:InvokeFunction
      Principal: apigateway.amazonaws.com
      SourceArn: !Sub "arn:aws:execute-api:${AWS::Region}:${AWS::AccountId}:${HelloApi}/*/*"

Outputs:
  ApiUrl:
    Description: "Invoke URL"
    Value: !Sub "https://${HelloApi}.execute-api.${AWS::Region}.amazonaws.com/hello?name=Ezops"
	
```

---
# Deploy via Console (AWS)

1. Acesse CloudFormation
    
2. Clique em **Create stack**
    
3. Escolha **With new resources (standard)**
    
4. Upload do arquivo `cloudformation-lambda-template.yaml`
    
5. Clique em **Next**
    
6. Defina o nome do stack (ex: `hello-serverless-stack`)
    
7. Avance até a etapa final
    
8. Marque:
    
    - `I acknowledge that AWS CloudFormation might create IAM resources`
        
9. Clique em **Create stack**
    

Aguarde o status:

CREATE_COMPLETE

---

# Teste da API

Após a criação:

1. Vá em **Outputs**
    
2. Copie o valor de `ApiUrl`
    
3. Acesse no navegador ou via curl:

```bash
https://<api-id>.execute-api.<region>.amazonaws.com/hello?name=Ezops
```

Resposta:

```json
{  
  "message": "Hello, Ezops!"  
}
```

---
# Custos

Cada requisição gera:

- 1 execução da Lambda
    
- 1 requisição no API Gateway
    

Para este projeto simples, o custo é extremamente baixo e proporcional ao número de acessos.

---

## Conceitos Aprendidos

- Serverless architecture
    
- Infrastructure as Code (IaC)
    
- HTTP API (API Gateway v2)
    
- Lambda proxy integration
    
- IAM Roles e permissões
    
- Permissão explícita para API Gateway invocar Lambda
    
- Estrutura de eventos do HTTP API v2
    
- Uso de Outputs no CloudFormation
    

---
# Conclusão

Foi criada uma API Serverless completa utilizando apenas CloudFormation, sem configuração manual de recursos, seguindo boas práticas de Infraestrutura como Código.

# Próximas etapas (TODO)

Implementar o API Proxy para ver a diferença entre ele e o API Gateway;
Empacotar o código lambda (zip) e armazenar no S3, e referenciar o bucket e key no cloudformation, invés de manter o código inline.
