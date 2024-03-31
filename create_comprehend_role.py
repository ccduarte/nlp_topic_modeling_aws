from dotenv import load_dotenv
import os
import boto3
import json

load_dotenv()

# Obter credenciais e região da AWS
ACCESS_ID = os.getenv("ACCESS_ID")
ACCESS_KEY = os.getenv("ACCESS_KEY")
REGION = os.getenv("region")

# Inicializar a sessão do boto3 com as credenciais carregadas
session = boto3.Session(
    aws_access_key_id=ACCESS_ID,
    aws_secret_access_key=ACCESS_KEY,
    region_name=REGION
)

# Inicializa o cliente do IAM
iam = session.client('iam')

# 1. Definir a política de confiança para o Amazon Comprehend
trust_policy = {
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Principal": {"Service": "comprehend.amazonaws.com"},
        "Action": "sts:AssumeRole"
    }]
}

# 2. Criar a IAM Role
role_name = 'ComprehendS3AccessRole'
try:
    create_role_response = iam.create_role(
        RoleName=role_name,
        AssumeRolePolicyDocument=json.dumps(trust_policy),
        Description='Role para permitir que o Comprehend acesse o S3',
    )
    role_arn = create_role_response['Role']['Arn']
    print(f"Role criada com ARN: {role_arn}")
except iam.exceptions.EntityAlreadyExistsException:
    print(f"Role {role_name} já existe.")
    role_arn = f"arn:aws:iam::{iam.get_caller_identity().get('Account')}:role/{role_name}"

# 3. Definir a política de permissões para acessar os dados de treino, teste e a saída no S3
policy_document = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket",
                "s3:PutObject"
            ],
            "Resource": [
                "arn:aws:s3:::nlp-topic-modeling",
                "arn:aws:s3:::nlp-topic-modeling/*"
            ]
        }
    ]
}

# 4. Criar a política de permissões
policy_name = 'ComprehendS3AccessPolicy'
policy = iam.create_policy(
    PolicyName=policy_name,
    PolicyDocument=json.dumps(policy_document)
)
policy_arn = policy['Policy']['Arn']

# 5. Anexar a política de permissões à IAM Role
iam.attach_role_policy(
    RoleName=role_name,
    PolicyArn=policy_arn
)
print(f"Política {policy_name} anexada à role {role_name} com sucesso.")
