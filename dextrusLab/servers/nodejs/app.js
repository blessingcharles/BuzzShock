const res = require("express/lib/response");
const http = require("http");
const fs = require("fs")

// https://nodejs.org/en/docs/guides/anatomy-of-an-http-transaction/

let request_count = 0 ;

console.log("server started at 8080");
http.createServer((request, response) => {

    let body = [];
    request
        .on("error", (err) => {
            response.end("error while reading body: " + err);
        })
        .on("data", (chunk) => {
            body.push(chunk);
        })
        .on("end", () => {
            body = Buffer.concat(body).toString();
            console.log("\n----------------------------\n")
            console.log(request.headers);
            console.log("Body : " , body , " length  : " , body.length.toString())
            console.log(response.statusCode)
            
            request_count += 1
            
            content = `\n---Count : ${request_count}---- Status : ${response.statusCode} --------\n${JSON.stringify(request.headers)}\nBody:[${body.toString()}]\n`
            
            fs.writeFile('output.txt', content, { flag: 'a+' }, err => {})

            response.on("error", (err) => {
                response.end("error while sending response: " + err);
            });

            response.end(
                "Body length: " + body.length.toString() + " Body: " + body
            );
        });
}).listen(80);
