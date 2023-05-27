from __future__ import annotations
from flask import Flask, render_template, request
import main
import ClientAccount
import TellerAccount

main.AccountInterface.tellerAcc.append(TellerAccount.TellerAccount("tahshins", "tahshin.shahriar", "abc"))
main.AccountInterface.clientAcc.append(ClientAccount.ClientAccount("slavas", "Slava", "slava123","slava89@gmail.com", "7239739273", "hwkqehkwqehkehq"))




app = Flask(__name__)
bank = main.AccountInterface()
teller = None
client =  None

@app.route('/')
def home():
    return render_template('login.html')

#Login Page
@app.route('/login', methods=['POST'])
def login():
    acctypel = request.form.getlist('btnVal')
    acctype = acctypel[-1]

    if acctype == "bt":
        username = request.form['btusername']
        password = request.form['btpasswd']
        global teller
        teller = bank.login(username, password, "bt")
        if teller != False or None:
            return tellerInterface(teller)
        else:
            return 'Input and Select all the fields properly'
    elif acctype == "cl":
        username = request.form['clusername']
        password = request.form['clpasswd']
        global client
        client = bank.login(username, password, "cl")
        if client != False or None:
            return clientInterface(client)
        else:
            return render_template('login.html', errmsg = "Input all the fields correctly")



# Teller Interface
@app.route('/teler')
def tellerInterface(tellerObj):
    name = tellerObj.getUserName()
    idd = tellerObj.employeeID
    return render_template('tellerInterface.html', name=name, ID=idd)

@app.route('/thome')
def tellerHome():
    return tellerInterface(teller)


@app.route('/reg')
def register():
    return render_template('registration.html')


@app.route('/regp', methods=['POST'])
def reg():
    username = request.form['username']
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    addr = request.form['addr']

    clientp = teller.registerClient(username, name, email, phone, addr)

    if clientp != False or None:
        return render_template('regsuccess.html', name=clientp.name_of_user, email=clientp.e_mail, passwd=clientp._password, phone=clientp.phone_no, accno=clientp._accountNumber, addr=clientp.address)
    else:
        return 'Reg failed!'


@app.route('/find')
def find():
    return render_template('find.html')


@app.route('/findp', methods=['POST'])
def findp():
    accno = request.form['accno']
    clientp = teller.findClient(int(accno))

    if clientp != False or None:
        return render_template('regsuccess.html', name=clientp.name, email=clientp.e_mail, phone=clientp.phone_no, accno=clientp._accountNumber, addr=clientp.address)
    else:
        return 'Client is not in the system!'

#Teller Ends



#Client Starts

@app.route('/client')
def clientInterface(clientObj):
    name = clientObj.username
    checkingsBalance = clientObj.chequingAccount.balance
    checkingsAccno = clientObj.chequingAccount.accountNumber
    if len(clientObj.savingsAccounts) > 0:
        savingsAcc = clientObj.savingsAccounts[0]
        savingsBalance = savingsAcc.balance
        savingsAccno = savingsAcc.accountNumber
    else:
        savingsBalance = "NIL"
        savingsAccno = "You don't have a Savings Account" 

    if len(clientObj.creditAccounts) > 0:
        creditAcc = clientObj.creditAccounts[0]
        creditBalance = creditAcc.balance
        creditAccno = creditAcc.accountNumber
    else:
        creditBalance = "NIL"
        creditAccno = "You don't have a Savings Account"        
    
    return render_template('clientInt.html', name=name, cbalance = checkingsBalance, caccno = checkingsAccno, sbalance = savingsBalance, saccno = savingsAccno, ccbalance = creditBalance, ccaccno = creditAccno)

#Home Page
@app.route('/chome')
def chome():
    return clientInterface(client)

#Apply for a Loan
@app.route('/applyLoan')
def loanapp():
    return render_template('applyLoan.html')

@app.route('/loanProccess')
def loanp():
    amount = request.form['amount']
    loanType = request.form['type']
    startDate = request.form['sDate']
    endDate = request.form['eDate']
    loanSuccess = client.applyLoan(amount, loanType, startDate, endDate)
    if loanSuccess == True:
        return "Success, your loan has been granted"
    else:
        return render_template('applyLoan.html', errmsg = "Input the fields appropriately")

# Apply for a Credit Account
@app.route('/applyCredit')
def Credapp():
    return render_template('applyCredit.html')

@app.route('/creditProccess')
def Credp():
    credBalance = request.form['balance']
    credSuccess = client.openCreditAccount(credBalance)
    if credSuccess == True:
        return "Success, your Credit account has been created"
    else:
        return "Error? Credit Account was not proccessed"

#Checkings Account
@app.route('/checkings')
def checkings():
    name = client.username
    checkingsBalance = client.chequingAccount.balance
    checkingsAccno = client.chequingAccount.accountNumber
    return render_template('balanceAccount.html', name = name, caccno = checkingsAccno, cbalance = checkingsBalance)

#SavingsAccount


#CreditAccounts


#TransferFunds
@app.route('/transferFunds')
def transferFunds():
    return render_template('TransFunds.html')
@app.route('/transfundProc' , methods=['POST'])
def transfundProc():
    fromAcc = request.form['fromAcc']
    toAcc = request.form['toAcc']
    amount = request.form['amount']
    if len(client.savingsAccounts) == 0:
        return "You dont have a savings account"
    if fromAcc == "Savings" and toAcc == "Checkings":
        client.savingsAccounts[0].transferBetweenAccounts(float(amount), client.chequingAccount)
        return "success"
    elif fromAcc == "Checkings" and toAcc == "Savings":
        client.chequingAccount.transferBetweenAccounts(float(amount),  client.savingsAccounts[0])
        return "success"
    else:
        return "Input fields properly"    


#AutoPayments

@app.route('/autoPayments')
def autoPayments():
    return render_template('AutoPay.html')

@app.route('/autopaymentsProc')


#Send Money

@app.route('/sendMoney')
def sendMoney():
    return render_template('SendMoney.html')
@app.route('/sendmoneyProc', methods=['POST'])
def sendMoneyProc():
    remail = request.form['remail']
    rphone = request.form['rphone']
    acctype = request.form ['acctype']
    amount = request.form['amount']

    if acctype == "Savings":
        client.savingsAccounts[0].sendEtransfer(float(amount), str(remail), str(rphone))
        return "Etransfer successs"
    elif acctype == "Checkings":
        client.chequingAccount.sendEtransfer(float(amount), str(remail), str(rphone))
        return "Success"
    else:
        return "error"


#WireTransfer

@app.route('/wireTransfer')
def WireTransfer():
    return render_template('WireT.html')





if __name__ == '__main__':
    app.run(debug=True, port=50012)
