import React, { useState, useEffect } from 'react';
import { JsonToTable } from "react-json-to-table";

function UserIdReport() {
    const [jsonReport, setJsonReport] = useState('');
    const jsonUrl = "https://nate-temp-bucket.s3-us-west-2.amazonaws.com/nate_sample.json";
    
    const getReport = async () => {
        const response = await fetch(jsonUrl)
        const json = await response.json();
        setJsonReport(json);
    }

    useEffect(() => {
        if (!jsonReport) getReport();
    }, [jsonReport])

    return (
        <div className="userIdRportTable">
            <h1>/users/{'{'}user_id{'}'} Serverless-Artillery Report</h1>
            <JsonToTable json={jsonReport}/>
        </div>
    );
}

export default UserIdReport;