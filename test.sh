python3 keygen.py -t rsa -s certSubject -pub keyRSA.pub -priv keyRSA
python3 keygen.py -t ec -s certSubject -pub keyEC.pub -priv keyEC

python3 lock.py -d secrets -p keyRSA.pub -r keyEC -s timmy
python3 unlock.py -d locked -p keyEC.pub -r keyRSA -s timmy
