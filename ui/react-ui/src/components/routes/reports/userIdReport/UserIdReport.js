import React, { useState } from 'react';
import { JsonToTable } from "react-json-to-table";

function UserIdReport() {
    const [jsonReport, setJsonReport] = useState('');
    const jsonUrl = "https://nate-temp-bucket.s3-us-west-2.amazonaws.com/nate_sample.json";
    
    (async function() {
        const response = await fetch(jsonUrl)
        if (response.ok) {
            const json = await response.json();
            setJsonReport(json);
        } else {
            alert("HTTP-Error: " + response.status)
        }
    })();

    return (
        <div className="userIdRportTable">
            <h1>/users/{'{'}user_id{'}'} Serverless-Artillery Report</h1>
            <JsonToTable json={jsonReport}/>
        </div>
    );
}

export default UserIdReport;