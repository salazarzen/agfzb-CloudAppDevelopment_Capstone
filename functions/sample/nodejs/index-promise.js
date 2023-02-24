/**
 * Get all dealerships
 */

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

function main(params) {
    return new Promise(function (resolve, reject) {
        const { CloudantV1 } = require('@ibm-cloud/cloudant');
        const { IamAuthenticator } = require('ibm-cloud-sdk-core');
        const authenticator = new IamAuthenticator({ apikey: 'NY832ImwcVT3MtWN7Nf8Tddl4JHF32ZJrxb1oCigK5P7' })
        const cloudant = CloudantV1.newInstance({authenticator: authenticator});
        cloudant.setServiceUrl('https://47758dc9-211d-4a78-a038-617ad9e1338a-bluemix.cloudantnosqldb.appdomain.cloud');
        if (params.st) {
            cloudant.postFind({
                db: 'dealerships',
                selector: {
                    st: params.st
                }
            })
            .then((result)=>{
                let code = 200;
                if (result.result.docs.length == 0) {
                    code = 404;
                }
                resolve({
                    statusCode: code,
                    headers: { 'Content-Type': 'application/json' },
                    body: result.result.docs
                });
            }).catch((err)=>{
                reject(err);
            })
        } else if (params.id) {
            id = parseInt(params.dealerId)
            cloudant.postFind({
                db: 'dealerships',
                selector: {
                    id: parseInt(params.id)
                }
            })
            .then((result)=>{
                let code = 200;
                if (result.result.docs.length == 0) {
                    code = 404;
                }
                resolve({
                    statusCode: code,
                    headers: { 'Content-Type': 'application/json' },
                    body: result.result.docs
                });
            }).catch((err)=>{
                reject(err);
            })
        } else {
            cloudant.postAllDocs({ db: 'dealerships', includeDocs: true, limit: 10 })            
            .then((result)=>{
                let code = 200;
                if (result.result.rows.length == 0) {
                    code = 404;
                }
                resolve({
                    statusCode: code,
                    headers: { 'Content-Type': 'application/json' },
                    body: result.result.rows
                });
            }).catch((err)=>{
                reject(err);
            })
        }
    })
}

function main(params) {

    const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
    const cloudant = CloudantV1.newInstance({
      authenticator: authenticator
    });
    cloudant.setServiceUrl(params.COUCH_URL);

    let dbListPromise = getDbs(cloudant);
    return dbListPromise;
}

function getDbs(cloudant) {
     return new Promise((resolve, reject) => {
         cloudant.getAllDbs()
             .then(body => {
                 resolve({ dbs: body.result });
             })
             .catch(err => {
                  console.log(err);
                 reject({ err: err });
             });
     });
 }
 
 
 /*
 Sample implementation to get the records in a db based on a selector. If selector is empty, it returns all records. 
 eg: selector = {state:"Texas"} - Will return all records which has value 'Texas' in the column 'State'
 */
 function getMatchingRecords(cloudant,dbname, selector) {
     return new Promise((resolve, reject) => {
         cloudant.postFind({db:dbname,selector:selector})
                 .then((result)=>{
                   resolve({result:result.result.docs});
                 })
                 .catch(err => {
                    console.log(err);
                     reject({ err: err });
                 });
          })
 }
 
                        
 /*
 Sample implementation to get all the records in a db.
 */
 function getAllRecords(cloudant,dbname) {
     return new Promise((resolve, reject) => {
         cloudant.postAllDocs({ db: dbname, includeDocs: true, limit: 10 })            
             .then((result)=>{
               resolve({result:result.result.rows});
             })
             .catch(err => {
                console.log(err);
                reject({ err: err });
             });
         })
 }
