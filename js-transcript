const axios = require('axios')
const getcreds = require('./aws-secrets.js');
let response;
const he = require('he');
 
exports.lambdaHandler = async (event, context) => {
    //Get domain from Environment Variables from lambda
    const DOMAIN = process.env.DOMAIN;

    //Get Creds from AWS Secrets Manager JS - Don't store your keys in the code
    let getcreds = require('./aws-secrets.js');
    let aswSMParams = await getcreds.handler()

    let p = JSON.parse(event.body);
    let issue = p["issue"];
    let playerEmail = p["email"];
    let title = ""
    let transcript = "";
    let customIssueFields ={}; 
    let note = ""
    let newIssueId = 0
    let tags = `["followup"]`
    

    //Encrypt the keys from AWS Secrets Manager
    'use strict';
    const encodedAPIReadKey = Buffer.from(aswSMParams.secrets.readOnlyAPIKey).toString('base64');
    const encodedAPIWriteKey = Buffer.from(aswSMParams.secrets.writeOnlyAPIKey).toString('base64');
    
    //GET AN ISSUE FROM HELPSHIFT - Replace this with a call to the existing system
    try {
        let getIssues = await axios.get(`https://api.helpshift.com/v1/${DOMAIN}/issues/${issue}`, {
             params: {},
             headers: { 
                 Authorization: `Basic ${encodedAPIReadKey}`,
                 Accept: 'application/json'
             }
           })
           .then(function (response){
               title = encodeURI(he.decode(title)).replace(/\&/g, "%26").replace(/=/g,"%3D")
               customIssueFields = response.data.issues[0].custom_fields;
               if(customIssueFields.hasOwnProperty('first_line')){
                   title = customIssueFields.first_line.value;
                }else{
                    title = response.data.issues[0].title;
                }
            
            for(let message of response.data.issues[0].messages)  {
                let userName = ""
                if (message.origin.includes("end-user")){
                    userName = playerEmail
                }else{
                    userName = message.author.name
                }

                transcript += `${userName} : ${unescape(message.body)}\n`
                if (message.origin.includes("end-user")){
                    transcript += `\n`
                }
            }
            
            event = response.data.issues[0];
            if(event.hasOwnProperty('private_notes')){
               note = "\n" + response.data.issues[0].private_notes[0].body;
               note = note.replace(/&amp;/g, "%26");
               note = note.replace(/=/g,"%3D");
               //note = note.replace(/+/g,"%2B");
            }
            transcript += `\n************** Notes for Agent **************\nOriginal Issue URL: https://${DOMAIN}.helpshift.com/admin/issue/${issue}/\n`
            playerEmail = playerEmail.replace(/\+/g,"%2B")
            

            customIssueFields = encodeURI(he.decode(JSON.stringify(customIssueFields)))
        }
         ).then(async function (){
             try{
             //CREATE A NEW ISSUE IN HELPSHIFT
                let makeNewIssue = await axios.post(`https://api.helpshift.com/v1/${DOMAIN}/issues`, 
                `email=${playerEmail}&message-body=${title}&tags=${tags}&custom_fields=${customIssueFields}`,
                    {headers:{
                        Authorization: `Basic ${encodedAPIWriteKey}`,
                        "Content-Type": 'application/x-www-form-urlencoded',
                        "Accept": "application/json"}
                }).then(function (response) {
                    newIssueId = response.data.id;
                    return 200
                })
                }catch (err) {
                    console.log(response)
                    return err;
                }
         }
         ).then(async function (){
            try{
            //ADD A TRANSCRIPT NOTE TO THE ISSUE YOU CREATED
                transcript = encodeURI(he.decode(transcript)).replace(/\&/g, "%26").replace(/=/g,"%3D")
                let bulkIssueUpdate = await axios.post(`https://api.helpshift.com/v1/${DOMAIN}/issues/${newIssueId}/private-notes`, 
                `note-text=${transcript}${note}`,
                    {headers:{
                        Authorization: `Basic ${encodedAPIWriteKey}`,
                        "Content-Type": 'application/x-www-form-urlencoded',
                        "Accept": "application/json"}
                }).then(function (response) {
                    return 200
                })
                }catch (err) {
                    console.log(err);
                    //console.log(response.data.error);
                    return err;
                }
        }
        ).then(async function (){
        }
        )
        } catch (err) {
         console.log(err);
         return err;
     }

    try {
        response = {
            'statusCode': 200,
            'body': JSON.stringify({
                message: 'Success',
                // location: ret.data.trim()
            })
        }
    } catch (err) {
       console.log(err);
        return err;
    }

    return response
};
