# pyshift
shift platfrom api test tool

## Development Environment
---------------
At the bare minimum you'll need the following for your development environment
- [Python](http://www.python.org/)

It is strongly recommended to also install and use the following tools:
- [Pipenv](https://github.com/pypa/pipenv)

### Local Setup

#### 1. Install pipenv
    $ brew install pipenv

#### 2. Clone the project
    $ git clone git@github.com:s-ri/pyshift.git pyshift
    cd pyshift
    chmod a+x cli.py

#### 3. Create and initialize virtualenv for the project
    $ pipenv sync --dev

#### 4. Run the development env
Change virtualenv

    $ pipenv shell

Exit virtualenv

    $ exit

#### 5. Setting settings.yml

    endpoints:
        token: 'https://connect.shift.games/token'
        tokeninfo: 'https://connect.shift.games/tokeninfo'
        payment: 'https://api.shift.games/v1/payment/purchase'

    # https://developer.shift.games/
    shift:
        public_client_id: none
        private_client_id: none
        client_secret: none
        public_key: none

    # https://developer.shift.games/ 
    developer_account:
        grant_type: none
        username: none
        password: none
        scope: none


#### 6. Execute commands
Commands

    client-credentials      Client Credentials Grant Flow
    issue-token             Issued AccessToken
    login                   Simulation shift login
    payment-cancel          Cancel order
    payment-order           Make payment order
    payment-verify-receipt  Verify payment receipt
    refresh-token           Refresh AccessToken
    verify                  Verify id_token

#### 7. Flow

Step 1)  Simulation shift login

    $ ./cli.py login

Step 2) Verify id_token

    $ ./cli.py verify -t {id_token}

    e.g.
    ./cli.py verify -t eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJqdGkiOiIwNDdjZjgyMy1iZDUxLTQzYzUtYThmZi0xZDcwNWEyOTMzN2QiLCJpc3MiOiJzaGlmdC5nYW1lcyIsInN1YiI6IjY5ODEiLCJhdWQiOiI4MDQxNS01MTIucHVibGljIiwiaWF0IjoxNTQ1ODA1NjkxLCJleHAiOjE1NDU5MDU2OTEsInNlcnZpY2VfaWQiOjF9.rQqvRD-OQaMc5KWeMOQju6V71YBL2FS2Ok5Nbp-EhRUI4XlSuzaOKOx6xk1vEGpppo6KwTGJCLGE-1o51vl47tejLLs6aWsDDUH70RwYZAFpvB1gCle_Yz4bbFnHhiQfqGDKJPwmnC2Ilfi6bnhTCczkR4sVET8UYK7BtrTGV4qDj9TbjgWAe0e5CQbXL1m7UpBCIkzq4KOtT82kglBIh-WobNiNHmAMwHmg-PaTU9bt-r7UtQv1FeZnkBESPv4tLkU1neEHRogm0gJ9IPYRHnuIddVKPVYirf-79YWnTW7xiRSFFrFGbInEecUojKRNoC8cpXi1jXuBy4U4Bm6yBg

Step 3) Generate AccessToken
    
    $ ./cli.py issued-token --cache -t {id_token}
    
Step 4) Get shift payment order id

    $ ./cli.py payment-order --cache

Step 5) Verify payment receipt

    $ ./cli.py payment-verify-receipt --cache -o {order_id}

Others

    $  ./cli.py refresh-token --cache