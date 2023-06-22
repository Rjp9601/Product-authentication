# Product-Authentication using Blockchain Technology
This project consists of a fully functional anti-countfeit system. All the possible participants in asupply chain such as manufacturer, distributer and consumer are brought together on a unified platform where they register themselves and login to carry out various operations required in a product's sale. All these personal details and product details are saved in the blockchain (here we use Ganache provider) and QR codes and IPFS (InterPlanetary File System) are used for extra layer of protection for the data for successfull Authetication purpose. For final detection and authentication by the end-user we have developed a scanning app.  
The solidity code for the smartcontract is included in a .txt file. The python file 'app.py' is the driver program for the front-end web App whereas the remaining '.java' and '.xml' files are for developing the scanning app in Android Studio. 
First and foremost the smartcontract is deployed via Remix IDE in 'Gnache provider' environment and then the driver program 'app.py' is executed for running our web app where manufacturer, distributor and consumers interact and participate in the sale proccess. QR codes for products are created and saved in the blockchain as well as the invidual personel's and product's details. Updated ownership is traced as sale process moves from manufacturer to distributor to finally the consumer and same is updated in terms for QR code and Blockchain data for the next user to authenticate. Scanning App developed can be used by the buyer to scan the QR code and verify the details from the blochchain.
