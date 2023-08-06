<!-- Output copied to clipboard! -->

<!-----
NEW: Check the "Suppress top comment" option to remove this info from the output.

Conversion time: 0.336 seconds.


Using this Markdown file:

1. Paste this output into your source file.
2. See the notes and action items below regarding this conversion run.
3. Check the rendered output (headings, lists, code blocks, tables) for proper
   formatting and use a linkchecker before you publish this page.

Conversion notes:

* Docs to Markdown version 1.0β29
* Thu Oct 29 2020 01:59:36 GMT-0700 (PDT)
* Source doc: MedaPay Python SDK
* Tables are currently converted to HTML tables.
----->

# **MedaPay Python SDK**


## **MedaPay Python Library[#](https://developer.pay.meda.chat/docs/nodejs-sdk#medapay-nodejs-library)**

The MedaPay Python SDK provides convenient access to the MedaPay API from applications written in server-side python.

For complete request/response flow and types please check[ HTTP API Guide](https://developer.pay.meda.chat/docs/).


## **Installation

Install the package with:

```
pip install medapaysdk
```


## **Usage

The package needs to be configured with your account's bearer token, which is provided by MedaPay team. Require it and initialize with the provided token and preferred environment value:


```
from medapaysdk.MedaPay import MedaPay

medaPay = MedaPay.MedaPay( isSandBox = True, merchantBearerToken = "Bearer blah-blah-blah", callbackWebhook = "https://test.herokuapps.com/" | None,  callbackVerifyToken = "Verification token" | None )
```



```
You can either set callbackWebhook or not, it'll help you in payment push notification when working with none Amole payment methods
```


**Amole Instance**

**Initialize new Amole Instance**

```
orderId, billref, paymentInstance = medaPay.amole( name = "Abebe bekila", clientPhone = "251911355516", amount = 4, description = "A 4 birr bill to me", otp_sent_callback = def Callback )
```


**Initialize from a pre-existing Bill reference**

```
orderId, billref, paymentInstance = medaPay.amoleBill( name = "Abebe bekila", clientPhone = "251911355516", amount = 4, description = "A 4 birr bill to me", otp_sent_callback = def Callback )
```


_After calling either of the above otp is directly sent. Will throw error if otp couldn’t be sent or if the bill is already paid or canceled_

**Amole Payment**

```
isPaid: bool = paymentInstance.verifyPayment( otp = "4633" )["status"] == "PAYED"
```


**Raw Bill creation**

```
orderId, billref = medaPay.createBill(clientPhone = "251911355516" , amount = 4, name = "Abebe bekila" , method = "CBEBirr" | "mBirr" | "HelloCash", description="Something new")
```


**Bill status retrieval**

```
referenceNumber, accountNumber, status, amount, issuerName, createdAt, description = medaPay.getBillDetails(billref = 10000054)

isPayed: bool = (status == "PAYED")
```

