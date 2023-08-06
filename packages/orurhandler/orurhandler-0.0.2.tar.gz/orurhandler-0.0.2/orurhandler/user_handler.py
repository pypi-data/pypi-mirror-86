import boto3

class UserHandler():
    
    def __init__(self, AWS_REGION=None, AWS_ACCESS_KEY=None, AWS_SECRET_KEY=None, db=None):
        self.awsRegion = AWS_REGION
        self.awsAccessKey = AWS_ACCESS_KEY
        self.awsSecretKey = AWS_SECRET_KEY
        self.cg = boto3.client(
            'cognito-idp',
            region_name=AWS_REGION,
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY
        )
        self.db = db

    def getUser(self, userPoolId, username):
        return self.cg.admin_get_user(
            UserPoolId=userPoolId,
            Username=username
        )

    def storeUserInDB(self, userId, userPoolId, username, firstName = None, lastName = None, email = None):
        checkUserQuery = ("SELECT id, firstName, lastName, username, email, active FROM User WHERE id = %s")
        params = (userId,)
        results = self.db.get(checkUserQuery, params)
        if not results:
            user = { 'id': None, 'active': False, 'email': None, 'firstName': None, 'lastName': None}
            try:
                cognitoUser = self.getUser(userPoolId, username)
                for attribute in cognitoUser['UserAttributes']:
                    if attribute['Name'] == 'sub':
                        user['id'] = attribute['Value']
                    elif attribute['Name'] == 'email_verified':
                        user['active'] = attribute['Value'] == 'true'
                    elif attribute['Name'] == 'email':
                        user['email'] = attribute['Value']
            except Exception:
                user['id'] = userId
                user['active'] = 1
                user['email'] = email
                user['firstName'] = firstName
                user['lastName'] = lastName
            addUser = ("INSERT INTO User "
                        "(id, email, active, username, firstName, lastName) "
                        "VALUES (%s, %s, %s, %s, %s, %s)")
            dataUser = (user['id'], user['email'], user['active'], username, user['firstName'], user['lastName'])
            self.db.add(addUser, dataUser)